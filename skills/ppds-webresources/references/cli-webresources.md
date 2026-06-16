# `ppds webresources` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds webresources`

```text
Description:
  Manage Dataverse web resources: list, get, url, publish, pull, push, create, update

Usage:
  ppds webresources [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list <name-pattern>   List web resources in the environment
  get <name>            Get web resource content
  url <name>            Get the Maker portal URL for a web resource
  publish <names>       Publish web resources (alias for ppds publish --type webresource)
  pull <folder>         Pull web resources to a local folder with tracking metadata
  push <folder>         Push locally-modified web resources back to Dataverse
  create <file>         Create a new web resource from a local file
  update <name> <file>  Update an existing web resource's content from a local file
```

## `ppds webresources create`

```text
Description:
  Create a new web resource from a local file

Usage:
  ppds webresources create <file> [options]

Arguments:
  <file>  Local file to upload as the web resource content

Options:
  --name <name>                        [Required] Logical name for the new web resource (e.g., new_/icons/vet.svg)
  --display-name <display-name>        Display name (defaults to the logical name)
  --type <type>                        Web resource type override; inferred from the file extension when omitted. One of: html, css, js, xml, png, jpg, gif, xap, xsl, ico, svg, resx
  -s, --solution <solution>            Solution unique name to add the web resource to
  --publish                            Publish the web resource after creation (required before it is visible to apps)
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds webresources get`

```text
Description:
  Get web resource content

Usage:
  ppds webresources get <name> [options]

Arguments:
  <name>  Web resource name, partial name, or GUID

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  --unpublished                        Get the unpublished (latest draft) version instead of published
  -o, --output <output>                Write content to file instead of stdout
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds webresources list`

```text
Description:
  List web resources in the environment

Usage:
  ppds webresources list [<name-pattern>] [options]

Arguments:
  <name-pattern>  Filter by partial name match (e.g., 'app.js', 'new_/scripts/')

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Filter by solution unique name
  -t, --type <type>                    Filter by type: text, image, data, or specific type (js, css, html, xml, png, etc.)
  --top <top>                          Maximum number of results (default: 5000)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds webresources publish`

```text
Description:
  Publish web resources (alias for ppds publish --type webresource)

Usage:
  ppds webresources publish [<names>...] [options]

Arguments:
  <names>  Web resource names, partial names, or GUIDs to publish

Options:
  -s, --solution <solution>            Publish all web resources in this solution
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds webresources pull`

```text
Description:
  Pull web resources to a local folder with tracking metadata

Usage:
  ppds webresources pull <folder> [options]

Arguments:
  <folder>  Target directory (created if missing)

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Filter by solution unique name
  -t, --type <type>                    Filter by type: text, image, data, or specific type (js, css, html, xml, png, etc.)
  --name <name>                        Filter by partial name match
  --strip-prefix                       Remove the solution publisher prefix from local file paths (e.g., new_/scripts/app.js -> scripts/app.js). The prefix is org-specific and set by the solution publisher.
  --force                              Overwrite local files even when they have been edited since the last pull
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds webresources push`

```text
Description:
  Push locally-modified web resources back to Dataverse

Usage:
  ppds webresources push <folder> [options]

Arguments:
  <folder>  Folder previously populated by 'ppds webresources pull'

Options:
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  --force                              Skip safety checks: server-conflict detection (someone edited since last pull) and environment URL validation (pulled from a different env than the current connection)
  --dry-run                            Preview what would be pushed without uploading. Still authenticates and queries the server for conflict detection.
  --publish                            After upload, run the Dataverse Publish step on the uploaded resources (required before changes take effect in apps)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds webresources update`

```text
Description:
  Update an existing web resource's content from a local file

Usage:
  ppds webresources update <name> <file> [options]

Arguments:
  <name>  Web resource name (exact) or GUID
  <file>  Local file whose content replaces the web resource content

Options:
  --publish                            Publish the web resource after the update (required before the change is visible to apps)
  -p, --profile <profile>              Authentication profile name
  -e, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds webresources url`

```text
Description:
  Get the Maker portal URL for a web resource

Usage:
  ppds webresources url <name> [options]

Arguments:
  <name>  Web resource name, partial name, or GUID

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

