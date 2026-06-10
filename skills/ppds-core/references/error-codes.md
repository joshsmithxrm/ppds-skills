# PPDS error interpretation — exit codes and error codes

Source of truth: PPDS CLI 1.2.0-rc.4 (`ExitCodes.cs`, `ErrorCodes.cs` in the
public repository). Errors are emitted to **stderr** as a structured JSON
envelope; **stdout carries only data**:

```json
{
  "version": "1.0",
  "success": false,
  "error": {
    "code": "Auth.ProfileNotFound",
    "message": "Profile 'production' not found.",
    "target": "production"
  },
  "timestamp": "2026-01-03T12:00:00Z"
}
```

## Process exit codes

| Exit code | Meaning | What an agent should do |
|-----------|---------|------------------------|
| 0 | Success | Continue. |
| 1 | Partial success — some records failed, operation completed | Inspect per-record failures on stderr/output; report the "X of Y" counts to the user; do not silently retry the whole batch. |
| 2 | Failure — operation could not complete | Read the stderr error envelope; act on the `error.code` per the table below. |
| 3 | Invalid arguments | Re-check flags against this skill's `references/cli-*.md` tables — a flag was probably hallucinated or mistyped. |
| 4 | Connection error | Verify environment URL (`ppds env who`); check network; retry once. |
| 5 | Authentication failed | Run `ppds auth who`; re-authenticate (`ppds auth create` / `ppds auth select`); for service principals check secret/cert expiry. |
| 6 | Not found (profile, environment, file) | Verify the name with the matching `list` command before retrying. |
| 7 | Mapping required — auto-mapping incomplete | Data import path: generate a mapping (`--generate-mapping`) or pass `--force` knowingly. |
| 8 | Validation error — incomplete mapping/schema mismatch | Fix the input file/schema; do not force past it blindly. |
| 9 | Forbidden — action not allowed (e.g. deleting a managed component) | Stop. Explain to the user why the platform refuses; do not look for bypasses. |
| 10 | Precondition failed — blocked by current state (e.g. has children) | Resolve the dependency first (the message names it). |
| 11 | Confirmation required — interactive prompt needed but stdin redirected | A safety prompt fired in a non-interactive context. Surface the pending action to the human; only rerun with the documented confirm/force flag after explicit approval. |

## Error codes by category (`error.code` on stderr)

Codes are `Category.Name` strings. The most actionable ones:

### Auth / Profile / Connection

| Code | Meaning / agent action |
|------|------------------------|
| `Profile.NotFound`, `Auth.ProfileNotFound` | Named profile missing — `ppds auth list` to see what exists. |
| `Profile.NoActiveProfile`, `Auth.NoActiveProfile` | No active profile — `ppds auth select --name <n>` or create one. |
| `Auth.Expired` | Token expired — interactive methods may need re-login. |
| `Auth.InvalidCredentials` | Bad secret/cert/password — confirm with the user; never guess credentials. |
| `Auth.InsufficientPermissions` | The identity lacks Dataverse privileges — needs admin action, not a retry. |
| `Auth.CertificateError` | Certificate file missing or invalid. |
| `Connection.Throttled` | Dataverse service-protection 429 — back off and retry later; reduce parallelism; do not hammer. |
| `Connection.Timeout`, `Connection.Failed` | Transient or network — one retry is reasonable. |
| `Connection.EnvironmentNotFound` | Environment name/URL didn't resolve — `ppds env list --filter <text>`. |
| `Connection.AmbiguousEnvironment` | Partial name matched several environments — use the URL or unique name. |

### Query

| Code | Meaning / agent action |
|------|------------------------|
| `Query.ParseError` | SQL didn't parse — check the dialect notes in the ppds-query skill. |
| `Query.DmlBlocked` | Safety guard blocked the DML (e.g. UPDATE/DELETE without WHERE, cross-env policy). Read the message; fix the statement — do not blindly add bypass flags. |
| `Query.DmlConfirmationRequired` | DML needs confirmation — show the human the statement + target environment; rerun with `--confirm` only after approval. |
| `Query.DmlRowCapExceeded` | Would affect more rows than the cap (default 10,000) — confirm intent with the human before `--no-limit`. |
| `Query.AggregateLimitExceeded` | FetchXML 50K aggregate limit hit — the engine usually partitions automatically; simplify or partition the query. |
| `Query.TdsIncompatible` | Query can't run on the TDS endpoint — drop `--tds` and let it transpile to FetchXML. |
| `Query.TdsConnectionFailed` | TDS endpoint unreachable/disabled in the org — fall back to FetchXML path. |
| `Query.SubqueryMultipleRows` | Scalar subquery returned >1 row — fix the SQL. |

### Operations and components

| Code | Meaning / agent action |
|------|------------------------|
| `Operation.PartialFailure` | Batch partially failed — report exact counts; never claim full success. |
| `Operation.InProgress` | Conflicting operation already running — wait, don't double-submit. |
| `Plugin.HasChildren` | Unregistering something with children — remove children first (message lists them). |
| `Solution.ImportFailed` | Check `ppds importjobs list` / `ppds importjobs get` for the job detail. |
| `WebResource.Conflict` | Server copy changed since pull — re-pull, merge, then push. |
| `View.ManagedComponentNotEditable` | Managed component — edits belong in the source (unmanaged) environment. |
| `Safety.ShakedownActive` | A PPDS safety session has mutations locked — do not work around it. |

Full category list also includes: `Validation.*`, `External.*`,
`PluginTrace.*`, `UpdateCheck.*`, `ServiceEndpoint.*`, `CustomApi.*`,
`DataProvider.*`, `DataSource.*`, `MetadataAuthoring.*`, `View.*`,
`WebResource.*`. When you hit an unfamiliar code, trust the `message` field —
it is written to be actionable — and report it verbatim to the user.
