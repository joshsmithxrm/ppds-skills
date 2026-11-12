#!/usr/bin/env python3
"""Record the complete released MCP tools/list surface and protocol evidence.

Only initialize, notifications/initialized and tools/list are sent. No tools/call
is available. Capture has a 120-second deadline, bounded pipes and owned-process
cleanup. The writer consumes the resulting data; it never runs this module.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import subprocess
import sys
import threading
import time
from pathlib import Path

from mcp_capture_format import (PROTOCOL_VERSION, decode_json, fixed_requests,
                                require, validate_capture, validate_initialize)


FRAME_BYTES = 2 * 1024 * 1024
PIPE_LIMITS = {"stdout": 4 * 1024 * 1024, "stderr": 1024 * 1024}
PROCESS_SECONDS = 120
SHUTDOWN_SECONDS = 6


class _OwnedProcess:
    """Bounded binary pipes; only the Popen handle we create is signalled."""

    def __init__(self):
        self.deadline = time.monotonic() + PROCESS_SECONDS
        self.data = {"stdout": bytearray(), "stderr": bytearray()}
        self.chunks = queue.Queue(maxsize=1025)
        self.buffer = bytearray()
        self.error = None
        self.proc = subprocess.Popen(
            ["ppds-mcp-server", "--read-only"], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0, shell=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        self.threads = []
        for name in ("stdout", "stderr"):
            thread = threading.Thread(target=self._pump,
                                      args=(name, getattr(self.proc, name)), daemon=True)
            thread.start()
            self.threads.append(thread)

    def _pump(self, name, stream):
        try:
            while True:
                chunk = stream.read(4096)
                if not chunk:
                    if name == "stdout":
                        self.chunks.put_nowait(None)
                    return
                require(len(self.data[name]) + len(chunk) <= PIPE_LIMITS[name],
                        "MCP " + name + " byte limit exceeded")
                self.data[name].extend(chunk)
                if name == "stdout":
                    self.chunks.put_nowait(chunk)
        except Exception as error:
            self.error = error

    def _check(self):
        require(time.monotonic() < self.deadline, "MCP capture deadline expired")
        if self.error is not None:
            raise ValueError("MCP pipe reader failed") from self.error

    def send(self, message):
        self._check()
        data = (json.dumps(message, separators=(",", ":")) + "\n").encode("utf-8")
        require(len(data) <= 1024, "Unexpected request frame size")
        done = threading.Event()
        failures = []

        def write():
            try:
                self.proc.stdin.write(data)
                self.proc.stdin.flush()
            except Exception as error:
                failures.append(error)
            finally:
                done.set()

        writer = threading.Thread(target=write, daemon=True)
        writer.start()
        self.threads.append(writer)
        while not done.wait(0.025):
            self._check()
        require(not failures, "Failed to send MCP request")

    def frame(self):
        while True:
            self._check()
            if b"\n" in self.buffer:
                line, remainder = self.buffer.split(b"\n", 1)
                self.buffer = bytearray(remainder)
                require(0 < len(line) <= FRAME_BYTES, "Empty or oversized MCP frame")
                return decode_json(bytes(line))
            require(len(self.buffer) <= FRAME_BYTES, "Unterminated MCP frame exceeds limit")
            try:
                chunk = self.chunks.get(timeout=0.025)
            except queue.Empty:
                continue
            require(chunk is not None, "MCP server closed before complete response")
            self.buffer.extend(chunk)

    def close(self):
        end = time.monotonic() + SHUTDOWN_SECONDS
        strategy = "already-exited"
        # A blocked write cannot hold up cleanup: terminate first in that case.
        writing = any(thread.is_alive() for thread in self.threads[2:])
        if not writing:
            try:
                self.proc.stdin.close()
            except (BrokenPipeError, OSError):
                pass
        stages = [("stdin-close", None), ("terminate-owned-handle", self.proc.terminate),
                  ("kill-owned-handle", self.proc.kill)]
        if writing:
            stages = stages[1:]
        for label, signal in stages:
            if self.proc.poll() is not None:
                break
            strategy = label
            if signal is not None:
                try:
                    signal()
                except OSError:
                    require(self.proc.poll() is not None, "Could not stop owned MCP process")
            try:
                self.proc.wait(timeout=max(0.001, min(2, end - time.monotonic())))
            except subprocess.TimeoutExpired:
                continue
        require(self.proc.poll() is not None, "Owned MCP process did not stop after kill")
        # wait() reaps the owned handle even if poll() observed a prior exit.
        self.proc.wait(timeout=max(0.001, end - time.monotonic()))
        for thread in self.threads:
            thread.join(timeout=max(0.001, end - time.monotonic()))
        require(not any(thread.is_alive() for thread in self.threads),
                "MCP pipe/writer thread did not stop")
        for stream in (self.proc.stdin, self.proc.stdout, self.proc.stderr):
            stream.close()
        return {"strategy": strategy, "returncode": self.proc.returncode,
                "descendant_shutdown_proven": False}


def record(expected_version=None):
    """Run the fixed exchange; return verified data only after bounded cleanup."""
    process = _OwnedProcess()
    requests = fixed_requests()
    try:
        process.send(requests[0])
        first = process.frame()
        validate_initialize(first, expected_version)
        process.send(requests[1])
        process.send(requests[2])
        second = process.frame()
    finally:
        shutdown = process.close()
    require(process.error is None, "MCP pipe reader failed or exceeded a limit")
    stdout, stderr = bytes(process.data["stdout"]), bytes(process.data["stderr"])
    require(stdout.endswith(b"\n"), "Unterminated final MCP frame")
    frames = [decode_json(line) for line in stdout.splitlines()]
    require(frames == [first, second], "Unexpected extra MCP request/notification/response")
    capture = validate_capture(frames, expected_version)
    require(process.proc.returncode == 0 or shutdown["strategy"] in
            {"terminate-owned-handle", "kill-owned-handle"},
            "MCP server exited unsuccessfully before owned shutdown")
    return capture, frames, requests, stdout, stderr, shutdown


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-version", default=os.environ.get("TARGET_MCP_VERSION"),
                        help="Exact selected PPDS.Mcp package version (or TARGET_MCP_VERSION)")
    parser.add_argument("--out", default="captured-help")
    args = parser.parse_args()
    capture, frames, requests, stdout, stderr, shutdown = record(args.expected_version)

    def encoded(value):
        return (json.dumps(value, indent=2) + "\n").encode("utf-8")

    files = {"mcp-tools.json": encoded(capture), "mcp-protocol-frames.json": encoded(frames),
             "mcp-protocol-requests.json": encoded(requests), "mcp-stdout.jsonl": stdout,
             "mcp-stderr.txt": stderr}
    receipt = {"schema_version": 1, "requested_package_version": args.expected_version,
               "effective_server_version": capture["server"]["version"],
               "protocol_version": PROTOCOL_VERSION, "argv": ["ppds-mcp-server", "--read-only"],
               "python_version": sys.version.split()[0], "shutdown": shutdown,
               "sha256": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
               "recorder_source_sha256": {
                   name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                   for name in ("capture_mcp_tools.py", "mcp_capture_format.py")}}
    files["mcp-capture-receipt.json"] = encoded(receipt)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        (out / name).write_bytes(data)
    sys.stderr.write("captured %s complete tools from %s %s\n" %
                     (capture["tool_count"], capture["server"]["name"], capture["server"]["version"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
