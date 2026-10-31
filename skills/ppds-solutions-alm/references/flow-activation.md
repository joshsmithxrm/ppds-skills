# Activate deployed solution cloud flows

Use the CLI for this candidate capability. No MCP/Extension flow mutation surface is added. Exact captured options: [cli-flows.md](cli-flows.md).

After deployment, inspect connection references with `ppds connectionreferences analyze`. Preview `ppds flows enable` or `ppds flows disable` with `--dry-run`. Choose exactly one selector: `--id`, exact unique/schema `--name`, or `--all`. Batch `--all` requires `--solution`; a solution on a single-flow command is a membership constraint. Never use a display-name guess when IDs disambiguate.

Only solution-aware modern cloud-flow definitions are eligible. Classic workflows, desktop flows, templates and activation records are reported as excluded. The default eligible-flow cap is 100; `--max-flows` can raise it explicitly after reviewing actual counts. The planner never silently truncates.

For enable, missing/inactive/unbound/unreadable references block the whole batch before writes. References can live outside the selected solution. A binding does not verify credentials, permissions, licensing, DLP, child-flow prerequisites or runtime connector health. Resolve bindings through the existing workflow; activation never binds implicitly. Disable does not require healthy bindings.

Review the target and complete plan, then pass the fresh `planHash` as `--expected-plan-hash` and the exact target URL as `--confirm-env` where required. A mismatch blocks before writes. Without the expected hash, dry run is informational and does not reserve a selection. Do not reinterpret an allowlist or selected environment as write acknowledgement.

Execution freezes IDs, processes sequentially, rechecks preconditions and verifies state. Already matching is successful `unchanged`. `--timeout` is the per-flow verification deadline (default 60 seconds). Known blockers make zero writes; runtime failure, cancellation or uncertainty stops remaining writes.

Preserve the full JSON result: counts, exclusions, `succeeded`, `unchanged`, `blocked`, `failed`, `unknown`, `cancelled`, and `not-attempted` entries. Dry run uses `would-change`. A timeout after submission is unknown, not evidence the change failed. Inspect before retrying; never blindly resubmit, automatically roll back, or claim all flows succeeded when entries were excluded. Disabling does not cancel already-running instances. Flow state changes never occur automatically during solution import.
