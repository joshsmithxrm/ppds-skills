# `ppds flows` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.4.3-alpha.0.8. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.4.3-alpha.0.8**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds flows`

```text
Description:
  Manage cloud flows (Power Automate)

Usage:
  ppds flows [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list        List cloud flows
  get <name>  Get a cloud flow by workflow ID or unique name
  url <name>  Get Power Automate maker URL for a flow
  enable      Enable solution cloud flows with preflight and verified outcomes
  disable     Disable solution cloud flows (does not cancel existing runs)
```

## `ppds flows disable`

```text
Description:
  Disable solution cloud flows (does not cancel existing runs)

Usage:
  ppds flows disable [options]

Options:
  --id <id>                                  Exact workflow ID
  --name <name>                              Exact flow unique/schema name
  --all                                      All eligible cloud-flow definitions in --solution
  --dry-run                                  Inspect a fresh plan without writing
  --confirm-env <confirm-env>                Acknowledge the exact resolved environment URL
  --timeout <timeout>                        State-verification deadline per flow in seconds (1-3600; default 60)
  --max-flows <max-flows>                    Maximum eligible flow count (default 100); exceeding it fails without writes
  --expected-plan-hash <expected-plan-hash>  Require this dry-run plan fingerprint before writes
  -s, --solution <solution>                  Filter by solution unique name
  -p, --profile <profile>                    Authentication profile name
  -e, --environment <environment>            Environment URL override
  -q, --quiet                                Show only warnings and errors
  -v, --verbose                              Show detailed output including debug messages
  --debug                                    Show trace-level diagnostic output
  --correlation-id <correlation-id>          Correlation ID for distributed tracing
  -f, --output-format <Text|Json>            Output format [default: Text]
  -?, -h, --help                             Show help and usage information
```

## `ppds flows enable`

```text
Description:
  Enable solution cloud flows with preflight and verified outcomes

Usage:
  ppds flows enable [options]

Options:
  --id <id>                                  Exact workflow ID
  --name <name>                              Exact flow unique/schema name
  --all                                      All eligible cloud-flow definitions in --solution
  --dry-run                                  Inspect a fresh plan without writing
  --confirm-env <confirm-env>                Acknowledge the exact resolved environment URL
  --timeout <timeout>                        State-verification deadline per flow in seconds (1-3600; default 60)
  --max-flows <max-flows>                    Maximum eligible flow count (default 100); exceeding it fails without writes
  --expected-plan-hash <expected-plan-hash>  Require this dry-run plan fingerprint before writes
  -s, --solution <solution>                  Filter by solution unique name
  -p, --profile <profile>                    Authentication profile name
  -e, --environment <environment>            Environment URL override
  -q, --quiet                                Show only warnings and errors
  -v, --verbose                              Show detailed output including debug messages
  --debug                                    Show trace-level diagnostic output
  --correlation-id <correlation-id>          Correlation ID for distributed tracing
  -f, --output-format <Text|Json>            Output format [default: Text]
  -?, -h, --help                             Show help and usage information
```

## `ppds flows get`

```text
Description:
  Get a cloud flow by workflow ID or unique name

Usage:
  ppds flows get <name> [options]

Arguments:
  <name>  The workflow ID (GUID) or unique name

Options:
  -p, --profile <profile>            Authentication profile name
  -e, --environment <environment>    Environment URL override
  -q, --quiet                        Show only warnings and errors
  -v, --verbose                      Show detailed output including debug messages
  --debug                            Show trace-level diagnostic output
  --correlation-id <correlation-id>  Correlation ID for distributed tracing
  -f, --output-format <Text|Json>    Output format [default: Text]
  -?, -h, --help                     Show help and usage information
```

## `ppds flows list`

```text
Description:
  List cloud flows

Usage:
  ppds flows list [options]

Options:
  -s, --solution <solution>          Filter by solution unique name
  --state <state>                    Filter by state (Draft, Activated, Suspended)
  -p, --profile <profile>            Authentication profile name
  -e, --environment <environment>    Environment URL override
  -q, --quiet                        Show only warnings and errors
  -v, --verbose                      Show detailed output including debug messages
  --debug                            Show trace-level diagnostic output
  --correlation-id <correlation-id>  Correlation ID for distributed tracing
  -f, --output-format <Text|Json>    Output format [default: Text]
  -?, -h, --help                     Show help and usage information
```

## `ppds flows url`

```text
Description:
  Get Power Automate maker URL for a flow

Usage:
  ppds flows url <name> [options]

Arguments:
  <name>  The workflow ID (GUID) or unique name

Options:
  -p, --profile <profile>            Authentication profile name
  -e, --environment <environment>    Environment URL override
  -q, --quiet                        Show only warnings and errors
  -v, --verbose                      Show detailed output including debug messages
  --debug                            Show trace-level diagnostic output
  --correlation-id <correlation-id>  Correlation ID for distributed tracing
  -f, --output-format <Text|Json>    Output format [default: Text]
  -?, -h, --help                     Show help and usage information
```

