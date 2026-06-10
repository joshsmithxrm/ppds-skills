# `ppds users` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.4. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.4**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds users`

```text
Description:
  Manage users

Usage:
  ppds users [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list          List users
  show <user>   Show user details
  roles <user>  List roles for a user
```

## `ppds users list`

```text
Description:
  List users

Usage:
  ppds users list [options]

Options:
  --filter <filter>                    Filter by name, email, or domain
  --include-disabled                   Include disabled users
  -t, --top <top>                      Maximum number of results [default: 100]
  -p, --profile <profile>              Authentication profile to use
  -e, --environment <environment>      Target environment (name, URL, or ID)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds users roles`

```text
Description:
  List roles for a user

Usage:
  ppds users roles <user> [options]

Arguments:
  <user>  User ID (GUID) or domain name (e.g., user@domain.com)

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

## `ppds users show`

```text
Description:
  Show user details

Usage:
  ppds users show <user> [options]

Arguments:
  <user>  User ID (GUID) or domain name (e.g., user@domain.com)

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

