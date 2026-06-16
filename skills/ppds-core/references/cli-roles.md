# `ppds roles` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds roles`

```text
Description:
  Manage security roles

Usage:
  ppds roles [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list           List security roles
  show <role>    Show role details and assigned users
  assign <role>  Assign a role to a user
  remove <role>  Remove a role from a user
```

## `ppds roles assign`

```text
Description:
  Assign a role to a user

Usage:
  ppds roles assign <role> [options]

Arguments:
  <role>  Role ID (GUID) or name

Options:
  -u, --user <user>                    [Required] User ID (GUID) or domain name
  -p, --profile <profile>              Authentication profile to use
  -e, --environment <environment>      Target environment (name, URL, or ID)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds roles list`

```text
Description:
  List security roles

Usage:
  ppds roles list [options]

Options:
  --filter <filter>                    Filter by role name
  -p, --profile <profile>              Authentication profile to use
  -e, --environment <environment>      Target environment (name, URL, or ID)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds roles remove`

```text
Description:
  Remove a role from a user

Usage:
  ppds roles remove <role> [options]

Arguments:
  <role>  Role ID (GUID) or name

Options:
  -u, --user <user>                    [Required] User ID (GUID) or domain name
  -p, --profile <profile>              Authentication profile to use
  -e, --environment <environment>      Target environment (name, URL, or ID)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds roles show`

```text
Description:
  Show role details and assigned users

Usage:
  ppds roles show <role> [options]

Arguments:
  <role>  Role ID (GUID) or name

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

