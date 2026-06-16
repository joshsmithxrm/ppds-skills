# `ppds forms` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds forms`

```text
Description:
  Inspect and modify Dataverse systemform records: list forms, view form structure, and manage tabs, sections, fields, and sub-grids

Usage:
  ppds forms [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list            List systemforms for a Dataverse entity
  get             Get the structure of a specific Dataverse systemform
  set-xml         Write raw form XML to a Dataverse systemform record. Schema validation is applied before writing. All id and labelid attributes must use brace-format GUIDs ({xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}). All id and labelid values must be unique within the document.
  add-tab         Add a tab to a Main form
  update-tab      Update properties of an existing tab on a Main form
  remove-tab      Remove a tab from a Main form
  find-tab        Find a tab in a form by label and return its ID and position
  add-section     Add a section to a tab on a Main form
  update-section  Update properties of an existing section on a Main form
  remove-section  Remove a section from a Main form
  find-section    Find a section in a form by label and return its ID and parent tab
  add-field       Add one or more fields to a section on a Main form. classid is resolved automatically from column metadata - never specify it directly.
  remove-field    Remove a field from a Main form. Without --section, removes all occurrences of the field; with --section, removes only from the specified section.
  reorder-fields  Reorder fields in a section. Provide the authoritative ordered list; fields not in the list are removed.
  add-subgrid     Add a sub-grid control to a section on a Main form
  remove-subgrid  Remove a sub-grid from a Main form by label or name
```

## `ppds forms add-field`

```text
Description:
  Add one or more fields to a section on a Main form. classid is resolved automatically from column metadata - never specify it directly.

Usage:
  ppds forms add-field [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --section <section>                  [Required] Label or name of the section to add the field(s) to
  --field <field>                      Field logical name to add. Repeat for multiple fields.
  --publish                            Publish customizations after writing
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms add-section`

```text
Description:
  Add a section to a tab on a Main form

Usage:
  ppds forms add-section [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --tab <tab>                          [Required] Label or name of the parent tab
  --label <label>                      [Required] Section label
  --show-label                         Show the section label
  --columns <columns>                  Number of columns (1 or 2)
  --visible                            Whether the section is visible
  --available-on-phone                 Whether the section is available on phone
  --publish                            Publish customizations after adding the section
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms add-subgrid`

```text
Description:
  Add a sub-grid control to a section on a Main form

Usage:
  ppds forms add-subgrid [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --section <section>                  [Required] Label or name of the section to add the sub-grid to
  --label <label>                      [Required] Display label for the sub-grid
  --target-entity <target-entity>      [Required] Logical name of the entity displayed in the sub-grid
  --default-view <default-view>        [Required] GUID of the default view (savedqueries record) to display in the sub-grid
  --relationship <relationship>        Relationship schema name used to filter the sub-grid records
  --hide-label                         Whether to hide the sub-grid label
  --hide-on-phone                      Whether to hide the sub-grid on phone
  --max-rows <max-rows>                Maximum number of rows to display in the sub-grid
  --hide-search-box                    Whether to hide the search box in the sub-grid
  --publish                            Publish customizations after writing
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms add-tab`

```text
Description:
  Add a tab to a Main form

Usage:
  ppds forms add-tab [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --label <label>                      [Required] Label for the new tab
  --show-label                         Whether to show the tab label
  --expanded                           Whether the tab is expanded by default
  --visible                            Whether the tab is visible
  --available-on-phone                 Whether the tab is available on phone
  --columns <columns>                  Number of columns in the tab (1, 2, or 3)
  --publish                            Publish customizations after writing
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms find-section`

```text
Description:
  Find a section in a form by label and return its ID and parent tab

Usage:
  ppds forms find-section [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --label <label>                      [Required] Label or name of the section to find
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms find-tab`

```text
Description:
  Find a tab in a form by label and return its ID and position

Usage:
  ppds forms find-tab [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --label <label>                      [Required] Label or name of the tab to find
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms get`

```text
Description:
  Get the structure of a specific Dataverse systemform

Usage:
  ppds forms get [options]

Options:
  --entity <entity>                    [Required] Logical name of the entity
  --form <form>                        [Required] Name or ID of the form
  --unpublished                        Show the unpublished (latest draft) form instead of the published version
  --raw                                Write raw formxml to stdout instead of the structured summary
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms list`

```text
Description:
  List systemforms for a Dataverse entity

Usage:
  ppds forms list [options]

Options:
  --entity <entity>                    [Required] Logical name of the entity
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms remove-field`

```text
Description:
  Remove a field from a Main form. Without --section, removes all occurrences of the field; with --section, removes only from the specified section.

Usage:
  ppds forms remove-field [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --field <field>                      [Required] Field logical name to remove
  --section <section>                  Label or name of the section to remove the field from. If omitted, all occurrences of the field are removed from the form.
  --publish                            Publish customizations after writing
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms remove-section`

```text
Description:
  Remove a section from a Main form

Usage:
  ppds forms remove-section [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --section <section>                  [Required] Label or name of the section to remove
  --publish                            Publish customizations after removing the section
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms remove-subgrid`

```text
Description:
  Remove a sub-grid from a Main form by label or name

Usage:
  ppds forms remove-subgrid [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --label <label>                      [Required] Label or name of the sub-grid to remove
  --publish                            Publish customizations after writing
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms remove-tab`

```text
Description:
  Remove a tab from a Main form

Usage:
  ppds forms remove-tab [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --tab <tab>                          [Required] Label or name of the tab to remove
  --publish                            Publish customizations after writing
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms reorder-fields`

```text
Description:
  Reorder fields in a section. Provide the authoritative ordered list; fields not in the list are removed.

Usage:
  ppds forms reorder-fields [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --section <section>                  [Required] Label or name of the section containing the fields to reorder
  --fields <fields>                    [Required] Comma-separated ordered list of field logical names. Fields not in the list are removed.
  --publish                            Publish customizations after writing
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms set-xml`

```text
Description:
  Write raw form XML to a Dataverse systemform record. Schema validation is applied before writing. All id and labelid attributes must use brace-format GUIDs ({xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}). All id and labelid values must be unique within the document.

Usage:
  ppds forms set-xml [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --xml <xml>                          [Required] Path to the XML file to write. Schema validation is applied before writing. All id and labelid attributes must use brace-format GUIDs ({xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}). All id and labelid values must be unique within the document.
  --publish                            Publish customizations after writing
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms update-section`

```text
Description:
  Update properties of an existing section on a Main form

Usage:
  ppds forms update-section [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --section <section>                  [Required] Current label or name of the section to update
  --label <label>                      New label for the section (renames the section)
  --show-label                         Show the section label
  --columns <columns>                  Number of columns
  --visible                            Whether the section is visible
  --available-on-phone                 Whether the section is available on phone
  --publish                            Publish customizations after updating the section
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds forms update-tab`

```text
Description:
  Update properties of an existing tab on a Main form

Usage:
  ppds forms update-tab [options]

Options:
  --entity <entity>                    [Required] Entity logical name
  --form <form>                        [Required] Name or ID of the form
  --tab <tab>                          [Required] Label or name of the tab to update
  --label <label>                      New label for the tab (renames the tab)
  --show-label                         Whether to show the tab label
  --expanded                           Whether the tab is expanded by default
  --visible                            Whether the tab is visible
  --available-on-phone                 Whether the tab is available on phone
  --columns <columns>                  Number of columns in the tab
  --publish                            Publish customizations after writing
  --solution <solution>                Solution unique name to associate the change with
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

