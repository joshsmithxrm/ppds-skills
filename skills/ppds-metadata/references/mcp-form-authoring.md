# MCP form authoring: bounded draft edit and explicit publication

This workflow targets the captured Safe multi-environment workflows candidate. Check the capture provenance and installed server before using it; a source capture is not published-package evidence.

Use `ppds_forms_list` with `entityLogicalName`, then `ppds_forms_get` with `formId` and `unpublished: true`. Verify the returned environment URL, Main-form type, stable section ID and draft fingerprint. Use the unpublished fingerprint as `expectedDraftHash`.

`ppds_forms_add_field` accepts `entityLogicalName`, `formId`, `sectionId`, `fieldLogicalName`, `expectedDraftHash`, optional `solutionUniqueName`, `dryRun` and `confirmEnvironment`. Add only an existing column to an existing section. Preview with `dryRun: true`, review the target/change, then save with a fresh fingerprint and any required target acknowledgement. No raw XML, new tab/section, destructive layout, or non-Main-form authoring tool is exposed.

The save is unpublished. Inspect `draftWrite`, `solutionAssociation` and `draftVerification` independently. A later failure does not undo an earlier write. Inspect a failed/unknown result before retrying; never infer that failure means zero changes. `concurrencyMode: preflight-only` cannot prevent an external concurrent editor, so avoid simultaneous edits and re-read a stale draft.

Managed-customizable forms can accept an unmanaged-layer edit; locked forms reject writes. Preserve unrelated modern control configuration. Fixture coverage is not proof that every tenant layout has been live-tested.

To publish, re-read/review the draft and call `ppds_forms_publish` with `entityLogicalName`, `formId`, `expectedDraftHash` and `confirmPublishEntity` equal to the table logical name. Use `confirmEnvironment` where required. **This publishes every pending customization for that table**, including changes beyond this form. Get authorization for that scope; permission to save a draft is not permission to publish the table. Inspect `entityPublication` and `publishedVerification`; only the selected form is verified. There is no rollback.

The environment guard applies to these form paths and the existing CLI form writers. CLI form writes accept `--confirm-env`; an MCP allowed environment permits selection but does not acknowledge mutation. Read-only sessions can inspect/preview, never write. See ppds-core's [candidate safety notes](../../ppds-core/references/safe-workflows.md).
