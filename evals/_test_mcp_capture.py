"""Offline MCP recorder controls: retained data and in-memory process doubles only."""
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import capture_mcp_tools as recorder
from mcp_capture_format import (PROTOCOL_VERSION, decode_json, fixed_requests,
                                validate_capture)


def sample_frames():
    return [
        {"jsonrpc": "2.0", "id": 1, "result": {
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {"tools": {}},
            "serverInfo": {"name": "ppds-mcp-server", "version": "1.3.0", "title": "PPDS"}}},
        {"jsonrpc": "2.0", "id": 2, "result": {"tools": [
            {"name": "ppds_z", "description": "  Preserve whitespace.\n",
             "inputSchema": {"type": "object", "properties": {
                 "items": {"type": "array", "items": {"anyOf": [
                     {"type": "null"}, {"type": "object", "properties": {"key": {"type": "string"}}}]}}},
                 "required": ["items"], "additionalProperties": False},
             "outputSchema": {"type": "object", "properties": {"count": {"type": "integer"}}},
             "annotations": {"readOnlyHint": True}, "_meta": {"future": [1, None, "x"]}},
            {"name": "ppds_a", "description": "Another complete descriptor.",
             "inputSchema": {"type": "object", "properties": {}}},
        ]}},
    ]


def raw_frames(frames):
    return b"".join((json.dumps(frame) + "\n").encode("utf-8") for frame in frames)


class _Input(io.BytesIO):
    def __init__(self, process):
        super().__init__()
        self.process = process

    def close(self):
        if not self.closed:
            self.process.sent = self.getvalue()
            if self.process.exit_on_close and self.process.returncode is None:
                self.process.returncode = 0
        super().close()


class FakeProcess:
    """No process is launched; BytesIO pipes exercise the real recorder pump."""
    def __init__(self, stdout=None, stderr=b"", exit_on_close=True, terminate_exits=True):
        self.stdout = io.BytesIO(raw_frames(sample_frames()) if stdout is None else stdout)
        self.stderr = io.BytesIO(stderr)
        self.stdin = _Input(self)
        self.exit_on_close = exit_on_close
        self.terminate_exits = terminate_exits
        self.returncode = None
        self.sent = b""
        self.waits = self.terminated = self.killed = 0

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        self.waits += 1
        if self.returncode is None:
            raise subprocess.TimeoutExpired("in-memory MCP double", timeout)
        return self.returncode

    def terminate(self):
        self.terminated += 1
        if self.terminate_exits:
            self.returncode = -15

    def kill(self):
        self.killed += 1
        self.returncode = -9


