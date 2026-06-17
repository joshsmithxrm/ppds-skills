# `ppds custom-apis` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds custom-apis`

```text
Description:
  Custom API management: list, get, register, update, unregister, add-parameter, update-parameter, remove-parameter

Usage:
  ppds custom-apis [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list                                      List registered Custom APIs in the environment
  get <unique-name-or-id>                   Get details for a specific Custom API
  register <unique-name>                    Register a new Custom API in Dataverse
  update <unique-name-or-id>                Update an existing Custom API
  unregister <unique-name-or-id>            Unregister a Custom API from Dataverse
  add-parameter <api-name> <param-name>     Add a request parameter or response property to a Custom API
  update-parameter <api-name> <param-name>  Update display name or description of a Custom API parameter
  remove-parameter <api-name> <param-name>  Remove a request parameter or response property from a Custom API
  set-plugin <unique-name-or-id>            Set or clear the implementing plugin type on a Custom API
```

## `ppds custom-apis add-parameter`

```text
Description:
  Add a request parameter or response property to a Custom API

Usage:
  ppds custom-apis add-parameter <api-name> <param-name> [options]

Arguments:
  <api-name>    Custom API unique name or GUID
  <param-name>  Unique parameter name

Options:
  --type <type>                        [Required] Data type: Boolean, DateTime, Decimal, Entity, EntityCollection, EntityReference, Float, Integer, Money, Picklist, String, StringArray, or Guid
  --direction <direction>              [Required] Direction: input or output
  --optional                           Mark the parameter as optional (input parameters only)
  --entity <entity>                    Logical entity name (required for Entity, EntityCollection, EntityReference types)
  --description <description>          Optional description
  --display-name <display-name>        Display name (defaults to param-name)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds custom-apis get`

```text
Description:
  Get details for a specific Custom API

Usage:
  ppds custom-apis get <unique-name-or-id> [options]

Arguments:
  <unique-name-or-id>  Custom API unique name or GUID

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds custom-apis list`

```text
Description:
  List registered Custom APIs in the environment

Usage:
  ppds custom-apis list [options]

Options:
  --solution <solution>                Filter by solution name
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds custom-apis register`

```text
Description:
  Register a new Custom API in Dataverse

Usage:
  ppds custom-apis register <unique-name> [options]

Arguments:
  <unique-name>  Unique message name for the Custom API

Options:
  --plugin <plugin>                        [Required] Plugin type name (e.g. MyAssembly.MyPlugin)
  --assembly <assembly>                    [Required] Plugin assembly name
  --display-name <display-name>            Display name for the Custom API (defaults to unique name)
  --description <description>              Optional description
  --binding-type <binding-type>            Binding type: Global, Entity, or EntityCollection (default: Global)
  --bound-entity <bound-entity>            Bound entity logical name (required when binding-type is Entity or EntityCollection)
  --is-function                            Mark this API as a function (returns a value)
  --is-private                             Mark this API as private
  --execute-privilege <execute-privilege>  Privilege name required to execute the API
  --allowed-step-type <allowed-step-type>  Allowed processing step type: None, AsyncOnly, or SyncAndAsync (default: None)
  -p, --profile <profile>                  Authentication profile name
  -env, --environment <environment>        Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                              Show only warnings and errors
  -v, --verbose                            Show detailed output including debug messages
  --debug                                  Show trace-level diagnostic output
  --correlation-id <correlation-id>        Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>      Output format [default: Text]
  -?, -h, --help                           Show help and usage information
```

## `ppds custom-apis remove-parameter`

```text
Description:
  Remove a request parameter or response property from a Custom API

Usage:
  ppds custom-apis remove-parameter <api-name> <param-name> [options]

Arguments:
  <api-name>    Custom API unique name or GUID
  <param-name>  Parameter unique name to remove

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds custom-apis set-plugin`

```text
Description:
  Set or clear the implementing plugin type on a Custom API

Usage:
  ppds custom-apis set-plugin <unique-name-or-id> [options]

Arguments:
  <unique-name-or-id>  Custom API unique name or GUID

Options:
  --plugin <plugin>                    Plugin type name to set as the implementing type
  --assembly <assembly>                Assembly name for disambiguation (optional)
  --none                               Clear the plugin type (mutually exclusive with --plugin)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds custom-apis unregister`

```text
Description:
  Unregister a Custom API from Dataverse

Usage:
  ppds custom-apis unregister <unique-name-or-id> [options]

Arguments:
  <unique-name-or-id>  Custom API unique name or GUID

Options:
  -f, --force                          Force cascade delete of dependent parameters and response properties
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds custom-apis update`

```text
Description:
  Update an existing Custom API

Usage:
  ppds custom-apis update <unique-name-or-id> [options]

Arguments:
  <unique-name-or-id>  Custom API unique name or GUID

Options:
  --display-name <display-name>        New display name
  --description <description>          New description
  --is-function                        Mark as function (returns a value)
  --is-private                         Mark as private
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds custom-apis update-parameter`

```text
Description:
  Update display name or description of a Custom API parameter

Usage:
  ppds custom-apis update-parameter <api-name> <param-name> [options]

Arguments:
  <api-name>    Custom API unique name or GUID
  <param-name>  Parameter unique name to update

Options:
  --display-name <display-name>        New display name for the parameter
  --description <description>          New description for the parameter
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

