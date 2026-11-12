"""Pure format checks shared by the MCP recorder and data-only artifact reader.

The three-message lane deliberately rejects pagination and unsolicited frames.
It preserves complete tool objects, including schemas and future descriptor fields.
"""
from __future__ import annotations

import copy
import json
import math


PROTOCOL_VERSION = "2025-03-26"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, "Duplicate JSON object key")
        value[key] = item
    return value


def _invalid_constant(value):
    raise ValueError("Non-finite JSON number: " + value)


def _finite_float(value):
    number = float(value)
    require(math.isfinite(number), "JSON number exceeds finite floating-point range")
    return number


def decode_json(data):
    """Decode UTF-8 JSON without silently losing duplicate keys or NaN values."""
    if isinstance(data, bytes):
        data = data.decode("utf-8", errors="strict")
    return json.loads(data, object_pairs_hook=_unique_object,
                      parse_constant=_invalid_constant, parse_float=_finite_float)


def fixed_requests() -> list[dict]:
    return [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name": "ppds-skills-capture", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    ]


def _response(frame, request_id):
    require(isinstance(frame, dict) and set(frame) == {"jsonrpc", "id", "result"},
            "Unexpected response, error, request or notification")
    require(frame["jsonrpc"] == "2.0" and type(frame["id"]) is int
            and frame["id"] == request_id, "Unexpected JSON-RPC response id/version")
    require(isinstance(frame["result"], dict), "Missing response result")
    return frame["result"]


def validate_initialize(frame, expected_version=None):
    result = _response(frame, 1)
    require(result.get("protocolVersion") == PROTOCOL_VERSION,
            "Unexpected negotiated protocol version")
    server = result.get("serverInfo")
    require(isinstance(server, dict) and server.get("name") == "ppds-mcp-server",
            "Unexpected MCP server identity")
    version = server.get("version")
    require(isinstance(version, str) and version and version == version.strip(),
            "Missing MCP server version")
    if expected_version is not None:
        # PPDS serverInfo deliberately omits informational-version build metadata.
        require(isinstance(expected_version, str) and bool(expected_version),
                "Missing expected MCP package version")
        require(version == expected_version.split("+", 1)[0],
                "MCP effective version differs from requested package version")
    capabilities = result.get("capabilities")
    require(isinstance(capabilities, dict) and isinstance(capabilities.get("tools"), dict),
            "MCP tools capability missing")
    return server


def _object_schema(schema):
    require(isinstance(schema, dict) and schema.get("type") == "object"
            and isinstance(schema.get("properties", {}), dict),
            "Missing object JSON schema")
    required = schema.get("required", [])
    require(isinstance(required, list) and all(isinstance(name, str) for name in required),
            "Invalid required input properties")
    require(len(required) == len(set(required))
            and all(name in schema.get("properties", {}) for name in required),
            "Duplicate or unknown required input property")


def validate_capture(frames, expected_version=None) -> dict:
    """Validate exactly initialize/tools-list responses and retain full descriptors.

    This checks the required descriptor shape, not every JSON Schema keyword.
    It is a protocol-completeness check, not public-package/source attestation.
    """
    require(isinstance(frames, list) and len(frames) == 2,
            "Capture must contain exactly two response frames")
    server = validate_initialize(frames[0], expected_version)
    result = _response(frames[1], 2)
    require("nextCursor" not in result, "Paginated tools/list is incomplete")
    tools = result.get("tools")
    require(isinstance(tools, list) and bool(tools), "Missing nonempty tools/list result")
    names = []
    for tool in tools:
        require(isinstance(tool, dict) and isinstance(tool.get("name"), str)
                and bool(tool["name"].strip()) and isinstance(tool.get("description"), str)
                and bool(tool["description"].strip()), "Invalid tool descriptor")
        _object_schema(tool.get("inputSchema"))
        if "outputSchema" in tool:
            _object_schema(tool["outputSchema"])
        names.append(tool["name"])
    require(len(names) == len(set(names)), "Duplicate tool name")
    return {"server": copy.deepcopy(server), "tool_count": len(tools),
            "protocol_version_negotiated": PROTOCOL_VERSION,
            "tools": copy.deepcopy(sorted(tools, key=lambda tool: tool["name"]))}
