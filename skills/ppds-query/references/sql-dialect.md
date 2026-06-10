# PPDS SQL dialect — what the SQL→FetchXML engine supports

Source of truth: the public `PPDS.Query` package README (1.2.0-rc line) and
the engine's published feature list. Parsing is full T-SQL via
`Microsoft.SqlServer.TransactSql.ScriptDom`; execution pushes work down to
FetchXML when possible and falls back to client-side operators when not.

## Supported

| Area | Support |
|------|---------|
| SELECT | columns, aliases, `TOP`, `DISTINCT`, computed expressions |
| WHERE | `=`, `<>`, `<`, `>`, `<=`, `>=`, `LIKE`, `IN`, `BETWEEN`, `IS NULL`, `IS NOT DISTINCT FROM` |
| JOIN | `INNER`, `LEFT`, `RIGHT`, `FULL OUTER`, `CROSS`, `OUTER APPLY` |
| GROUP BY | aggregates `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STDEV`, `STDEVP`, `VAR`, `VARP`; `HAVING` |
| ORDER BY | `ASC` / `DESC` |
| Set ops | `UNION`, `UNION ALL` |
| Subqueries | `IN`, `NOT IN`, `EXISTS`, `NOT EXISTS`, derived tables, scalar subqueries |
| Window functions | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `CUME_DIST`, `PERCENT_RANK` |
| CTEs | including recursive CTEs |
| Conditionals | `CASE WHEN`, `IIF` |
| Functions | `ISNULL`, `COALESCE`, `NULLIF`, `CAST`, string functions, `DATEADD`, `DATEDIFF`, `DATEPART`, `YEAR`, `MONTH`, `DAY`, `GETDATE`, `GETUTCDATE`, `TIMEFROMPARTS` |
| JSON | `OPENJSON` table-valued function, `JSON_MODIFY` (array paths) |
| Scripting | `DECLARE`/`SET` variables, `IF`/`ELSE`, `WHILE`/`BREAK`/`CONTINUE`, `SELECT INTO #temp`, `@@ERROR`, `ERROR_MESSAGE()` |
| DML | `INSERT ... VALUES`, `INSERT ... SELECT`, `UPDATE ... WHERE`, `DELETE ... WHERE` — all safety-guarded (see below) |
| Cross-environment | `[env-label].[entity]` bracket syntax; remote FetchXML execution; e.g. `SELECT COUNT(*) FROM [prod-org].[account]` |

## Not supported

| Missing | Use instead |
|---------|-------------|
| `TRUNCATE TABLE` | `ppds data truncate` (dedicated command with its own guards) |
| DDL (`CREATE/ALTER/DROP TABLE`, indexes) | ppds-metadata skill (`ppds metadata entity create` etc.) |
| Transactions (`BEGIN/COMMIT/ROLLBACK`) | not available — statements execute independently |
| `LIMIT n` (MySQL/Postgres syntax) | `TOP n` or the `--top` flag |

## Execution model notes

- **FetchXML pushdown**: filters, joins, and aggregates run server-side when
  expressible in FetchXML; otherwise hash/merge/nested-loop joins run
  client-side over streamed pages (Volcano iterator model).
- **Aggregate 50K limit**: Dataverse caps FetchXML aggregates at 50,000
  records. PPDS works around it with parallel partitioned aggregates
  (date-range partitioning, adaptive binary splitting), so `COUNT(*)` on
  large tables is accurate. If you still hit `Query.AggregateLimitExceeded`,
  narrow the query.
- **TDS endpoint routing**: compatible SELECTs can run directly against the
  Dataverse TDS (SQL) endpoint — opt in per query with `--tds`, or
  per-environment with the `use_tds_endpoint` safety setting. Incompatible
  queries (`Query.TdsIncompatible`) should be rerun without `--tds` to use
  the FetchXML path. TDS is read-only by nature.
- **EXPLAIN**: `ppds query explain "<sql>"` (or `ppds query sql --explain`)
  shows the plan — including the transpiled FetchXML — without executing.

## DML safety (enforced by the engine, not by convention)

- `UPDATE` / `DELETE` **without a WHERE clause are blocked** by default
  (`prevent_update_without_where` / `prevent_delete_without_where`).
- **Row cap**: a DML statement affecting more than 10,000 rows (default)
  fails with `Query.DmlRowCapExceeded`; `--no-limit` removes the cap after
  human approval.
- **Environment protection**: `EnvironmentConfig.Type = Production` (or
  unknown) forces confirmation-with-preview for every DML statement;
  non-interactive runs need `--confirm` (exit code 11 otherwise).
- **Cross-environment DML** defaults to read-only
  (`cross_env_dml_policy: ReadOnly`); `Prompt` and `Allow` exist, but a
  Production target always prompts.
- **Plugin/flow bypass**: per-environment settings `bypass_custom_plugins`
  and `bypass_power_automate_flows` exist for migration scenarios — leave
  them off unless the user explicitly asks.
- Other tunables (per-environment `QuerySafetySettings`): warn thresholds
  per verb, `dml_batch_size` (default 100), `max_parallelism`,
  `use_bulk_delete` (route full-table DELETE to async `BulkDeleteRequest`),
  `query_timeout_seconds` (default 300), `max_page_retrievals` (default 200),
  `datetime_mode` (Utc/Local/EnvironmentTimezone).
