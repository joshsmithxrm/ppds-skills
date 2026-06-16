# `ppds publish` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds publish`

```text
Description:
  Publish Dataverse customizations

Usage:
  ppds publish [<names>...] [options]

Arguments:
  <names>  Web resource names, partial names, or GUIDs to publish

Options:
  --all                                Publish all customizations (PublishAllXml). Cannot combine with other flags.
  -t, --type <type>                    Component type to publish. Required when specifying resources or --solution. Supported: webresource, entity
  -s, --solution <solution>            Publish all components of the specified type in this solution
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

