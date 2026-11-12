# Migrate CLI aliases and form layout commands

This guide describes the unpublished candidate's implemented contracts. Final
source and generated help must be bound before distribution. Check your
installed version's help before applying this guidance to an older release.

## Environment aliases

This minor release keeps every existing meaning of `-e`. Use `--entity`,
`--entities` and `--environment` for clear scripts. Every existing environment
option also accepts `-env`; there is no opt-in mode, and commands that did not
accept `-e` do not gain it.

An actual parsed entity/entity-list `-e` emits one fixed deprecation notice on
stderr. Environment `-e`, argument values and unknown options do not emit that
notice. The warning contains no option values and leaves stdout JSON intact.

CLI 2.0 may standardize `-e` for environments only after at least 90 days from
the first stable release containing the complete replacement aliases and
deprecation guidance. Both requirements apply; no calendar date is set.

## Form operations

Use `forms add-field` to add a placement, `forms reorder-fields-strict` to
permute all existing selected-section fields, and `forms move-field` to move
an existing unique control. Legacy `forms reorder-fields` retains its
authoritative add/drop behavior during transition and warns on stderr only.
Its removal requires CLI 2.0 and at least 90 days after the replacement
commands' stable release. Read the form-layout guide for preservation,
ambiguity and no-op rules.

## Version-selected plugin cleanup

The registration file version determines cleanup authority; there is no new
cleanup-mode switch.

| Registration version | Invocation | Cleanup authority |
|---|---|---|
| Missing or 1.0 | Ordinary deploy | No independent image pruning |
| 1.0 | Deploy with clean | Legacy orphan-step cleanup |
| 1.0 | Standalone clean | Legacy orphan-step and empty-type cleanup |
| 2.0 | Ordinary deploy | Nonsecret reconciliation; no independent deletion |
| 2.0 | Deploy with clean or standalone clean | The same image-only plan on configured, uniquely owned steps; retain parent registrations |

Version 2 cleanup requires a complete, explicit `images` list on every
configured step. `images: []` authorizes an empty desired set. Omission is not
permission to clear images; omitted or duplicate/case-variant list properties
fail validation. Review the dry-run's exact image and parent IDs first.

Ownership, identity, protection and inventory ambiguity fail visibly. Only
planned image IDs can be deleted after fresh checks. A concurrent change after
the final read remains possible; the operation is not an atomic conditional
delete. Cancellation or failure stops later calls and retains acknowledged or
unknown effects. Inspect those outcomes before retrying; no rollback is promised.

Generated references still describe the earlier captured candidate. Final help
recapture is required before distributing these newly implemented contracts.
