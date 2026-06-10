---
name: ppds-solutions-alm
description: Dataverse solution ALM with PPDS — export/import solutions, watch import jobs, inspect components, manage environment variables and connection references, and generate/sync/validate deployment settings files for target environments. Use when the user wants to export or import a solution, move customizations between environments, check why a solution import failed, fix orphaned connection references, set environment variables, or prepare deployment settings for a pipeline. Read ppds-core first for auth and safety rules.
license: MIT
metadata:
  ppds_cli_version_tested: "1.2.0-rc.4"
  ppds_mcp_version_tested: "1.0.0"
---

# PPDS Solutions ALM — move customizations, keep the receipts

Exact flags: [references/cli-solutions.md](references/cli-solutions.md),
[references/cli-importjobs.md](references/cli-importjobs.md),
[references/cli-environmentvariables.md](references/cli-environmentvariables.md),
[references/cli-connectionreferences.md](references/cli-connectionreferences.md),
[references/cli-deployment-settings.md](references/cli-deployment-settings.md),
[references/cli-connections.md](references/cli-connections.md),
[references/cli-publish.md](references/cli-publish.md).

**Surface routing**: mutations (export/import/publish/set) are CLI-first.
MCP read tools for shell-less hosts: `ppds_solutions_list`,
`ppds_solutions_components`, `ppds_import_jobs_list`, `ppds_import_jobs_get`,
`ppds_environment_variables_list/get/set`,
`ppds_connection_references_list/get/analyze`.

## Solution round-trip

```bash
ppds solutions list -f json
ppds solutions get MySolution
ppds solutions components MySolution            # what's inside
ppds solutions export MySolution --managed -o ./out/MySolution_managed.zip
ppds solutions import ./out/MySolution_managed.zip --environment <target-url>
ppds importjobs wait <job-id> --timeout 30      # poll to completion
ppds solutions publish                          # publish-all after unmanaged changes
ppds solutions url MySolution                   # Maker portal deep link
```

- Import is a **mutation against the target** — safety model rules apply:
  state the target URL, get confirmation (especially Production), then run.
- `export` defaults unmanaged; `--managed` for the deployable artifact.
  `--allow-outside-workspace` is required to write outside the working dir.
- Import failed? `ppds importjobs list`, then `ppds importjobs get <id>`
  (and `ppds importjobs data <id>` for the raw result XML).

## Target-environment configuration

```bash
# Environment variables (the supported way to vary config per environment)
ppds environmentvariables list -f json
ppds environmentvariables set <schema-name> "<value>"

# Connection references — find ones with no connection bound (import breaker)
ppds connectionreferences list --unbound
ppds connectionreferences analyze               # flow ↔ connection-reference map
ppds connections list                           # available connections to bind

# Deployment settings files (for pac/pipeline-style deployments)
ppds deployment-settings generate --solution MySolution --output ./deploy/dev.json
ppds deployment-settings sync --solution MySolution --file ./deploy/dev.json
ppds deployment-settings validate --solution MySolution --file ./deploy/dev.json
```

## Common mistakes (do not invent these)

| Wrong | Correct |
|-------|---------|
| `ppds solutions export --name MySolution` | positional: `ppds solutions export MySolution` |
| `ppds solutions import --path file.zip` | positional: `ppds solutions import file.zip` |
| `ppds solutions import --async --max-async-wait-time` (pac style) | import returns a job; `ppds importjobs wait <id>` does the waiting |
| `ppds env-vars` / `ppds envvars` | the group is `ppds environmentvariables` |
| `ppds connectionreferences update --connection <id>` | binding connections is not a CLI write today — `analyze`/`list` diagnose; bind in the Maker portal |
| `ppds solutions checker` / `clone` / `pack` | not in this CLI — use `pac` for those; PPDS covers list/get/export/import/components/publish/url |

## Skill boundaries

| Need | Use instead |
|------|-------------|
| Reference data / records that ship with the solution | ppds-data |
| Plugin assemblies inside the solution | ppds-plugins |
| Entity/column changes before export | ppds-metadata |
| Web resources inside the solution | ppds-webresources |
| Auth, environment selection, error codes | ppds-core |
