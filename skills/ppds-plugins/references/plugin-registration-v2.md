# Registration versions and diff outcomes

Use this with the exact tested-version frontmatter and candidate provenance.
These are approved candidate contracts; public distribution remains held.

- Missing/version 1.0 preserves legacy optional fields. Version 2.0 opts into
  supported nonsecret desired fields and PPDS defaults. Unknown versions fail
  before connection. Extract with `--registration-version 2.0` only after
  reviewing those defaults; absence retains an existing file version or 1.0.
- Review cleared filtering and all-attribute images for workload changes.
  Optional omission and explicit Update empty-string clears remain distinct.
- Diff exits are 0 for completed/equal, 1 for completed/drift and 2 for incomplete.
  Retain `data[]` and inspect status/coverage. Assembly/package bytes, solution
  membership and Custom APIs remain outside this step/image comparison.
- Secure input stays write-only. Supplying it does not establish equality;
  comparison/extraction output provides no secret value or hash.
- Cleanup authority follows the registration version; review the image-only
  rules below before generating a cleanup command.
- Keep the three existing update-step flags in generated references:
  `--can-be-bypassed`, `--can-use-readonly`, `--invocation-source`. Daemon/UI
  additions do not create MCP tools or establish identical DTO coverage.

Bind the core `schemas/plugin-registration.schema.json` URL to the actual final
source after it is selected. Schema validation does not prove live permission
or feasibility. Regenerate CLI flags; do not edit captured fences by hand.

## Review cleanup authority

The registration file version selects cleanup behavior. Version 1.0 preserves
legacy `plugins deploy --clean` orphan-step cleanup and `plugins clean`
orphan-step/empty-type cleanup. Version 2.0 uses the same image-only planner
for both commands; ordinary version-2 deploy does not independently delete.
Version-2 cleanup retains steps, types, assemblies and packages.

Every configured version-2 step must contain a complete explicit `images`
list. `images: []` permits clearing that step's owned images; omission or
duplicate/case-variant list properties fail validation before writes. The
whole requested scope is planned before mutation. Package ownership requires
validated package identity and the selected package/assembly chain, not names
or solution membership alone. Dry-run reports exact image and parent IDs.

Fresh ownership and protection checks precede each planned image deletion.
Unknown, hidden, managed, noncustomizable or ambiguous targets fail visibly;
new unplanned images remain. These checks are not an atomic conditional delete.
Inspect acknowledged and dispatched-unknown effects after failure or
cancellation. Later calls stop; no automatic rollback or whole-environment
equality is promised. Live persisted deploy-to-diff acceptance remains a
separate gate from mock/command validation.
