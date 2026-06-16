# `ppds views` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds views`

```text
Description:
  Manage Dataverse savedqueries views: list, get, add-column, remove-column, update-column, reorder-columns, set-sort, clear-sort, set-filter, clear-filter, set-fetchxml

Usage:
  ppds views [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list             List all views for an entity
  get              Get detailed view configuration including columns, sort, and filter
  add-column       Add one or more columns to a view
  remove-column    Remove a column from a view by attribute name
  update-column    Update the width of an existing column in a view
  reorder-columns  Set the authoritative column order for a view. Columns not listed are dropped.
  set-sort         Set the sort order for a view. Multiple --sort flags applied in declaration order.
  clear-sort       Remove all sort configuration from a view
  set-filter       Set or replace the filter on a view.
  
                   Use --filter-file to apply a <filter> XML fragment from a file:
                     <filter type="and">
                       <condition attribute="statecode" operator="eq" value="0" />
                     </filter>
  
                   Use --condition for a quick single-condition filter: --condition "statecode:eq:0"
  clear-filter     Remove all filter conditions from a view
  set-fetchxml     Apply a complete FetchXML document to a view, replacing the existing fetchxml.
  
                   Expected format (file must have <fetch> as root element):
                     <fetch version="1.0" output-format="xml-platform" mapping="logical" no-lock="false">
                       <entity name="account">
                         <attribute name="name" />
                         <order attribute="name" descending="false" />
                         <filter type="and">
                           <condition attribute="statecode" operator="eq" value="0" />
                         </filter>
                       </entity>
                     </fetch>
```

## `ppds views add-column`

```text
Description:
  Add one or more columns to a view

Usage:
  ppds views add-column [options]

Options:
  -p, --profile <profile>                Authentication profile name
  -e, --environment <environment>        Override the environment URL.
  --entity <entity>                      [Required] Entity logical name (e.g., account)
  -v, --view <view>                      [Required] View name or ID
  -c, --column <column>                  [Required] Column to add. Format: 'attributename' or 'attributename:width' (default width 150). Repeatable.
  --via-relationship <via-relationship>  Lookup/relationship attribute to use for related-entity columns
  --solution <solution>                  Add the view to this solution after the operation
  --publish                              Publish the entity after the operation
  -q, --quiet                            Show only warnings and errors
  -v, --verbose                          Show detailed output including debug messages
  --debug                                Show trace-level diagnostic output
  --correlation-id <correlation-id>      Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>    Output format [default: Text]
  -?, -h, --help                         Show help and usage information
```

## `ppds views clear-filter`

```text
Description:
  Remove all filter conditions from a view

Usage:
  ppds views clear-filter [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -v, --view <view>                    [Required] View name or ID
  --solution <solution>                Add the view to this solution after the operation
  --publish                            Publish the entity after the operation
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds views clear-sort`

```text
Description:
  Remove all sort configuration from a view

Usage:
  ppds views clear-sort [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -v, --view <view>                    [Required] View name or ID
  --solution <solution>                Add the view to this solution after the operation
  --publish                            Publish the entity after the operation
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds views get`

```text
Description:
  Get detailed view configuration including columns, sort, and filter

Usage:
  ppds views get [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -v, --view <view>                    [Required] View name or ID
  --unpublished                        Show the unpublished (latest draft) view instead of the published version
  --raw                                Write raw fetchxml to stdout instead of the structured summary
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds views list`

```text
Description:
  List all views for an entity

Usage:
  ppds views list [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds views remove-column`

```text
Description:
  Remove a column from a view by attribute name

Usage:
  ppds views remove-column [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -v, --view <view>                    [Required] View name or ID
  -c, --column <column>                [Required] Attribute name of the column to remove
  --solution <solution>                Add the view to this solution after the operation
  --publish                            Publish the entity after the operation
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds views reorder-columns`

```text
Description:
  Set the authoritative column order for a view. Columns not listed are dropped.

Usage:
  ppds views reorder-columns [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -v, --view <view>                    [Required] View name or ID
  --columns <columns>                  [Required] Comma-separated list of attribute names in desired order. Columns not in the list are dropped.
  --solution <solution>                Add the view to this solution after the operation
  --publish                            Publish the entity after the operation
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds views set-fetchxml`

```text
Description:
  Apply a complete FetchXML document to a view, replacing the existing fetchxml.
  
  Expected format (file must have <fetch> as root element):
    <fetch version="1.0" output-format="xml-platform" mapping="logical" no-lock="false">
      <entity name="account">
        <attribute name="name" />
        <order attribute="name" descending="false" />
        <filter type="and">
          <condition attribute="statecode" operator="eq" value="0" />
        </filter>
      </entity>
    </fetch>

Usage:
  ppds views set-fetchxml [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -v, --view <view>                    [Required] View name or ID
  --fetchxml <fetchxml>                [Required] Path to a file containing a complete FetchXML document with <fetch> root element.
  --solution <solution>                Add the view to this solution after the operation
  --publish                            Publish the entity after the operation
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds views set-filter`

```text
Description:
  Set or replace the filter on a view.
  
  Use --filter-file to apply a <filter> XML fragment from a file:
    <filter type="and">
      <condition attribute="statecode" operator="eq" value="0" />
    </filter>
  
  Use --condition for a quick single-condition filter: --condition "statecode:eq:0"

Usage:
  ppds views set-filter [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -v, --view <view>                    [Required] View name or ID
  --filter-file <filter-file>          Path to a file containing a <filter> XML fragment. Mutually exclusive with --condition.
  --condition <condition>              Inline single condition in format 'attribute:operator:value' (e.g. statecode:eq:0). Mutually exclusive with --filter-file.
  --solution <solution>                Add the view to this solution after the operation
  --publish                            Publish the entity after the operation
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds views set-sort`

```text
Description:
  Set the sort order for a view. Multiple --sort flags applied in declaration order.

Usage:
  ppds views set-sort [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -v, --view <view>                    [Required] View name or ID
  --sort <sort>                        [Required] Sort specification: 'attributename:asc' or 'attributename:desc'. Repeatable; applied in declaration order (first = primary).
  --solution <solution>                Add the view to this solution after the operation
  --publish                            Publish the entity after the operation
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds views update-column`

```text
Description:
  Update the width of an existing column in a view

Usage:
  ppds views update-column [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL.
  --entity <entity>                    [Required] Entity logical name (e.g., account)
  -v, --view <view>                    [Required] View name or ID
  -c, --column <column>                [Required] Attribute name of the column to update
  --width <width>                      [Required] New column width in pixels (positive integer)
  --solution <solution>                Add the view to this solution after the operation
  --publish                            Publish the entity after the operation
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

