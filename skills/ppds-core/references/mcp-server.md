# ppds-mcp-server — setup and session safety flags

Source of truth: released `PPDS.Mcp` 1.0.0 (NuGet) and its public README.
The tool list lives in [mcp-tools.md](mcp-tools.md), captured from a live
`tools/list` call — never cite a tool that is not in that file.

## Install

```bash
dotnet tool install -g PPDS.Mcp
```

The server binary is `ppds-mcp-server` (stdio transport, JSON-RPC). It reads
authentication from the same PPDS profile store as the CLI — create a profile
with `ppds auth create` first.

## Register with Claude Code

```json
{
  "mcpServers": {
    "ppds": {
      "command": "ppds-mcp-server",
      "args": ["--read-only"]
    }
  }
}
```

## Session safety flags

These are parsed at server startup (`McpSessionOptions`). They are the
protocol-level safety story — set them in the MCP client config, not at tool
call time:

| Flag | Effect |
|------|--------|
| `--read-only` | Every DML operation (INSERT / UPDATE / DELETE) is rejected for the whole session. SELECT and metadata reads still work. |
| `--allowed-env <url>` | Allowlist for the `ppds_env_select` tool; repeat the flag for multiple environments. **If no `--allowed-env` is given, environment switching is disabled entirely** — the session stays locked to the startup environment. |
| `--profile <name>` | Lock the session to a named auth profile (default: active profile at first tool call). |
| `--environment <url>` | Lock the session to an environment URL (default: the profile's selected environment). |

Recommended default posture for agent sessions:

```bash
# Exploration / analysis sessions
ppds-mcp-server --read-only

# Mutation sessions, pinned to one known-safe environment
ppds-mcp-server --environment https://yourorg-dev.crm.dynamics.com \
  --allowed-env https://yourorg-dev.crm.dynamics.com
```

Note: the server prints nothing when invoked with `--help` in 1.0.0 — the
flags above come from the released source and README, both public.

## Logging

Server logs go to **stderr** (stdout is reserved for the MCP protocol).
Verbosity: `--log-level <level>` or the `PPDS_MCP_LOG_LEVEL` environment
variable (default Warning).
