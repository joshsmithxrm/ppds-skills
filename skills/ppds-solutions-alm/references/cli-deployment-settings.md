# `ppds deployment-settings` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds deployment-settings`

```text
Description:
  Generate, sync, and validate deployment settings files

Usage:
  ppds deployment-settings [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  generate  Generate a new deployment settings file from current environment
  sync      Sync deployment settings file with solution (preserves existing values)
  validate  Validate deployment settings file against solution
```

## `ppds deployment-settings generate`

```text
Description:
  Generate a new deployment settings file from current environment

Usage:
  ppds deployment-settings generate [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name
  -o, --output <output>                [Required] Output file path
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Environment URL override
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds deployment-settings sync`

```text
Description:
  Sync deployment settings file with solution (preserves existing values)

Usage:
  ppds deployment-settings sync [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name
  -f, --file <file>                    [Required] Deployment settings file path
  --dry-run                            Show what would change without modifying the file
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Environment URL override
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds deployment-settings validate`

```text
Description:
  Validate deployment settings file against solution

Usage:
  ppds deployment-settings validate [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name
  --file <file>                        [Required] Deployment settings file path
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Environment URL override
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

