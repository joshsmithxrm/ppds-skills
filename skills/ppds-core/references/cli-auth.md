# `ppds auth` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds auth`

```text
Description:
  Manage authentication profiles

Usage:
  ppds auth [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  create  Create and store authentication profiles on this computer
  list    List all authentication profiles
  select  Select which authentication profile should be active
  delete  Delete a particular authentication profile
  update  Update profile name or default environment
  name    Name or rename an existing authentication profile
  clear   Delete all profiles and cached credentials
  who     Show the current active profile
```

## `ppds auth clear`

```text
Description:
  Delete all profiles and cached credentials

Usage:
  ppds auth clear [options]

Options:
  -?, -h, --help  Show help and usage information
```

## `ppds auth create`

```text
Description:
  Create and store authentication profiles on this computer

Usage:
  ppds auth create [options]

Options:
  -n, --name <name>                                     The name you want to give to this authentication profile (maximum 30 characters)
  -env, --environment <environment>                     Default environment (ID, url, unique name, or partial name)
  -ci, --cloud <China|Public|UsGov|UsGovDod|UsGovHigh>  Optional: The cloud instance to authenticate with [default: Public]
  -t, --tenant <tenant>                                 Tenant ID if using application ID/client secret or application ID/client certificate
  -dc, --deviceCode                                     Use the Microsoft Entra ID Device Code flow for interactive sign-in
  -id, --applicationId <applicationId>                  Optional: The application ID to authenticate with
  -cs, --clientSecret <clientSecret>                    Optional: The client secret to authenticate with
  -cdp, --certificateDiskPath <certificateDiskPath>     Optional: The certificate disk path to authenticate with
  -cp, --certificatePassword <certificatePassword>      Optional: The certificate password to authenticate with
  -ct, --certificateThumbprint <certificateThumbprint>  Certificate thumbprint for Windows certificate store authentication
  -mi, --managedIdentity                                Use Azure Managed Identity
  -un, --username <username>                            Optional: The username to authenticate with; shows a Microsoft Entra ID dialog if not specified
  -p, --password <password>                             Optional: The password to authenticate with
  -ghf, --githubFederated                               Use GitHub Federation for Service Principal Auth; requires --tenant and --applicationId arguments
  -adof, --azureDevOpsFederated                         Use Azure DevOps Federation for Service Principal Auth; requires --tenant and --applicationId arguments
  -?, -h, --help                                        Show help and usage information
```

## `ppds auth delete`

```text
Description:
  Delete a particular authentication profile

Usage:
  ppds auth delete [options]

Options:
  -i, --index <index>  The index of the profile to be deleted
  -n, --name <name>    The name of the profile to be deleted
  -?, -h, --help       Show help and usage information
```

## `ppds auth list`

```text
Description:
  List all authentication profiles

Usage:
  ppds auth list [options]

Options:
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds auth name`

```text
Description:
  Name or rename an existing authentication profile

Usage:
  ppds auth name [options]

Options:
  -i, --index <index>  [Required] The index of the profile to be named/renamed
  -n, --name <name>    [Required] The name you want to give to this authentication profile (maximum 30 characters)
  -?, -h, --help       Show help and usage information
```

## `ppds auth select`

```text
Description:
  Select which authentication profile should be active

Usage:
  ppds auth select [options]

Options:
  -i, --index <index>  The index of the profile to be active
  -n, --name <name>    The name of the profile to be active
  -?, -h, --help       Show help and usage information
```

## `ppds auth update`

```text
Description:
  Update profile name or default environment

Usage:
  ppds auth update [options]

Options:
  -i, --index <index>                [Required] The index of the profile to update
  -n, --name <name>                  The name to give this profile (max 30 characters)
  -env, --environment <environment>  Default environment (ID, URL, unique name, or partial name)
  -?, -h, --help                     Show help and usage information
```

## `ppds auth who`

```text
Description:
  Show the current active profile

Usage:
  ppds auth who [options]

Options:
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

