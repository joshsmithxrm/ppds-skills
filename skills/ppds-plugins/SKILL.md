---
name: ppds-plugins
description: Register, deploy, and debug Dataverse plugins declaratively with PPDS — attribute-driven registration ([PluginStep]/[PluginImage]/[CustomApi]), the extract → diff → deploy loop, assembly management, Custom APIs, service endpoints, and plugin trace log debugging (list/get/timeline). Use when the user wants to register or deploy a plugin assembly, sync plugin steps from code, diagnose a plugin error or performance problem, read plugin trace logs, or manage Custom APIs. Read ppds-core first for auth and safety rules.
license: MIT
metadata:
  ppds_cli_version_tested: "1.2.0"
  ppds_mcp_version_tested: "1.0.0"
---

# PPDS Plugins — registration as code, traces as evidence

PPDS replaces Plugin Registration Tool clicks with attributes on the plugin
class. Registration metadata is **extracted from the compiled assembly**,
reviewed as JSON, diffed against the environment, and deployed
deterministically. Attribute reference (all properties, verified):
[references/plugin-attributes.md](references/plugin-attributes.md). Exact
CLI flags: [references/cli-plugins.md](references/cli-plugins.md).

**Surface routing**: deployment is CLI-only. For read-side analysis from an
MCP-only host: `ppds_plugins_list`, `ppds_plugins_get`,
`ppds_plugin_traces_list`, `ppds_plugin_traces_get`,
`ppds_plugin_traces_timeline`, `ppds_plugin_traces_delete`.

## The declarative loop

```bash
# 0. Code: decorate plugin classes with [PluginStep] / [PluginImage] / [CustomApi]
#    (PPDS.Plugins NuGet package, net462) and build.

# 1. Extract attribute metadata from the assembly to JSON
ppds plugins extract --input bin/Release/net462/MyPlugins.dll --output registrations.json

# 2. Diff against what the environment actually has
ppds plugins diff --config registrations.json

# 3. Preview the deployment (always before the real run — safety model rule 3)
ppds plugins deploy --config registrations.json --dry-run

# 4. Deploy (after the user has seen the preview)
ppds plugins deploy --config registrations.json

# 5. Verify
ppds plugins list --assembly MyPlugins
```

Key facts:

- `deploy` takes `--config registrations.json` (**required**) — it does not
  take an assembly path. `extract` is the step that reads the DLL.
- `deploy --clean` also removes registrations in the environment that are
  missing from the config (orphans). Run `--dry-run` with `--clean` first —
  it deletes.
- `--solution <unique-name>` on extract/deploy adds components to a solution.
- Step-level management: `ppds plugins enable` / `ppds plugins disable` /
  `ppds plugins unregister`, `ppds plugins update` (swap assembly bytes),
  `ppds plugins download`, `ppds plugins clean` (orphan removal),
  `ppds plugins get`.
- Custom APIs declared via `[CustomApi]` deploy in the same loop; manual
  management exists under `ppds custom-apis`
  ([references/cli-custom-apis.md](references/cli-custom-apis.md)) and
  `ppds service-endpoints`
  ([references/cli-service-endpoints.md](references/cli-service-endpoints.md)).

## Trace debugging recipe

Plugin trace logs are the evidence. Filters:
[references/cli-plugintraces.md](references/cli-plugintraces.md).

```bash
# 1. Make sure tracing is on (all = verbose; exception = errors only)
ppds plugintraces settings get
ppds plugintraces settings set all

# 2. Reproduce the failing operation (e.g. the Update that misbehaves)

# 3. Find the trace
ppds plugintraces list --errors-only --last-hour --entity account
ppds plugintraces list --type AccountUpdatePlugin --message Update -n 20

# 4. Read it — message block + exception detail
ppds plugintraces get <trace-id>

# 5. See the whole transaction as a tree (correlation ID — finds chained/
#    nested plugin executions and the slow step)
ppds plugintraces timeline <trace-id>
ppds plugintraces related <trace-id>          # flat list, same correlation

# 6. Restore trace settings when done (all is noisy and costs storage)
ppds plugintraces settings set exception

# Housekeeping (destructive — preview first; durations like 7d, 24h, 30m)
ppds plugintraces delete --older-than 7d --dry-run
```

Useful list filters: `--mode sync|async`, `--min-duration <ms>` (find slow
steps), `--since/--until` (ISO 8601), `--correlation-id`, `--step-id`,
`--record account/<guid>`, `--recursive` (nested depth >1 only).

## Common mistakes (do not invent these)

| Wrong | Correct |
|-------|---------|
| `ppds plugins deploy --assembly My.dll` | `extract --input My.dll` first, then `deploy --config registrations.json` |
| `ppds plugins deploy --file registrations.json` | the flag is `--config` (alias `-c`) |
| `ppds plugins register --assembly ...` for updates | `register` is first-time direct registration; the maintained loop is extract → diff → deploy |
| `ppds plugintraces list --query "..."` / `--filter-xml` | `--filter <json-file>`, or the typed flags (`--entity`, `--message`, `--errors-only`, ...) |
| `ppds traces ...` / `ppds plugin-traces ...` | the group is `ppds plugintraces` |
| Leaving trace level at `all` | `ppds plugintraces settings set exception` after debugging |

## Skill boundaries

| Need | Use instead |
|------|-------------|
| Query the data a plugin wrote (verify behavior) | ppds-query |
| Add the plugin's solution to ALM flow, import/export | ppds-solutions-alm |
| Entity/attribute metadata the plugin depends on | ppds-metadata |
| Auth, environment selection, error-code meanings | ppds-core |
