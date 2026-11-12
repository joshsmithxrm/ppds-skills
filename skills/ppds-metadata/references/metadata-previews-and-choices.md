# Review metadata previews and Choice values

This guide describes implemented candidate behavior. Final generated references
and exact artifact provenance remain distribution gates.

## Omit values when requesting allocation

Initial local Choice/Choices columns and global choices distinguish an omitted
numeric value from an explicit zero. In an options JSON file, omission requests
publisher-based allocation; a supplied zero remains zero:

```json
[
  { "label": "Allocate this value" },
  { "label": "Keep explicit zero", "value": 0 }
]
```

For .NET callers, the existing `OptionDefinition.Value` property remains an
`int` with public get/set accessors and a parameterless constructor. Omit the
assignment to request allocation. Setting `Value = 0` deliberately preserves
zero. The additive read-only `HasExplicitValue` getter records presence and is
ignored in JSON. Allocation uses copies and leaves caller-owned options intact.

Global-choice label syntax accepts a bare label or `label=value`, splitting an
explicit definition at its last equals sign. Invalid nonempty definitions fail
rather than disappearing. Use the exact captured command's options-file rules;
a bare label and an explicitly supplied numeric zero have different intent.

Explicit values outside the publisher's numeric range are retained with a
warning. Without numeric publisher-prefix metadata, an explicit-only request
can continue with a range-unavailable warning; omission still fails because it
cannot be allocated. Global-choice MCP output adds `validationMessages`.
Consumers must tolerate the additional warning field. Warnings do not prove
that the server will accept the choice or that values have been persisted.

## Read the scope of a dry-run

Initial omitted-value creation reports provisional allocation after input and
publisher checks. It neither reserves numbers nor proves server feasibility.
Explicit-only requests and requests without allocation report that allocation
was not performed. Other previews report only the checks actually completed.

Table, column, relationship, key and global-choice delete previews resolve the
unpublished target identity and retrieve delete dependencies. Every returned
edge remains visible, including unknown component types or unresolved names.
Blocked previews are non-success; incomplete reads also fail. A clear dependency
observation leaves permissions, customizability, other server constraints and
concurrent changes unchecked. The real delete reads again; force only skips
confirmation and cannot bypass dependencies.

Option-removal previews check target existence, not removability or complete
dependency coverage. Inspect structured preview scope and status rather than
assuming every dry-run checks the same things. JSON diagnostics remain in the
stdout envelope; text diagnostics and alias notices use stderr.

## Update labels without replacing structural metadata

Supported finite State, Status and GUID label updates use the required identity
and requested label fields. Known noneditable attributes are rejected before
mutation. Unknown supported cases remain subject to server authority. This does
not promise arbitrary type changes or universal server acceptance.

After a failed or uncertain write, inspect the target before retrying. The
bounded public metadata error-privacy correction retains error codes and
causes; it does not guarantee that every repository error is normalized.
