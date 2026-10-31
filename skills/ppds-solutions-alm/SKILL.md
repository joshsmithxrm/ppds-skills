---
name: ppds-solutions-alm
description: Dataverse solution ALM with PPDS — export/import solutions, watch import jobs, inspect components, manage environment variables and connection references, activate deployed solution cloud flows, and generate/sync/validate deployment settings. Use when the user wants to move customizations, diagnose import failures or orphaned references, configure target environments, enable or disable solution flows, or prepare deployment settings. Read ppds-core first for auth and safety rules.
license: MIT
metadata:
  ppds_cli_version_tested: "1.4.3-alpha.0.8"
  ppds_mcp_version_tested: "1.2.3-alpha.0.8"
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

## Enable or disable deployed flows

Use `ppds flows enable` / `ppds flows disable` for exact single-flow selection
or a capped `--all --solution` batch. Read
[flow activation](references/flow-activation.md) and
[captured flags](references/cli-flows.md). Preview first, inspect reference
blockers, and retain the expected plan hash and explicit target acknowledgement.
Already matching is `unchanged`; preserve partial/unknown outcomes and inspect
before retrying. PPDS does not auto-run activation after import; inspect imported state. No MCP mutation tool
is added for this workflow.

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
