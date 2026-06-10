#!/usr/bin/env python3
"""Capture the released ppds-mcp-server tool surface over stdio JSON-RPC.

Spawns the server with --read-only, performs the MCP initialize handshake,
calls tools/list, and writes captured-help/mcp-tools.json with the server
version and every tool name + description. Skills cite this file — never a
hand-written tool list.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    proc = subprocess.Popen(
        ["ppds-mcp-server", "--read-only"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )

    def send(msg: dict) -> None:
        assert proc.stdin is not None
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()

    def recv() -> dict:
        assert proc.stdout is not None
        while True:
            line = proc.stdout.readline()
            if not line:
                raise RuntimeError("server closed stdout")
            line = line.strip()
            if not line:
                continue
            return json.loads(line)

    send(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "ppds-skills-capture", "version": "0.1"},
            },
        }
    )
    init = recv()
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    tools_resp = recv()
    proc.terminate()

    server_info = init.get("result", {}).get("serverInfo", {})
    tools = tools_resp.get("result", {}).get("tools", [])
    out = {
        "server": server_info,
        "tool_count": len(tools),
        "tools": [
            {
                "name": t.get("name"),
                "description": (t.get("description") or "").strip(),
            }
            for t in sorted(tools, key=lambda t: t.get("name") or "")
        ],
    }
    Path("captured-help").mkdir(exist_ok=True)
    Path("captured-help/mcp-tools.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8"
    )
    sys.stderr.write(
        f"captured {len(tools)} tools from {server_info.get('name')} "
        f"{server_info.get('version')}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
