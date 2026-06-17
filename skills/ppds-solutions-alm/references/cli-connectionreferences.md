# `ppds connectionreferences` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds connectionreferences`

```text
Description:
  Manage connection references

Usage:
  ppds connectionreferences [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list                List connection references
  get <name>          Get a connection reference by logical name
  flows <name>        List flows that use a connection reference
  connections <name>  Show bound connection for a connection reference
  analyze             Analyze flow-connection reference relationships (orphan detection)
```

## `ppds connectionreferences analyze`

```text
Description:
  Analyze flow-connection reference relationships (orphan detection)

Usage:
  ppds connectionreferences analyze [options]

Options:
  -s, --solution <solution>            Filter by solution unique name
  --orphans-only                       Only show orphaned relationships
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Environment URL override
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds connectionreferences connections`

```text
Description:
  Show bound connection for a connection reference

Usage:
  ppds connectionreferences connections <name> [options]

Arguments:
  <name>  The logical name of the connection reference

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

## `ppds connectionreferences flows`

```text
Description:
  List flows that use a connection reference

Usage:
  ppds connectionreferences flows <name> [options]

Arguments:
  <name>  The logical name of the connection reference

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

## `ppds connectionreferences get`

```text
Description:
  Get a connection reference by logical name

Usage:
  ppds connectionreferences get <name> [options]

Arguments:
  <name>  The logical name of the connection reference

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

## `ppds connectionreferences list`

```text
Description:
  List connection references

Usage:
  ppds connectionreferences list [options]

Options:
  -s, --solution <solution>            Filter by solution unique name
  --unbound                            Only show connection references without a bound connection
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Environment URL override
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

