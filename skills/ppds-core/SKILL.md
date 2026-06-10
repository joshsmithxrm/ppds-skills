---
name: ppds-core
description: Install, authenticate, and safely operate the Power Platform Developer Suite (PPDS) CLI and MCP server against Microsoft Dataverse — auth profiles, environment selection, the environment-safety model, and error interpretation. Use when the user wants to connect to Dataverse with PPDS, set up `ppds` or `ppds-mcp-server`, manage auth profiles or environments, decide between the PPDS CLI and MCP surfaces, or interpret a PPDS error or exit code. Load this skill first before any other ppds-* skill.
license: MIT
metadata:
  ppds_cli_version_tested: "1.2.0-rc.4"
  ppds_mcp_version_tested: "1.0.0"
---

# PPDS Core — connect, select, stay safe

PPDS (Power Platform Developer Suite) is a single .NET global tool giving you
a typed CLI, an MCP server, a TUI, and NuGet libraries over Microsoft
Dataverse. One install, no Python, no PAC CLI dependency. Docs:
https://joshsmithxrm.github.io/ppds-docs/

```bash
dotnet tool install -g PPDS.Cli --prerelease   # CLI: `ppds`
dotnet tool install -g PPDS.Mcp                # MCP server: `ppds-mcp-server`
```

Verify: `ppds --version`. Flag tables in references/ were generated from CLI
**1.2.0-rc.4**; if the installed major/minor differs, prefer live `--help`.

## Surface routing (applies to every ppds-* skill)

**The CLI is the primary surface for terminal agents.** Use the MCP server
instead when either holds:

1. The host has no shell (an MCP-only client), or
2. You want protocol-level session safety the shell cannot give you —
   `--read-only` (all DML rejected for the session) and `--allowed-env`
   (environment switching locked to an allowlist). Setup:
   [references/mcp-server.md](references/mcp-server.md).

Where an MCP tool mirrors a CLI command this package names it, e.g.
`ppds env list` ↔ `ppds_env_list`. The released server (1.0.0) exposes 41
tools — the authoritative list is
[references/mcp-tools.md](references/mcp-tools.md). The CLI surface is wider;
anything without an MCP tool routes to the CLI.

## Authentication profiles

Profiles are stored per-machine and shared by CLI, MCP server, and TUI.
All methods and exact flags: [references/cli-auth.md](references/cli-auth.md).

```bash
ppds auth create --name dev                    # interactive browser (default)
ppds auth create --name dev --deviceCode      # headless / SSH / containers
ppds auth create --name ci --applicationId <app-id> --clientSecret <secret> --tenant <tenant-id>
```

Also supported: certificate file/store (`--certificateDiskPath` /
`--certificateThumbprint`), `--managedIdentity`, and workload identity
federation (`--githubFederated`, `--azureDevOpsFederated`).

Manage: `ppds auth list`, `ppds auth select --index <n>` (or `--name <n>`),
`ppds auth who`, `ppds auth update`, `ppds auth delete`, `ppds auth clear`.

## Environment selection

A profile has one selected environment; commands accept per-call overrides.
Exact flags: [references/cli-env.md](references/cli-env.md).

```bash
ppds env list --filter contoso          # discover (name/URL/ID, partial ok)
ppds env select --environment <url-or-name>
ppds env who                            # identity + selected environment
```

Per-call override on most commands: `--environment <url>` (alias `-env`) and
`--profile <name>` (`-p`). `ppds org ...` is an alias for `ppds env ...`.

## The safety model — hard rules

These rules are not style; agents must follow them.

1. **Know your target before any mutation.** Run `ppds env who` (CLI) or
   `ppds_auth_who` (MCP) and state the environment to the user before the
   first write of a session. Environments have a configured
   `EnvironmentConfig.Type`: `Production`, `Sandbox`, `Development`, `Test`,
   `Trial`, or `Unknown`. **Production gets blocked-by-default DML that
   requires confirmation with a preview; treat `Unknown` with the same
   suspicion.**

2. **Multi-environment confirmation.** When a session has touched more than
   one environment, or a command carries an explicit `--environment`
   override, restate the exact target (URL, not nickname) and get the user's
   confirmation before executing any mutation. Cross-environment DML defaults
   to read-only (`cross_env_dml_policy: ReadOnly`); a Production target
   always prompts even when the policy is `Allow`.

3. **Dry-run first.** Every PPDS mutation surface has a preview: use it,
   show the user the result, then execute. `ppds query sql --dry-run` (DML
   plan), `ppds plugins deploy --dry-run`, `ppds plugintraces delete
   --dry-run`, and friends. Only add `--confirm` / `--force` after a human
   has seen the preview.

4. **MCP sessions get pinned.** Launch `ppds-mcp-server` with `--read-only`
   for analysis sessions, and `--allowed-env <url>` (repeatable) when
   switching must be possible. No `--allowed-env` flags means
   `ppds_env_select` is disabled — that is a feature, not a bug.

5. **Never bypass a refusal.** Exit code 9 (Forbidden), exit code 11
   (ConfirmationRequired), `Query.DmlBlocked`, `Safety.ShakedownActive` —
   these are answers, not obstacles. Surface them to the user.

## Reading PPDS output

- **stdout is data, stderr is status.** Pipe-safe by design. Parse stdout;
  show stderr to humans.
- Machine-readable: add `-f json` (`--output-format Json`); CSV is `-f csv`.
- Quiet/verbose: `-q` warnings+errors only; `-v` debug; `--debug` trace.
- Non-zero exits carry a structured JSON error envelope on stderr with an
  `error.code` like `Connection.Throttled`. Exit codes 0–11 and per-code
  agent actions: [references/error-codes.md](references/error-codes.md).

## Common mistakes (do not invent these)

| Wrong | Correct |
|-------|---------|
| `ppds env select <name>` (positional) | `ppds env select --environment <name>` — the flag is required |
| `ppds auth select 1` | `ppds auth select --index 1` |
| `ppds auth login` / `ppds login` | `ppds auth create` (first time) or `ppds auth select` (existing) |
| `ppds env switch` | `ppds env select --environment <name>` |
| `--format json` / `--json` | `-f json` / `--output-format Json` |
| `pac auth create` patterns (e.g. `--url`) | PPDS is not PAC CLI — check [references/cli-auth.md](references/cli-auth.md) |

## Where to go next

| Need | Skill |
|------|-------|
| SQL / FetchXML queries, DML, explain, history | ppds-query |
| Plugin registration, deployment, trace debugging | ppds-plugins |
| Solutions, import jobs, env vars, connection refs | ppds-solutions-alm |
| Tables, columns, relationships, keys, choices, views, forms | ppds-metadata |
| Bulk data export/import/copy/load/delete | ppds-data |
| Web resources pull/push/publish | ppds-webresources |
| Users, roles, diagnostics | [references/cli-users.md](references/cli-users.md), [references/cli-roles.md](references/cli-roles.md), [references/cli-logs.md](references/cli-logs.md) |
| Anything else (raw Web API escape hatch) | `ppds api request` — prefer a typed command when one exists |
