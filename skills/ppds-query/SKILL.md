---
name: ppds-query
description: Query and modify Microsoft Dataverse data with PPDS — SQL (transpiled to FetchXML) with joins, CTEs, aggregates and window functions, raw FetchXML, guarded DML, execution plans, TDS endpoint routing, and query history. Use when the user wants to read, filter, join, aggregate, count, or analyze Dataverse records, run INSERT/UPDATE/DELETE statements, inspect a query plan, convert SQL to FetchXML, or recall a previous query. Read ppds-core first for auth and safety rules.
license: MIT
metadata:
  ppds_cli_version_tested: "1.2.0-rc.6"
  ppds_mcp_version_tested: "1.0.0"
---

# PPDS Query — SQL over Dataverse, with guardrails

`ppds query sql` parses real T-SQL and transpiles it to FetchXML (with
client-side fallback for what FetchXML can't express). You almost never need
to hand-write FetchXML. Exact flags for every command:
[references/cli-query.md](references/cli-query.md). Dialect boundaries —
what is and is not supported:
[references/sql-dialect.md](references/sql-dialect.md).

**Surface routing**: CLI `ppds query sql` ↔ MCP `ppds_query_sql`;
CLI `ppds query fetch` ↔ MCP `ppds_query_fetch`. Prefer the CLI in a
terminal; prefer MCP when the host has no shell or the session should be
protocol-level read-only (`ppds-mcp-server --read-only`). Explain and
history are CLI-only.

## Reading data

```bash
ppds query sql "SELECT TOP 10 name, revenue FROM account WHERE statecode = 0 ORDER BY revenue DESC"
ppds query sql "SELECT a.name, c.fullname FROM account a JOIN contact c ON c.parentcustomerid = a.accountid"
ppds query sql "SELECT ownerid, COUNT(*) AS total FROM account GROUP BY ownerid HAVING COUNT(*) > 10"
ppds query sql --file ./report.sql -f json     # SQL from file, JSON to stdout
```

- Paging: `--top`, `--page`, `--paging-cookie`; `--count` adds total count.
- Big SELECTs: route through the TDS endpoint with `--tds` when the query is
  compatible; on `Query.TdsIncompatible` rerun without `--tds`.
- Cross-environment reads: `SELECT COUNT(*) FROM [prod-org].[account]`
  (bracket syntax, see dialect reference).

## FetchXML fallback

For FetchXML-specific features or verbatim reuse of existing queries:

```bash
ppds query fetch "<fetch top='5'><entity name='account'><attribute name='name'/></entity></fetch>"
ppds query sql "SELECT name FROM account" --show-fetchxml   # see the transpilation
```

## DML — the safety contract

INSERT / UPDATE / DELETE work through the same command and are guarded by
the engine (details in [references/sql-dialect.md](references/sql-dialect.md)):
WHERE-less UPDATE/DELETE are blocked, >10,000 affected rows fail without
`--no-limit`, and Production/Unknown environments force confirmation.

The agent loop for any DML:

```bash
ppds env who                                   # 1. name the target environment
ppds query sql "UPDATE contact SET jobtitle = 'Senior Developer' WHERE jobtitle = 'Developer'" --dry-run   # 2. preview plan + row estimate
# 3. show the user the preview and the environment; get approval
ppds query sql "UPDATE contact SET jobtitle = 'Senior Developer' WHERE jobtitle = 'Developer'" --confirm   # 4. execute
```

Exit code 11 means a confirmation prompt fired non-interactively — that is
your cue for step 3, never a cue to retry with bypass flags. `TRUNCATE` is
not SQL here; full-table clears route to `ppds data truncate` (ppds-data
skill).

## Explain, history, debugging

```bash
ppds query explain "SELECT name FROM account WHERE revenue > 1000000"  # plan without executing
ppds query sql "<sql>" --explain          # same, inline
ppds query history list                   # recall past queries
ppds query history execute <id>           # rerun one
```

Use `--show-fetchxml` when a query behaves unexpectedly — the transpiled
FetchXML is the ground truth of what Dataverse was asked.

## Common mistakes (do not invent these)

| Wrong | Correct |
|-------|---------|
| `LIMIT 10` | `SELECT TOP 10 ...` or `--top 10` |
| `--limit 10` / `--max-rows 10` | `--top 10` (alias `-t`) |
| `ppds query sql --fetchxml "<fetch>...""` | `ppds query fetch "<fetch>..."` |
| `ppds sql "..."` | `ppds query sql "..."` |
| `--format json` | `-f json` / `--output-format Json` |
| `BEGIN TRAN ... COMMIT` | not supported — statements run independently |
| `--force` on `query sql` | the DML flags are `--confirm`, `--dry-run`, `--no-limit` |

## Skill boundaries

| Need | Use instead |
|------|-------------|
| Bulk export/import/copy between environments, CSV load, truncate | ppds-data |
| Entity/attribute structure (what columns exist, types, option sets) | ppds-metadata (`ppds metadata attributes <entity>`) or MCP `ppds_data_schema` |
| Why a plugin fired / failed during my DML | ppds-plugins (trace recipe) |
| Auth, environment selection, error-code meanings | ppds-core |
