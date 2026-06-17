# `ppds connections` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds connections`

```text
Description:
  Manage Power Platform connections (Power Apps Admin API)

Usage:
  ppds connections [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list      List connections from Power Apps Admin API
  get <id>  Get a connection by ID
```

## `ppds connections get`

```text
Description:
  Get a connection by ID

Usage:
  ppds connections get <id> [options]

Arguments:
  <id>  The connection ID

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Environment URL override
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds connections list`

```text
Description:
  List connections from Power Apps Admin API

Usage:
  ppds connections list [options]

Options:
  --connector <connector>              Filter by connector ID (e.g., shared_commondataserviceforapps)
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Environment URL override
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

