# `ppds query` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds query`

```text
Description:
  Execute FetchXML and SQL queries against Dataverse

Usage:
  ppds query [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  fetch <fetchxml>  Execute a FetchXML query against Dataverse
  sql <sql>         Execute a SQL query against Dataverse (transpiled to FetchXML)
  explain <sql>     Show the execution plan for a SQL query
  history           Manage SQL query history: list, get, execute, delete, clear
```

## `ppds query explain`

```text
Description:
  Show the execution plan for a SQL query

Usage:
  ppds query explain <sql> [options]

Arguments:
  <sql>  SQL query to explain

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

## `ppds query fetch`

```text
Description:
  Execute a FetchXML query against Dataverse

Usage:
  ppds query fetch [<fetchxml>] [options]

Arguments:
  <fetchxml>  FetchXML query string. Can be omitted if using --file or --stdin.

Options:
  --file <file>                        Read FetchXML from a file
  --stdin                              Read FetchXML from standard input
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -t, --top <top>                      Limit the number of results returned
  --page <page>                        Page number (1-based) for paged results
  --paging-cookie <paging-cookie>      Paging cookie from previous query for continuation
  -c, --count                          Include total record count in results
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds query history`

```text
Description:
  Manage SQL query history: list, get, execute, delete, clear

Usage:
  ppds query history [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list          List recent query history entries
  get <id>      Get a specific query history entry
  execute <id>  Re-execute a query from history
  delete <id>   Delete a query history entry
  clear         Clear all query history for the current environment
```

## `ppds query sql`

```text
Description:
  Execute a SQL query against Dataverse (transpiled to FetchXML)

Usage:
  ppds query sql [<sql>] [options]

Arguments:
  <sql>  SQL query string. Can be omitted if using --file or --stdin.

Options:
  --file <file>                        Read SQL from a file
  --stdin                              Read SQL from standard input
  --show-fetchxml                      Output the transpiled FetchXML instead of executing the query
  --explain                            Show the execution plan without executing the query
  --tds                                Route query through the TDS Endpoint (direct SQL) instead of FetchXML
  --confirm                            Confirm DML execution without interactive prompt
  --dry-run                            Show the execution plan without running the DML statement
  --no-limit                           Remove the 10,000 row safety cap for DML operations
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -t, --top <top>                      Limit the number of results returned
  --page <page>                        Page number (1-based) for paged results
  --paging-cookie <paging-cookie>      Paging cookie from previous query for continuation
  -c, --count                          Include total record count in results
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds query history clear`

```text
Description:
  Clear all query history for the current environment

Usage:
  ppds query history clear [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -f, --force                          Skip confirmation prompt
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds query history delete`

```text
Description:
  Delete a query history entry

Usage:
  ppds query history delete <id> [options]

Arguments:
  <id>  The history entry ID to delete

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

## `ppds query history execute`

```text
Description:
  Re-execute a query from history

Usage:
  ppds query history execute <id> [options]

Arguments:
  <id>  The history entry ID to execute

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -t, --top <top>                      Limit the number of results returned (overrides query TOP)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds query history get`

```text
Description:
  Get a specific query history entry

Usage:
  ppds query history get <id> [options]

Arguments:
  <id>  The history entry ID to retrieve

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

## `ppds query history list`

```text
Description:
  List recent query history entries

Usage:
  ppds query history list [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -l, --limit <limit>                  Maximum number of entries to return [default: 20]
  --filter <filter>                    Filter queries by substring match (case-insensitive)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

