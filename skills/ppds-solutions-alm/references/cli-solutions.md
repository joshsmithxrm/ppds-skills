# `ppds solutions` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds solutions`

```text
Description:
  Manage Dataverse solutions: list, get, export, import, publish

Usage:
  ppds solutions [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list                      List solutions in the environment
  get <unique-name>         Get details for a specific solution
  export <unique-name>      Export a solution to a ZIP file
  import <file>             Import a solution from a ZIP file
  components <unique-name>  List components in a solution
  publish                   Publish all customizations (alias for ppds publish --all)
  url <unique-name>         Get the Maker portal URL for a solution
```

## `ppds solutions components`

```text
Description:
  List components in a solution

Usage:
  ppds solutions components <unique-name> [options]

Arguments:
  <unique-name>  The solution unique name

Options:
  -t, --type <type>                    Filter by component type (e.g., 61 for WebResource, 69 for PluginAssembly)
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds solutions export`

```text
Description:
  Export a solution to a ZIP file

Usage:
  ppds solutions export <unique-name> [options]

Arguments:
  <unique-name>  The solution unique name

Options:
  -o, --output <output>                Output file path (default: <unique-name>.zip or <unique-name>_managed.zip)
  --managed                            Export as managed solution
  --allow-outside-workspace            Permit --output paths that resolve outside the current working directory. Off by default to prevent a mistyped or redirected path from writing anywhere on disk.
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds solutions get`

```text
Description:
  Get details for a specific solution

Usage:
  ppds solutions get <unique-name> [options]

Arguments:
  <unique-name>  The solution unique name

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

## `ppds solutions import`

```text
Description:
  Import a solution from a ZIP file

Usage:
  ppds solutions import <file> [options]

Arguments:
  <file>  The solution ZIP file to import

Options:
  -w, --overwrite                      Overwrite unmanaged customizations (default: true)
  --publish-workflows                  Automatically publish workflows (default: true)
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds solutions list`

```text
Description:
  List solutions in the environment

Usage:
  ppds solutions list [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  --filter <filter>                    Filter by solution unique name or friendly name
  -m, --include-managed                Include managed solutions in the list
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds solutions publish`

```text
Description:
  Publish all customizations (alias for ppds publish --all)

Usage:
  ppds solutions publish [options]

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

## `ppds solutions url`

```text
Description:
  Get the Maker portal URL for a solution

Usage:
  ppds solutions url <unique-name> [options]

Arguments:
  <unique-name>  The solution unique name

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

