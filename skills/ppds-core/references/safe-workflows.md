# Safe multi-environment workflows candidate

This branch prepares the next release increment. Generated captures identify the exact source candidate and binaries; they do not prove published packages or live Dataverse behavior. Prefer the installed surface's help/tool schema if it differs.

## Approved release preparation

The approved versions are CLI 1.5.0, MCP 1.3.0, Extension 1.8.0 stable and Skills 0.2.0. Publication is pending. Existing alpha captures retain their original provenance; regenerate and verify the references against the actual stable tools before distributing Skills 0.2.0.

CLI/MCP use an explicitly approved one-release minor-version exception for safety hardening that changes existing behavior. Protected form writers require the environment acknowledgement described below; ambiguous form selectors fail closed; MCP sessions retain captured targets. Update the Extension with its matching daemon. Custom .NET consumers embedding CLI/MCP implementation assemblies must adapt to changed form and web-resource signatures. Do not describe this release as universally backward-compatible or weaken a guard to preserve an older workflow.

## Environment acknowledgement

The shared guard is adopted by form writers and flow enable/disable, not every mutation domain. It binds acknowledgement to actual URL, profile identity, session and current environment policy. Effective Production/Test protection requires acknowledgement; Unknown defaults to Production unless explicitly overridden. Read-only denies actual writes but permits a supported write-free preview. CLI uses `--confirm-env`; MCP forms use `confirmEnvironment`. An allowed environment is a selectable destination, not write approval. Surface mismatches, unavailable policy and unresolved targets; do not change protection to evade a refusal.

Route MCP form draft/verification/publication to ppds-metadata. Route post-deployment flow activation to ppds-solutions-alm. Draft-save authorization does not authorize publication of all pending customizations for a table.

## Notebook environment isolation

For Extension notebook work, **Select Notebook Environment** changes only that notebook. **Use session default** clears its binding without changing global selection. Saved metadata retains only environment ID/name/URL, no credentials/profile identity/acknowledgement. Per-cell targets are not supported.

A queued run captures target and opaque profile identity when it begins. Focus/default/profile/binding changes cannot redirect that active run. Check the output's executed URL and timestamp, not just current notebook metadata. Record links and exports use executed context; Data Explorer transfer preserves it. An old daemon lacking identity support requires restart/update rather than fallback.

On notebook or transferred Data Explorer authentication failure, confirm the captured target and intended profile in **PPDS Profiles**, re-authenticate, and rerun. Do not invalidate a profile using a possibly changed name, index or global selection.

Interrupt cancels only that notebook's active request and queue; cell cancellation does not cancel the next cell. Closing cancels only owned work. Production/Unknown confirmation is scoped to notebook+target+profile+type, not saved, and never grants DML approval.

## Release fix interpretation

- Plugin deployment can report both earlier step errors and a later terminal failure. Keep both when diagnosing; a failed command can leave partial state. Diff cancellation stops further reads and comparisons.
- Web resource creation reports missing/mismatched publisher-prefix warnings in JSON and stderr without renaming. A supplied solution/publisher resolution failure remains an error.
- Managed form fixture and provenance coverage supplements retained view tests; live managed roundtrips remain separate evidence.
- Update-check assertions now use explicit background completion and controlled clocks. This is test reliability work, not a new command.
- Live plugin propagation polling uses `PPDS_TEST_PROPAGATION_TIMEOUT_SECONDS` (default 90, integer 1–900) and reports elapsed time, attempts and last output on timeout. This environment variable controls tests, not normal CLI execution.
- Relevant Python tests now feed required `test-status`; unintended skip, cancellation or failure cannot be treated as success. Hosted check/protection evidence must still match the candidate SHA.
