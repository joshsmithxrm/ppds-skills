# `ppds plugins` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds plugins`

```text
Description:
  Plugin registration management: extract, deploy, register, diff, list, get, clean, download, update, unregister, enable, disable

Usage:
  ppds plugins [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  extract                         Extract plugin step/image attributes from assembly to JSON configuration
  deploy                          Deploy plugin registrations to environment
  register                        Register plugin components: assembly, package, type, step, image
  diff                            Compare configuration against environment state
  list                            List registered plugins in the environment
  get <type> <name-or-id>         Get details for a specific plugin entity
  clean                           Remove orphaned registrations not in configuration
  download                        Download plugin assembly or package binary from Dataverse
  update                          Update existing plugin registrations
  unregister <type> <name-or-id>  Unregister plugin entities from Dataverse
  enable <step-name-or-id>        Enable a plugin processing step
  disable <step-name-or-id>       Disable a plugin processing step
```

## `ppds plugins clean`

```text
Description:
  Remove orphaned registrations not in configuration

Usage:
  ppds plugins clean [options]

Options:
  -c, --config <config>                [Required] Path to registrations.json
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  --dry-run                            Preview deletions without applying
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins deploy`

```text
Description:
  Deploy plugin registrations to environment

Usage:
  ppds plugins deploy [options]

Options:
  -c, --config <config>                [Required] Path to registrations.json
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Solution unique name. Overrides value in configuration file.
  --clean                              Also remove orphaned registrations not in config
  --dry-run                            Preview changes without applying
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins diff`

```text
Description:
  Compare configuration against environment state

Usage:
  ppds plugins diff [options]

Options:
  -c, --config <config>                [Required] Path to registrations.json
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins disable`

```text
Description:
  Disable a plugin processing step

Usage:
  ppds plugins disable <step-name-or-id> [options]

Arguments:
  <step-name-or-id>  Step name or GUID to disable

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

## `ppds plugins download`

```text
Description:
  Download plugin assembly or package binary from Dataverse

