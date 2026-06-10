# `ppds schema` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.4. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.4**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds schema`

```text
Description:
  Compare Dataverse schemas across environments and data packages.

Usage:
  ppds schema [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  compare  Compare schema between a data package and an environment, or between two environments. Differences are classified by severity (Error / Warning / Info); the highest severity determines the exit code. Supported output formats: Text (default), Json.
```

## `ppds schema compare`

```text
Description:
  Compare schema between a data package and an environment, or between two environments. Differences are classified by severity (Error / Warning / Info); the highest severity determines the exit code. Supported output formats: Text (default), Json.

Usage:
  ppds schema compare [options]

Options:
  --data <data>                        [Required with --environment] Path to a data package zip whose schema is compared against the target environment.
  -e, --environment <environment>      [Required with --data] Target environment - URL, friendly name, unique name, or ID.
  -se, --source-env <source-env>       [Required with --target-env] Source environment for env-to-env comparison.
  -te, --target-env <target-env>       [Required with --source-env] Target environment for env-to-env comparison.
  -p, --profile <profile>              Authentication profile name (defaults to active profile).
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

