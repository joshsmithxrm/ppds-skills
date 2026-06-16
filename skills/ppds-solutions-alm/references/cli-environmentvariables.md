# `ppds environmentvariables` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds environmentvariables`

```text
Description:
  Manage environment variables

Usage:
  ppds environmentvariables [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list                      List environment variables
  get <schemaName>          Get environment variable details
  set <schemaName> <value>  Set an environment variable value
  export                    Export environment variables for deployment settings
  url <schemaName>          Get the Maker portal URL for an environment variable
```

## `ppds environmentvariables export`

```text
Description:
  Export environment variables for deployment settings

Usage:
  ppds environmentvariables export [options]

Options:
  -s, --solution <solution>            Filter by solution unique name
  -o, --output <output>                Output file path (default: stdout)
  -p, --profile <profile>              Authentication profile to use
  -e, --environment <environment>      Target environment (name, URL, or ID)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds environmentvariables get`

```text
Description:
  Get environment variable details

Usage:
  ppds environmentvariables get <schemaName> [options]

Arguments:
  <schemaName>  The schema name of the environment variable

Options:
  -p, --profile <profile>              Authentication profile to use
  -e, --environment <environment>      Target environment (name, URL, or ID)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds environmentvariables list`

```text
Description:
  List environment variables

Usage:
  ppds environmentvariables list [options]

Options:
  -s, --solution <solution>            Filter by solution unique name
  -p, --profile <profile>              Authentication profile to use
  -e, --environment <environment>      Target environment (name, URL, or ID)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds environmentvariables set`

```text
Description:
  Set an environment variable value

Usage:
  ppds environmentvariables set <schemaName> <value> [options]

Arguments:
  <schemaName>  The schema name of the environment variable
  <value>       The value to set

Options:
  -p, --profile <profile>              Authentication profile to use
  -e, --environment <environment>      Target environment (name, URL, or ID)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds environmentvariables url`

```text
Description:
  Get the Maker portal URL for an environment variable

Usage:
  ppds environmentvariables url <schemaName> [options]

Arguments:
  <schemaName>  The schema name of the environment variable

Options:
  -p, --profile <profile>              Authentication profile to use
  -e, --environment <environment>      Target environment (name, URL, or ID)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

