# `ppds importjobs` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds importjobs`

```text
Description:
  Monitor solution import jobs: list, get, data, wait

Usage:
  ppds importjobs [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list       List import jobs in the environment
  get <id>   Get details for a specific import job
  data <id>  Get the raw XML data for an import job
  wait <id>  Wait for an import job to complete
  url <id>   Get the Maker portal URL for an import job
```

## `ppds importjobs data`

```text
Description:
  Get the raw XML data for an import job

Usage:
  ppds importjobs data <id> [options]

Arguments:
  <id>  The import job ID

Options:
  -o, --output <output>                Output file path (default: stdout)
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds importjobs get`

```text
Description:
  Get details for a specific import job

Usage:
  ppds importjobs get <id> [options]

Arguments:
  <id>  The import job ID

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

## `ppds importjobs list`

```text
Description:
  List import jobs in the environment

Usage:
  ppds importjobs list [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Filter by solution name
  -n, --top <top>                      Maximum number of results to return [default: 50]
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds importjobs url`

```text
Description:
  Get the Maker portal URL for an import job

Usage:
  ppds importjobs url <id> [options]

Arguments:
  <id>  The import job ID

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

## `ppds importjobs wait`

```text
Description:
  Wait for an import job to complete

Usage:
  ppds importjobs wait <id> [options]

Arguments:
  <id>  The import job ID

Options:
  -t, --timeout <timeout>              Maximum wait time in minutes [default: 30]
  -i, --interval <interval>            Poll interval in seconds [default: 5]
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

