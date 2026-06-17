# `ppds service-endpoints` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds service-endpoints`

```text
Description:
  Service endpoint management: list, get, register, update, unregister

Usage:
  ppds service-endpoints [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list                     List registered service endpoints in the environment
  get <name-or-id>         Get details for a specific service endpoint
  register                 Register a service endpoint: webhook, queue, topic, eventhub
  update <name-or-id>      Update an existing service endpoint
  unregister <name-or-id>  Unregister a service endpoint from Dataverse
```

## `ppds service-endpoints get`

```text
Description:
  Get details for a specific service endpoint

Usage:
  ppds service-endpoints get <name-or-id> [options]

Arguments:
  <name-or-id>  Service endpoint name or GUID

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

## `ppds service-endpoints list`

```text
Description:
  List registered service endpoints in the environment

Usage:
  ppds service-endpoints list [options]

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

## `ppds service-endpoints register`

```text
Description:
  Register a service endpoint: webhook, queue, topic, eventhub

Usage:
  ppds service-endpoints register [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  webhook <name>   Register an HTTP webhook endpoint
  queue <name>     Register an Azure Service Bus queue endpoint
  topic <name>     Register an Azure Service Bus topic endpoint
  eventhub <name>  Register an Azure Event Hub endpoint
```

## `ppds service-endpoints unregister`

```text
Description:
  Unregister a service endpoint from Dataverse

Usage:
  ppds service-endpoints unregister <name-or-id> [options]

Arguments:
  <name-or-id>  Service endpoint name or GUID

Options:
  -f, --force                          Force cascade delete of dependent step registrations
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds service-endpoints update`

```text
Description:
  Update an existing service endpoint

Usage:
  ppds service-endpoints update <name-or-id> [options]

Arguments:
  <name-or-id>  Service endpoint name or GUID

Options:
  --name <name>                        New display name for the endpoint
  --description <description>          New description for the endpoint
  --url <url>                          New webhook URL (webhooks only)
  --auth-type <auth-type>              New authentication type
  --auth-value <auth-value>            New auth secret value
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds service-endpoints register eventhub`

```text
Description:
  Register an Azure Event Hub endpoint

Usage:
  ppds service-endpoints register eventhub <name> [options]

Arguments:
  <name>  Unique display name for the endpoint

Options:
  --namespace <namespace>              [Required] Service Bus namespace address (e.g. sb://myns.servicebus.windows.net)
  --path <path>                        [Required] EventHub name
  --sas-key-name <sas-key-name>        [Required] SAS key name
  --sas-key <sas-key>                  [Required] SAS key value (exactly 44 characters)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds service-endpoints register queue`

```text
Description:
  Register an Azure Service Bus queue endpoint

Usage:
  ppds service-endpoints register queue <name> [options]

Arguments:
  <name>  Unique display name for the endpoint

Options:
  --namespace <namespace>              [Required] Service Bus namespace address (e.g. sb://myns.servicebus.windows.net)
  --path <path>                        [Required] Queue name
  --sas-key-name <sas-key-name>        [Required] SAS key name
  --sas-key <sas-key>                  [Required] SAS key value (exactly 44 characters)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds service-endpoints register topic`

```text
Description:
  Register an Azure Service Bus topic endpoint

Usage:
  ppds service-endpoints register topic <name> [options]

Arguments:
  <name>  Unique display name for the endpoint

Options:
  --namespace <namespace>              [Required] Service Bus namespace address (e.g. sb://myns.servicebus.windows.net)
  --path <path>                        [Required] Topic name
  --sas-key-name <sas-key-name>        [Required] SAS key name
  --sas-key <sas-key>                  [Required] SAS key value (exactly 44 characters)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds service-endpoints register webhook`

```text
Description:
  Register an HTTP webhook endpoint

Usage:
  ppds service-endpoints register webhook <name> [options]

Arguments:
  <name>  Unique display name for the webhook endpoint

Options:
  --url <url>                          [Required] Absolute HTTPS/HTTP URL of the webhook receiver
  --auth-type <auth-type>              [Required] Authentication type: WebhookKey, HttpHeader, or HttpQueryString
  --auth-key <auth-key>                Auth key name (for HttpHeader or HttpQueryString auth types)
  --auth-value <auth-value>            Auth secret value. For WebhookKey: plain string. For HttpHeader/HttpQueryString: name=value pairs.
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