class McpCaptureTests(unittest.TestCase):
    def test_complete_descriptors_and_nested_schemas_are_retained(self):
        frames = sample_frames()
        original = copy.deepcopy(frames)
        output = validate_capture(frames, "1.3.0+selected-build")
        self.assertEqual(output["tools"], list(reversed(frames[1]["result"]["tools"])))
        self.assertEqual(output["server"], frames[0]["result"]["serverInfo"])
        self.assertEqual(output["protocol_version_negotiated"], PROTOCOL_VERSION)
        output["tools"][0]["inputSchema"]["properties"]["new"] = {}
        self.assertEqual(frames, original)

    def test_retained_candidate_schema_capture_roundtrips(self):
        frames = decode_json((ROOT / "captured-help/mcp-protocol-frames.json").read_bytes())
        original = decode_json((ROOT / "captured-help/mcp-tools.json").read_bytes())
        output = validate_capture(frames, original["server"]["version"])
        self.assertEqual(output["tool_count"], original["tool_count"])
        self.assertEqual(output["tools"], original["tools"])
        self.assertEqual(output["server"], original["server"])
        self.assertEqual(output["protocol_version_negotiated"], original["protocol_version_negotiated"])

    def test_json_rejects_lossy_or_malformed_values(self):
        for data in (b'{"id":1,"id":2}', b'{"nested":{"x":1,"x":2}}', b'{"x":NaN}',
                     b'{"x":Infinity}', b'{"x":-Infinity}', b'{"x":1e999}',
                     b'{broken}', b'{"x":"\xff"}'):
            with self.subTest(data=data), self.assertRaises((ValueError, UnicodeError)):
                decode_json(data)

    def test_protocol_and_identity_fail_closed(self):
        mutations = [
            lambda f: f.pop(),
            lambda f: f.append(copy.deepcopy(f[1])),
            lambda f: f[0].update(id=True),
            lambda f: f[1].update(id=1),
            lambda f: f[1].update(error={"code": -1}),
            lambda f: f[0].update(method="notifications/message"),
            lambda f: f[0]["result"].update(protocolVersion="2024-11-05"),
            lambda f: f[0]["result"]["serverInfo"].update(name="another-server"),
            lambda f: f[0]["result"]["serverInfo"].update(version="1.3.1"),
            lambda f: f[0]["result"].update(capabilities={}),
            lambda f: f[1]["result"].update(nextCursor=None),
            lambda f: f[1]["result"].update(tools=[]),
        ]
        for mutate in mutations:
            frames = sample_frames()
            mutate(frames)
            with self.subTest(frames=frames), self.assertRaises(ValueError):
                validate_capture(frames, "1.3.0")

    def test_incomplete_schemas_and_duplicate_tools_fail_closed(self):
        mutations = [
            lambda t: t[0].pop("inputSchema"),
            lambda t: t[0].update(inputSchema={"type": "string"}),
            lambda t: t[0]["inputSchema"].update(properties=[]),
            lambda t: t[0]["inputSchema"].update(required=["items", "items"]),
            lambda t: t[0]["inputSchema"].update(required=["missing"]),
            lambda t: t[0]["inputSchema"].update(required=[{}]),
            lambda t: t[0].update(outputSchema=[]),
            lambda t: t[0].update(description=""),
            lambda t: t[0].update(name=""),
            lambda t: t[1].update(name=t[0]["name"]),
        ]
        for mutate in mutations:
            frames = sample_frames()
            mutate(frames[1]["result"]["tools"])
            with self.subTest(frames=frames), self.assertRaises(ValueError):
                validate_capture(frames, "1.3.0")

    def test_exchange_sends_only_fixed_requests_and_reaps_child(self):
        process = FakeProcess(stderr=b"synthetic diagnostic\n")
        with mock.patch.object(recorder.subprocess, "Popen", return_value=process) as launch:
            result = recorder.record("1.3.0")
        self.assertEqual([decode_json(line) for line in process.sent.splitlines()], fixed_requests())
        self.assertEqual(launch.call_args.args[0], ["ppds-mcp-server", "--read-only"])
        self.assertEqual(result[0], validate_capture(sample_frames(), "1.3.0"))
        self.assertEqual(result[3], raw_frames(sample_frames()))
        self.assertEqual(result[4], b"synthetic diagnostic\n")
        self.assertEqual(result[5]["returncode"], 0)
        self.assertGreater(process.waits, 0)
        self.assertTrue(process.stdout.closed and process.stderr.closed and process.stdin.closed)

    def test_invalid_initialize_stops_before_tools_list_and_cleans_up(self):
        frames = sample_frames()
        frames[0]["result"]["serverInfo"]["version"] = "1.4.0"
        process = FakeProcess(stdout=raw_frames(frames))
        with mock.patch.object(recorder.subprocess, "Popen", return_value=process):
            with self.assertRaises(ValueError):
                recorder.record("1.3.0")
        self.assertEqual([decode_json(line) for line in process.sent.splitlines()], fixed_requests()[:1])
        self.assertIsNotNone(process.returncode)

    def test_extra_blank_truncated_and_error_frames_are_rejected(self):
        inputs = [raw_frames(sample_frames()) + b'{"jsonrpc":"2.0","method":"unexpected"}\n',
                  raw_frames(sample_frames()) + b"\n", raw_frames(sample_frames())[:-1],
                  b'{"jsonrpc":"2.0","id":1,"error":{"code":-1}}\n',
                  b'{"jsonrpc":"2.0","id":1,"id":1,"result":{}}\n']
        for data in inputs:
            process = FakeProcess(stdout=data)
            with self.subTest(data=data), mock.patch.object(recorder.subprocess, "Popen", return_value=process):
                with self.assertRaises(ValueError):
                    recorder.record("1.3.0")
            self.assertIsNotNone(process.returncode)
            self.assertGreater(process.waits, 0)

    def test_pipe_and_frame_limits_stop_capture(self):
        limits = [("FRAME_BYTES", 16, FakeProcess()),
                  ("PIPE_LIMITS", {"stdout": 16, "stderr": 16}, FakeProcess()),
                  ("PIPE_LIMITS", {"stdout": 4096, "stderr": 16}, FakeProcess(stderr=b"x" * 17))]
        for name, limit, process in limits:
            with self.subTest(name=name, limit=limit), mock.patch.object(recorder, name, limit), \
                    mock.patch.object(recorder.subprocess, "Popen", return_value=process):
                with self.assertRaises(ValueError):
                    recorder.record("1.3.0")
            self.assertIsNotNone(process.returncode)

    def test_deadline_failure_still_reaps_owned_process(self):
        process = FakeProcess()
        with mock.patch.object(recorder, "PROCESS_SECONDS", -1), \
                mock.patch.object(recorder.subprocess, "Popen", return_value=process):
            with self.assertRaisesRegex(ValueError, "deadline"):
                recorder.record("1.3.0")
        self.assertGreater(process.waits, 0)
        self.assertIsNotNone(process.returncode)

    def test_owned_terminate_and_kill_fallback_are_reported(self):
        for terminate_exits, strategy in [(True, "terminate-owned-handle"), (False, "kill-owned-handle")]:
            process = FakeProcess(exit_on_close=False, terminate_exits=terminate_exits)
            with self.subTest(strategy=strategy), mock.patch.object(recorder.subprocess, "Popen", return_value=process):
                result = recorder.record("1.3.0")
            self.assertEqual(result[5]["strategy"], strategy)
            self.assertFalse(result[5]["descendant_shutdown_proven"])
            self.assertEqual(process.terminated, 1)
            self.assertEqual(process.killed, int(not terminate_exits))

    def test_unsuccessful_server_exit_is_not_success(self):
        process = FakeProcess()
        process.returncode = 7
        with mock.patch.object(recorder.subprocess, "Popen", return_value=process):
            with self.assertRaisesRegex(ValueError, "exited unsuccessfully"):
                recorder.record("1.3.0")

    def test_cli_writes_hash_bound_evidence_and_uses_selected_version(self):
        frames = sample_frames()
        result = (validate_capture(frames, "1.3.0"), frames, fixed_requests(), raw_frames(frames), b"",
                  {"strategy": "stdin-close", "returncode": 0, "descendant_shutdown_proven": False})
        with tempfile.TemporaryDirectory(prefix="ppds-mcp-offline-") as directory, \
                mock.patch.object(recorder, "record", return_value=result) as record, \
                mock.patch.dict(os.environ, {"TARGET_MCP_VERSION": "1.3.0"}), \
                mock.patch.object(sys, "argv", ["capture_mcp_tools.py", "--out", directory]):
            self.assertEqual(recorder.main(), 0)
            record.assert_called_once_with("1.3.0")
            receipt = decode_json((Path(directory) / "mcp-capture-receipt.json").read_bytes())
            self.assertEqual(receipt["requested_package_version"], "1.3.0")
            self.assertEqual(receipt["effective_server_version"], "1.3.0")
            self.assertEqual(len(receipt["sha256"]), 5)
            for name, digest in receipt["sha256"].items():
                self.assertEqual(hashlib.sha256((Path(directory) / name).read_bytes()).hexdigest(), digest)
            for name, digest in receipt["recorder_source_sha256"].items():
                self.assertEqual(hashlib.sha256((ROOT / "tools" / name).read_bytes()).hexdigest(), digest)

    def test_failed_record_does_not_emit_success_files(self):
        with tempfile.TemporaryDirectory(prefix="ppds-mcp-offline-") as directory, \
                mock.patch.object(recorder, "record", side_effect=ValueError("incomplete")), \
                mock.patch.object(sys, "argv", ["capture_mcp_tools.py", "--out", directory]):
            with self.assertRaises(ValueError):
                recorder.main()
            self.assertEqual(list(Path(directory).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
