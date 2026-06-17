# `ppds plugintraces` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds plugintraces`

```text
Description:
  Query and manage plugin trace logs: list, get, related, timeline, settings, delete

Usage:
  ppds plugintraces [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list                 List plugin trace logs with optional filtering
  get <trace-id>       Get detailed information about a plugin trace
  settings             View or set plugin trace logging settings
  related <trace-id>   Get plugin traces related by correlation ID or record
  timeline <trace-id>  Display plugin execution timeline as a hierarchy tree
  delete <trace-id>    Delete plugin trace logs
```

## `ppds plugintraces delete`

```text
Description:
  Delete plugin trace logs

Usage:
  ppds plugintraces delete [<trace-id>] [options]

Arguments:
  <trace-id>  The plugin trace ID to delete

Options:
  --ids <ids>                          Comma-separated list of trace IDs to delete
  --older-than <older-than>            Delete traces older than this duration (e.g., 7d, 24h, 30m)
  --all                                Delete ALL plugin traces (requires --force)
  --dry-run                            Preview count without deleting
  --force                              Skip confirmation prompt
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugintraces get`

```text
Description:
  Get detailed information about a plugin trace

Usage:
  ppds plugintraces get <trace-id> [options]

Arguments:
  <trace-id>  The plugin trace ID

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugintraces list`

```text
Description:
  List plugin trace logs with optional filtering

Usage:
  ppds plugintraces list [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -t, --type <type>                    Filter by plugin type name (contains)
  -m, --message <message>              Filter by message name (Create, Update, etc.)
  --entity <entity>                    Filter by primary entity (contains)
  --mode <mode>                        Filter by execution mode: sync or async
  --errors-only                        Show only traces with exceptions
  --success-only                       Show only successful traces (no exceptions)
  --since <since>                      Show traces created after this time (ISO 8601)
  --until <until>                      Show traces created before this time (ISO 8601)
  --min-duration <min-duration>        Minimum execution duration in milliseconds
  --max-duration <max-duration>        Maximum execution duration in milliseconds
  --correlation-id <correlation-id>    Filter by correlation ID
  --request-id <request-id>            Filter by request ID
  --step-id <step-id>                  Filter by plugin step ID
  --last-hour                          Show traces from the last hour
  --last-24h                           Show traces from the last 24 hours
  --async-only                         Show only asynchronous traces
  --recursive                          Show only nested traces (depth > 1)
  --record <record>                    Filter by record (format: entity or entity/guid, e.g., account or account/12345678-...)
  --filter <filter>                    JSON file with filter criteria
  -n, --top <top>                      Maximum number of results to return [default: 100]
  --order-by <order-by>                Sort field (default: createdon desc)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugintraces related`

```text
Description:
  Get plugin traces related by correlation ID or record

Usage:
  ppds plugintraces related [<trace-id>] [options]

Arguments:
  <trace-id>  The plugin trace ID (gets correlation ID from this trace)

Options:
  -c, --correlation-id <correlation-id>  The correlation ID to look up (alternative to trace-id)
  --record <record>                      Filter by record (format: entity or entity/guid, e.g., account or account/12345678-...)
  -n, --top <top>                        Maximum number of results to return [default: 1000]
  -p, --profile <profile>                Authentication profile name
  -e, --environment <environment>        Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                            Show only warnings and errors
  -v, --verbose                          Show detailed output including debug messages
  --debug                                Show trace-level diagnostic output
  --correlation-id <correlation-id>      Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>    Output format [default: Text]
  -?, -h, --help                         Show help and usage information
```

## `ppds plugintraces settings`

```text
Description:
  View or set plugin trace logging settings

Usage:
  ppds plugintraces settings [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  get          Get current plugin trace logging setting
  set <value>  Set plugin trace logging setting
```

## `ppds plugintraces timeline`

```text
Description:
  Display plugin execution timeline as a hierarchy tree

Usage:
  ppds plugintraces timeline [<trace-id>] [options]

Arguments:
  <trace-id>  Trace ID of any execution in the request - the timeline shows all related traces via the correlation ID

Options:
  -c, --correlation-id <correlation-id>  Correlation ID to look up directly (use this if you already have the correlation ID)
  -p, --profile <profile>                Authentication profile name
  -e, --environment <environment>        Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                            Show only warnings and errors
  -v, --verbose                          Show detailed output including debug messages
  --debug                                Show trace-level diagnostic output
  --correlation-id <correlation-id>      Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>    Output format [default: Text]
  -?, -h, --help                         Show help and usage information
```

## `ppds plugintraces settings get`

```text
Description:
  Get current plugin trace logging setting

Usage:
  ppds plugintraces settings get [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugintraces settings set`

```text
Description:
  Set plugin trace logging setting

Usage:
  ppds plugintraces settings set <value> [options]

Arguments:
  <value>  The trace setting: off, exception, or all

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

