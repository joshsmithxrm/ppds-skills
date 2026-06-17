---
name: ppds-data
description: Bulk Dataverse data operations with PPDS — schema-driven export/import (CMT-compatible), direct environment-to-environment copy, CSV load, bulk update/delete, truncate, user mapping, and dependency analysis. Use when the user wants to move records between environments, seed reference data, export data to a ZIP, load a CSV into a table, bulk-delete records, or migrate data with lookup and owner remapping. Read ppds-core first for auth and safety rules.
license: MIT
metadata:
  ppds_cli_version_tested: "1.2.0-rc.6"
  ppds_mcp_version_tested: "1.0.0"
---

# PPDS Data — bulk movement with a schema, not a script

Exact flags for every command (export/import/copy/analyze/schema/users/load/
update/delete/truncate): [references/cli-data.md](references/cli-data.md).

**Surface routing**: bulk data movement is **CLI-only** (long-running,
progress-reporting operations). MCP offers read-side analysis only:
`ppds_data_analyze` (record counts, samples), `ppds_data_schema` (entity
schema). For ad-hoc row DML prefer SQL via ppds-query.

## The migration loop

```bash
# 1. Generate a migration schema (which entities + columns travel)
ppds data schema --entities account,contact --output ./schema.xml

# 2. Understand dependency order / lookups before moving anything
ppds data analyze --schema ./schema.xml

# 3. Export from source
ppds data export --schema ./schema.xml --output ./data.zip

# 4. Map users source → target (service accounts, departed users)
ppds data users --source-env <source-url> --target-env <target-url> --output ./usermap.xml

# 5. Import to target — STOP: confirm target env with the user first
ppds data import --data ./data.zip --user-mapping ./usermap.xml --mode Upsert
```

Or skip the ZIP for direct transfer: `ppds data copy` (source → target in
one step; same schema-driven model — see reference for flags).

Import facts worth knowing (all real flags, see reference):

- `--mode Create|Update|Upsert|Skip` (default Upsert).
- `--bypass-plugins <sync|async|all>` (needs `prvBypassCustomBusinessLogic`)
  and `--bypass-flows` — for clean reference-data loads; leave off otherwise.
- `--resolve-lookups` + `--skip-unresolved-lookups`, `--skip-missing-columns`,
  `--strip-owner-fields`, `--impersonate-owners` (needs `--user-mapping`).
- `--continue-on-error` + `--error-report <path>` stream per-record failures
  to `.errors.jsonl` — exit code 1 means partial success; report "X of Y".
- Export format: `--format Cmt` (default, CMT-compatible) or `Json`.
- Throughput: multiple app-user profiles multiply API quota
  (`-p app1,app2,app3`); `--parallel`, `--batch-size`, `--page-parallel`.

## Targeted bulk operations

`load` / `update` / `delete` / `truncate` are single-entity and filter- or
file-driven — distinct from the schema-driven export/import loop above. Each
previews with `--dry-run`; `update` / `delete` / `truncate` take `--force` to
run non-interactively, only after the user has seen the preview.

```bash
# CSV → table; upsert on an alternate key so re-runs don't duplicate rows
ppds data load --file products.csv --entity new_product --key new_productcode --dry-run
#   --generate-mapping / --mapping for column maps; without --key it creates every row.

# Bulk field change by filter (deactivate = set statecode) — the direct route
ppds data update --entity account --filter "statecode eq 0" --set "statecode=1" --dry-run

# Bulk delete by filter (preview the matched rows first)
ppds data delete --entity task --filter "statecode eq 1" --dry-run

# Wipe an ENTIRE table — DANGEROUS, no undo
ppds data truncate --entity new_stagingrow --dry-run
```

For a criteria-based bulk field change, `ppds data update --filter --set` is
the direct route — don't reach for `ppds query sql "UPDATE ..."` unless you
specifically want the SQL/FetchXML DML path (see ppds-query). `truncate` is
the command behind "wipe this table" asks — never run it without naming the
entity, the record count (`ppds query sql "SELECT COUNT(*) FROM <entity>"`),
and the environment to the user, then getting explicit confirmation.

## Common mistakes (do not invent these)

| Wrong | Correct |
|-------|---------|
| `ppds data export --entity account` | exports are schema-driven: `--schema schema.xml` (generate with `ppds data schema`) |
| `ppds data import ./data.zip` (positional) | `ppds data import --data ./data.zip` |
| `--dry-run` on `data import` | does not exist — validate with `data analyze` and import into a sandbox first |
| `DELETE FROM x` without WHERE via ppds-query for "clear the table" | `ppds data truncate` (purpose-built) — and confirm with the human |
| CMT (`DataMigrationUtility`) flag names | PPDS flags differ — check [references/cli-data.md](references/cli-data.md) |

## Skill boundaries

| Need | Use instead |
|------|-------------|
| Ad-hoc queries, row-level DML, counts | ppds-query |
| What columns/lookups an entity has | ppds-metadata |
| Moving customizations (not data) | ppds-solutions-alm |
| Auth, environment selection, error codes | ppds-core |
