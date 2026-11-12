# Add, reorder and move form fields

This guide describes approved candidate behavior. Final source, generated help,
validation and public availability must be pinned before distribution. Inspect
the installed CLI's help when its version differs.

Start with the intended profile, exact environment URL, table and customizable
Main form. Save the unpublished XML and identify sections by stable ID when
labels or names are ambiguous. Each write and protected no-op still checks the
resolved target; use `--confirm-env` when required. A read-only session cannot
authorize a mutation by presenting it as an unchanged request.

## Add a placement

`forms add-field` adds genuinely absent fields to the selected section. Repeat
`--field` for a batch. Metadata lookup ignores input casing; new controls use
the canonical logical name and display label, with a logical-name fallback
when the metadata label is empty.

Repeating a field already in that section preserves the existing control,
IDs, custom labels and settings. A batch reports added fields, already-present
fields and duplicate input separately. An all-existing request skips the XML
update. A deliberate placement in another section remains allowed; this is
not a ban on displaying a field in more than one section.

## Reorder existing placements

Use `forms reorder-fields-strict` with every existing selected-section field
exactly once:

```text
ppds forms reorder-fields-strict --entity account --form <form-id> --section <section-id> --fields name,telephone1 --profile <profile> --environment <environment-url> --confirm-env <environment-url>
```

Strict reorder neither creates nor removes fields. It permutes existing bound
cell slots while retaining row attributes, non-field positions, subgrids,
Timeline settings, IDs, labels and nested control content. Missing, extra,
repeated or ambiguous bindings fail before writing. A changed field with a
non-unit row/column span needs an explicit layout edit instead of flattening.
An already-satisfied permutation skips the XML update.

## Move a placement

Use `forms move-field` to relocate an existing control rather than recreating
one in another section:

```text
ppds forms move-field --entity account --form <form-id> --field telephone1 --from-section <source-section-id> --to-section <target-section-id> --before-field name --profile <profile> --environment <environment-url> --confirm-env <environment-url>
```

A cross-section move appends by default. `--before-field` inserts before one
different, uniquely identified target field in its own row. A standalone source
row moves with its attributes. A cell leaving a mixed row keeps the source
row's attributes and sibling cells intact and receives a new plain target row.
The complete moved cell, custom label, control IDs and nested content survive.
Unrelated sections, subgrids and non-field cells are retained. Empty source
row containers are valid; a rowless target gains its own rows element.

Ambiguous sections or controls, a source-present field already in the target,
unsafe spanning fields and bound subgrid movement are rejected without an XML
update. A same-section move without a position is a no-op. If a retry finds no
source control and exactly one target control, it can complete the requested
target placement after all guards; it does not prove which earlier request
created that state. Inspect the draft after a timeout or uncertain submission.

## Migrate legacy reorder

`forms reorder-fields` remains available during transition. Its list is
authoritative: it can add genuinely new fields and remove unlisted bound
fields, and it retains its historical row-flattening behavior. New cells use
metadata labels; existing custom labels are retained. Repeated arguments,
ambiguous selected bindings and silent copying from other sections now fail.

The deprecation warning goes to stderr only; the existing JSON data shape stays
`section`, `fields`, `message`. Migrate to strict reorder, explicit add or move
according to the intended action. Removal is planned for CLI 2.0 and no earlier
than 90 days after the replacement commands' stable release. Both conditions
apply; no calendar removal date has been set.

## Review publication separately

The layout is validated before at most one final XML update. Cancellation and
customization protection also apply to no-ops. Explicit `--solution` and
`--publish` requests keep their separate effects even when XML is unchanged;
do not interpret an XML no-op as zero overall writes. Publication applies to
all pending customizations for the table, not just this form.

The bounded MCP form tools still cover inspecting, adding an existing column
to an existing section and separate table publication. These CLI commands do
not introduce MCP move/reorder tools or new form-designer controls.
