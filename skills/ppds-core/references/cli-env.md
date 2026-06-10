# `ppds env` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.4. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.4**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds env`

```text
Description:
  Manage environment selection

Usage:
  ppds env [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  list                                                      List available environments
  select                                                    Select the active environment for the current profile
  who                                                       Verify connection and show current user info from Dataverse
  config <url>                                              Configure environment display settings (label, type, color)
  type <Development|Production|Sandbox|Test|Trial|Unknown>  Manage custom environment type definitions
```

## `ppds env config`

```text
Description:
  Configure environment display settings (label, type, color)

Usage:
  ppds env config [<url>] [options]

Arguments:
  <url>  Environment URL to configure

Options:
  -l, --label <label>                                                                                                 Short display label for status bar and tabs
  -t, --type <Development|Production|Sandbox|Test|Trial|Unknown>                                                      Environment type (Production, Sandbox, Development, Test, Trial)
  -c, --color <Blue|BrightBlue|BrightCyan|BrightGreen|BrightRed|BrightYellow|Brown|Cyan|Gray|Green|Red|White|Yellow>  Status bar color. Valid values: Red, Green, Yellow, Cyan, Blue, Gray, Brown, BrightRed, BrightGreen, BrightYellow, BrightCyan, BrightBlue, White
  -s, --show                                                                                                          Show current configuration for the environment
  --list                                                                                                              List all configured environments
  --remove                                                                                                            Remove configuration for the environment
  -?, -h, --help                                                                                                      Show help and usage information
```

## `ppds env list`

```text
Description:
  List available environments

Usage:
  ppds env list [options]

Options:
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -fl, --filter <filter>               Filter environments by name, URL, or ID (case-insensitive)
  -?, -h, --help                       Show help and usage information
```

## `ppds env select`

```text
Description:
  Select the active environment for the current profile

Usage:
  ppds env select [options]

Options:
  -env, --environment <environment>  [Required] Default environment (ID, url, unique name, or partial name)
  -?, -h, --help                     Show help and usage information
```

## `ppds env type`

```text
Description:
  Manage custom environment type definitions

Usage:
  ppds env type [<name>] [options]

Arguments:
  <Development|Production|Sandbox|Test|Trial|Unknown>  Type name (Production, Sandbox, Development, Test, Trial)

Options:
  -c, --color <Blue|BrightBlue|BrightCyan|BrightGreen|BrightRed|BrightYellow|Brown|Cyan|Gray|Green|Red|White|Yellow>  Default color for this type
  --remove                                                                                                            Remove this custom type definition
  --list                                                                                                              List all type definitions (built-in + custom)
  -?, -h, --help                                                                                                      Show help and usage information
```

## `ppds env who`

```text
Description:
  Verify connection and show current user info from Dataverse

Usage:
  ppds env who [options]

Options:
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -env, --environment <environment>    Environment to query (ID, URL, unique name, or partial name). Uses profile default if not specified.
  -?, -h, --help                       Show help and usage information
```

