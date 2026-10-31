# View form and app editing

This guidance describes the CLI 1.4.2 maintenance candidate. Check the installed
version and captured provenance before relying on candidate-only fixes. Apply
ppds-core's environment and mutation controls; these examples do not authorize
a write or publication.

## Views and managed layers

Views are `savedquery` records (`savedqueries`), not `systemquery`. Forms are
`systemform` records. Managed views can accept an unmanaged-layer edit when
their managed properties allow it. `View.ManagedComponentNotEditable` reports
a rejected write, not a blanket prohibition on managed components.

Pin the reviewed profile/environment on every command. Replace angle-bracket
values with the intended profile, environment URL, and component IDs.

```text
ppds api request --path /api/data/v9.2/WhoAmI --profile <profile> --environment <environment-url>
ppds views get --entity account --view <view-id> --unpublished --profile <profile> --environment <environment-url>
```

Save the original draft before mutation. In the candidate, adding a direct
column synchronizes its layout cell and FetchXML projection, repairing a
missing projection when needed. Related cells use `alias.attribute`:

```text
ppds views add-column --entity account --view <view-id> --via-relationship parentaccountid --column name --profile <profile> --environment <environment-url>
ppds views update-column --entity account --view <view-id> --column parentaccountid.name --width 220 --profile <profile> --environment <environment-url>
```

Use that qualified identity for updates/removal/reordering; base and related
`name` cells are distinct. Removing a display cell preserves query projections
that filters or other query logic may use.

## Raw view creation

There is no typed `views create`. For a user-authorized raw creation, provide
both XML documents. This account payload uses its standard ObjectTypeCode 1;
resolve the actual table code for other tables. Save as `view.json` and review
the payload before POSTing to `/api/data/v9.2/savedqueries`.

```json
{
  "name": "Account telephone review",
  "returnedtypecode": "account",
  "querytype": 0,
  "fetchxml": "<fetch><entity name='account'><attribute name='accountid'/><attribute name='name'/><attribute name='telephone1'/></entity></fetch>",
  "layoutxml": "<grid name='resultset' object='1' jump='name' select='1' preview='1' icon='1'><row name='result' id='accountid'><cell name='name' width='240'/><cell name='telephone1' width='180'/></row></grid>"
}
```

```text
ppds api request --method POST --path /api/data/v9.2/savedqueries --body-file view.json --include --profile <profile> --environment <environment-url>
```

Read the created view ID from the `OData-EntityId` response header exposed
by `--include`. A cell without its FetchXML projection can render empty.

## Draft verification and publication

The candidate verifies every written view XML field against intended normalized
draft state, including equivalent no-ops. Formatting and the platform-maintained
root annotation can differ; query attributes, aliases, filters and order matter.
`View.UpdateNotPersisted` means different XML or a missing read-back record;
`View.VerificationFailed` means read-back was unavailable. Either can follow an
applied write. Inspect the unpublished draft before retrying or publishing.

After review and authorization, publish only the intended table:

```text
ppds publish --type entity account --profile <profile> --environment <environment-url>
```

View mutations' `--publish` performs the same table-scoped publish. Read-back
cannot prevent a later concurrent edit. Verify the saved query's returned
values after publication; ordinary reads show published state unless requested
with `--unpublished`.

## App selections and Timeline forms

The candidate resolves the entire requested app form/view/chart set before
writing; ambiguous names require a returned candidate ID. It retains existing
selections and adds before removing. A later server failure can leave partial
state: inspect the app draft before retry/publish. `--all` removes explicit
selections, not the underlying records. Empty explicit sets can broaden access
to components. Use stable sitemap IDs across languages; translations survive.
Publish only the specific app when its changes are ready.

The Timeline fix accepts `UClientActivitiesConfigurationJSON` on standard
Timeline controls, preserving it in direct XML and unrelated structured edits.
Known parameter types and form structure remain validated; arbitrary unknown
parameters are not guaranteed. Save and inspect unpublished form XML before
publication. A targeted live Timeline round-trip is not established by local
schema tests.

Source: [metadata editing guide](https://github.com/joshsmithxrm/power-platform-developer-suite/blob/main/docs/METADATA-EDITING.md),
[Timeline fix](https://github.com/joshsmithxrm/power-platform-developer-suite/pull/1468).
