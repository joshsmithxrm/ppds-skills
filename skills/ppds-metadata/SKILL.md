---
name: ppds-metadata
description: Browse and author Dataverse schema with PPDS — list entities/tables, inspect attributes/columns and relationships, create or update tables, columns, relationships, alternate keys, and global choices/option sets, compare schemas across environments, and adjust views and forms. Use when the user wants to know what columns or relationships an entity has, create or modify a table or column, manage option sets or keys, diff schema between environments, or edit a view or form definition. Read ppds-core first for auth and safety rules.
license: MIT
metadata:
  ppds_cli_version_tested: "1.2.0-rc.6"
  ppds_mcp_version_tested: "1.0.0"
---

# PPDS Metadata — schema as a first-class surface

Exact flags: [references/cli-metadata.md](references/cli-metadata.md),
[references/cli-schema.md](references/cli-schema.md),
[references/cli-views.md](references/cli-views.md),
[references/cli-forms.md](references/cli-forms.md).

**Surface routing**: browsing is CLI or MCP; **schema authoring is one of
the few places MCP is unusually strong** — the released server ships typed
authoring tools (`ppds_metadata_create_table`, `ppds_metadata_add_column`,
`ppds_metadata_update_column`, `ppds_metadata_create_relationship`,
`ppds_metadata_create_choice`, `ppds_metadata_create_key`,
`ppds_metadata_add_option_value`, and update variants). In a terminal the
CLI equivalents live under the `ppds metadata` subgroups: entity, attribute,
relationship, key, optionset.

## Browsing schema

```bash
ppds metadata entities -f json                  # all tables
ppds metadata entity account                    # full metadata for one table
ppds metadata attributes account                # columns, types
ppds metadata relationships account             # 1:N, N:1, N:N
ppds metadata keys account                      # alternate keys
ppds metadata optionsets                        # global choices
ppds metadata optionset <name>
```

MCP equivalents: `ppds_metadata_entities`, `ppds_metadata_entity`,
`ppds_data_schema` (per-entity field list with option values).

## Authoring schema (mutations — safety model applies)

The authoring verbs hang off the noun subgroups; see
[references/cli-metadata.md](references/cli-metadata.md) for each
subcommand's exact flags before generating a command — column/table creation
has many typed options.

```bash
ppds metadata entity create --help        # check real flags first
ppds metadata attribute create --help
ppds metadata relationship create --help
ppds metadata key create --help
```

After metadata changes, publish: `ppds metadata publish <names>` (alias for
`ppds publish --type entity`).

Note: the `table`, `column`, and `choice` subgroups are **deprecated
aliases** of entity, attribute, and optionset — prefer the canonical names.

## Cross-environment schema comparison

```bash
ppds schema compare --help                # compare environments / data packages
```

Use this before solution import to spot drift between source and target.

## Views and forms (maker-portal gap fillers)

Saved queries (views) and system forms are editable from the CLI — column
layout, sort, filter, raw FetchXML on views; tabs/sections/fields on forms.
These write **systemquery/systemform** records: unmanaged-layer mutations,
so confirm the environment first, and managed components will refuse edits
(`View.ManagedComponentNotEditable`).

```bash
ppds views list --entity account
ppds views set-filter --entity account --view "Active Accounts" --filter-file ./filter.xml
ppds forms list --entity account
```

## Common mistakes (do not invent these)

| Wrong | Correct |
|-------|---------|
| `ppds metadata list-entities` | `ppds metadata entities` |
| `ppds metadata entity account --attributes` | `ppds metadata attributes account` |
| `ppds metadata create-table` | `ppds metadata entity create ...` (check `--help` for flags) |
| Editing managed views/forms | edit in the unmanaged source environment instead |
| Forgetting publish | metadata edits need `ppds metadata publish <names>` (or `ppds publish`) to take effect in apps |

## Skill boundaries

| Need | Use instead |
|------|-------------|
| The data inside the tables | ppds-query (reads/DML), ppds-data (bulk) |
| Ship schema changes to another environment | ppds-solutions-alm |
| Web resource files referenced by forms | ppds-webresources |
| Auth, environment selection, error codes | ppds-core |