Usage:
  ppds plugins download [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  assembly <name-or-id>  Download a plugin assembly DLL
  package <name-or-id>   Download a plugin package (nupkg)
```

## `ppds plugins enable`

```text
Description:
  Enable a plugin processing step

Usage:
  ppds plugins enable <step-name-or-id> [options]

Arguments:
  <step-name-or-id>  Step name or GUID to enable

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

## `ppds plugins extract`

```text
Description:
  Extract plugin step/image attributes from assembly to JSON configuration

Usage:
  ppds plugins extract [options]

Options:
  -i, --input <input>                  [Required] Path to assembly (.dll) or plugin package (.nupkg)
  -o, --output <output>                Output file path (default: registrations.json in input directory)
  -s, --solution <solution>            Solution unique name to add components to
  -f, --force                          Overwrite existing file without merging
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins get`

```text
Description:
  Get details for a specific plugin entity

Usage:
  ppds plugins get <type> <name-or-id> [options]

Arguments:
  <type>        Entity type: assembly, package, type, step, image
  <name-or-id>  Entity name or GUID

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

## `ppds plugins list`

```text
Description:
  List registered plugins in the environment

Usage:
  ppds plugins list [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -a, --assembly <assembly>            Filter by assembly name (classic DLL plugins)
  -pkg, --package <package>            Filter by package name or unique name (NuGet plugin packages)
  --include-hidden                     Include hidden steps (excluded by default)
  --include-microsoft                  Include Microsoft.* assemblies (excluded by default, except Microsoft.Crm.ServiceBus)
  --all                                Show all plugins (equivalent to --include-hidden --include-microsoft)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins register`

```text
Description:
  Register plugin components: assembly, package, type, step, image

Usage:
  ppds plugins register [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  assembly <path>  Register a plugin assembly (DLL)
  package <path>   Register a plugin package (NuGet)
  type <assembly>  Register a plugin type within an assembly
  step <type>      Register a processing step for a plugin type
  image <step>     Register an image for a processing step
```

## `ppds plugins unregister`

```text
Description:
  Unregister plugin entities from Dataverse

Usage:
  ppds plugins unregister <type> <name-or-id> [options]

Arguments:
  <type>        The type of entity to unregister: assembly, package, type, step, image
  <name-or-id>  Name or GUID of the entity to unregister

Options:
  -f, --force                          Force cascade delete of all child entities
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins update`

```text
Description:
  Update existing plugin registrations

Usage:
  ppds plugins update [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  assembly <name> <path>  Update assembly content with new DLL
  package <name> <path>   Update package content with new nupkg
  step <name-or-id>       Update step properties
  image <name-or-id>      Update image attributes
```

## `ppds plugins download assembly`

```text
Description:
  Download a plugin assembly DLL

Usage:
  ppds plugins download assembly <name-or-id> [options]

Arguments:
  <name-or-id>  Assembly name or GUID

Options:
  -o, --output <output>                [Required] Output file path or directory
  -f, --force                          Overwrite existing file
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins download package`

```text
Description:
  Download a plugin package (nupkg)

Usage:
  ppds plugins download package <name-or-id> [options]

Arguments:
  <name-or-id>  Package name, unique name, or GUID

Options:
  -o, --output <output>                [Required] Output file path or directory
  -f, --force                          Overwrite existing file
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins register assembly`

```text
Description:
  Register a plugin assembly (DLL)

Usage:
  ppds plugins register assembly <path> [options]

Arguments:
  <path>  Path to the plugin assembly DLL file

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Solution unique name. Overrides value in configuration file.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins register image`

```text
Description:
  Register an image for a processing step

Usage:
  ppds plugins register image <step> [options]

Arguments:
  <step>  Step name to attach the image to

Options:
  --name <name>                        [Required] Image name
  --type <type>                        [Required] Image type: pre, post, or both
  --attributes <attributes>            Comma-separated list of attributes to include (all if not specified)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Solution unique name. Overrides value in configuration file.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins register package`

```text
Description:
  Register a plugin package (NuGet)

Usage:
  ppds plugins register package <path> [options]

Arguments:
  <path>  Path to the plugin package (.nupkg) file

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Solution unique name. Overrides value in configuration file.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins register step`

```text
Description:
  Register a processing step for a plugin type

Usage:
  ppds plugins register step <type> [options]

Arguments:
  <type>  Plugin type name (fully qualified)

Options:
  --message <message>                            [Required] SDK message name (Create, Update, Delete, etc.)
  --entity <entity>                              [Required] Primary entity logical name
  --stage <stage>                                [Required] Pipeline stage: PreValidation, PreOperation, or PostOperation
  --mode <mode>                                  Execution mode: Sync or Async [default: Sync]
  --rank <rank>                                  Execution order (1-999999) [default: 1]
  --filtering-attributes <filtering-attributes>  Comma-separated list of attributes that trigger this step (for Update message)
  --name <name>                                  Step display name (auto-generated if not specified)
  --secure-config <secure-config>                Secure configuration string (write-only, not stored in source control)
  --event-handler-type <event-handler-type>      Event handler type: pluginType or serviceEndpoint [default: pluginType]
  -p, --profile <profile>                        Authentication profile name
  -env, --environment <environment>              Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>                      Solution unique name. Overrides value in configuration file.
  -q, --quiet                                    Show only warnings and errors
  -v, --verbose                                  Show detailed output including debug messages
  --debug                                        Show trace-level diagnostic output
  --correlation-id <correlation-id>              Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>            Output format [default: Text]
  -?, -h, --help                                 Show help and usage information
```

## `ppds plugins register type`

```text
Description:
  Register a plugin type within an assembly

Usage:
  ppds plugins register type <assembly> [options]

Arguments:
  <assembly>  Assembly name containing the plugin type

Options:
  --typename <typename>                [Required] Fully qualified type name (namespace.classname)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Solution unique name. Overrides value in configuration file.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins update assembly`

```text
Description:
  Update assembly content with new DLL

Usage:
  ppds plugins update assembly <name> <path> [options]

Arguments:
  <name>  Assembly name
  <path>  Path to the assembly DLL

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Solution unique name. Overrides value in configuration file.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins update image`

```text
Description:
  Update image attributes

Usage:
  ppds plugins update image <name-or-id> [options]

Arguments:
  <name-or-id>  Image name or GUID

Options:
  --attributes <attributes>            Comma-separated list of attributes to include in the image
  --name <name>                        New name for the image
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins update package`

```text
Description:
  Update package content with new nupkg

Usage:
  ppds plugins update package <name> <path> [options]

Arguments:
  <name>  Package name or unique name
  <path>  Path to the .nupkg file

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -s, --solution <solution>            Solution unique name. Overrides value in configuration file.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds plugins update step`

```text
Description:
  Update step properties

Usage:
  ppds plugins update step <name-or-id> [options]

Arguments:
  <name-or-id>  Step name or GUID

Options:
  --mode <mode>                                  Execution mode: Sync or Async
  --stage <stage>                                Pipeline stage: PreValidation, PreOperation, or PostOperation
  --rank <rank>                                  Execution order (1-999999)
  --filtering-attributes <filtering-attributes>  Comma-separated list of attributes that trigger this step
  --description <description>                    Step description
  --can-be-bypassed                              Whether this step can be bypassed via BypassBusinessLogicExecution
  --can-use-readonly                             Whether this step can use a read-only database connection
  --invocation-source <invocation-source>        Pipeline invocation source: Parent or Child
  -p, --profile <profile>                        Authentication profile name
  -env, --environment <environment>              Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                                    Show only warnings and errors
  -v, --verbose                                  Show detailed output including debug messages
  --debug                                        Show trace-level diagnostic output
  --correlation-id <correlation-id>              Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>            Output format [default: Text]
  -?, -h, --help                                 Show help and usage information
```

