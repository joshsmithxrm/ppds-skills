# `ppds metadata` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds metadata`

```text
Description:
  Browse Dataverse entity metadata: entities, attributes, relationships, option sets

Usage:
  ppds metadata [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  entities                List all entities with basic information
  entity <entity>         Get full metadata for a specific entity, or create/update/delete entities and manage status reasons (see subcommands)
  attribute               Create, update, or delete columns (attributes) on Dataverse tables
  attributes <entity>     List attributes for an entity
  relationships <entity>  List relationships for an entity
  keys <entity>           List alternate keys for an entity
  optionsets              List global option sets
  optionset <name>        Get details for or manage a global option set (choice)
  publish <names>         Publish entity metadata (alias for ppds publish --type entity)
  table                   Create, update, or delete Dataverse tables (deprecated - use 'entity')
  column                  Create, update, or delete columns (deprecated - use 'attribute')
  relationship            Create, update, or delete Dataverse relationships
  choice                  Manage global choices/option sets (deprecated - use 'optionset')
  key                     Create, delete, or reactivate alternate keys on Dataverse tables
```

## `ppds metadata attribute`

```text
Description:
  Create, update, or delete columns (attributes) on Dataverse tables

Usage:
  ppds metadata attribute [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  create         Create a new attribute on a Dataverse table (for Choice/Choices columns use --option to define a local option set, or --choice to attach a global one)
  update         Update an existing attribute on a Dataverse table
  delete         Delete an attribute from a Dataverse table
  add-option     Add an option to a column's local option set
  update-option  Update an option (label/color) on a column's local option set
  remove-option  Remove an option from a column's local option set
```

## `ppds metadata attributes`

```text
Description:
  List attributes for an entity

Usage:
  ppds metadata attributes <entity> [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -t, --type <type>                    Filter by attribute type (e.g., 'Lookup', 'String', 'DateTime', 'Picklist')
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata choice`

```text
Description:
  Manage global choices/option sets (deprecated - use 'optionset')

Usage:
  ppds metadata choice [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  create         Create a new global choice (option set)
  update         Update an existing global choice (option set)
  delete         Delete a global choice (option set)
  add-option     Add a new option value to an existing option set
  update-option  Update an existing option value in an option set
  remove-option  Remove an option value from an option set
  reorder        Reorder option values in an option set
```

## `ppds metadata column`

```text
Description:
  Create, update, or delete columns (deprecated - use 'attribute')

Usage:
  ppds metadata column [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  create  Create a new column (attribute) on a Dataverse table
  update  Update an existing column (attribute) on a Dataverse table
  delete  Delete a column (attribute) from a Dataverse table
```

## `ppds metadata entities`

```text
Description:
  List all entities with basic information

Usage:
  ppds metadata entities [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  --filter <filter>                    Filter by name. Without wildcards, matches names containing the text. Use * for patterns: 'foo*' (starts with), '*foo' (ends with)
  --custom-only                        Only show custom entities
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata entity`

```text
Description:
  Get full metadata for a specific entity, or create/update/delete entities and manage status reasons (see subcommands)

Usage:
  ppds metadata entity <entity> [command] [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  --include <include>                  Include specific metadata sections: attributes, relationships, keys, privileges (comma-separated or multiple flags)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information

Commands:
  create                        Create a new Dataverse table (entity)
  update <entity>               Update an existing Dataverse table (entity)
  delete <entity>               Delete a Dataverse table (entity)
  add-statusreason <entity>     Add a new status reason to an entity's statuscode attribute
  list-statusreasons <entity>   List all status reasons for an entity's statuscode attribute
  update-statusreason <entity>  Update an existing status reason on an entity
  remove-statusreason <entity>  Remove a status reason from an entity's statuscode attribute
```

## `ppds metadata key`

```text
Description:
  Create, delete, or reactivate alternate keys on Dataverse tables

Usage:
  ppds metadata key [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  create      Create an alternate key on a Dataverse table
  delete      Delete an alternate key from a Dataverse table
  reactivate  Reactivate a failed alternate key
```

## `ppds metadata keys`

```text
Description:
  List alternate keys for an entity

Usage:
  ppds metadata keys <entity> [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')

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

## `ppds metadata optionset`

```text
Description:
  Get details for or manage a global option set (choice)

Usage:
  ppds metadata optionset [<name>] [command] [options]

Arguments:
  <name>  The option set name (e.g., 'new_customstatus')

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information

Commands:
  create         Create a new global option set
  update         Update an existing global option set
  delete         Delete a global option set
  add-option     Add a new option value to an existing option set
  update-option  Update an existing option value in an option set
  remove-option  Remove an option value from an option set
  reorder        Reorder option values in an option set
```

## `ppds metadata optionsets`

```text
Description:
  List global option sets

Usage:
  ppds metadata optionsets [options]

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  --filter <filter>                    Filter by name. Without wildcards, matches names containing the text. Use * for patterns: 'foo*' (starts with), '*foo' (ends with)
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata publish`

```text
Description:
  Publish entity metadata (alias for ppds publish --type entity)

Usage:
  ppds metadata publish [<names>...] [options]

Arguments:
  <names>  Entity logical names to publish

Options:
  -s, --solution <solution>            Publish all entities in this solution
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata relationship`

```text
Description:
  Create, update, or delete Dataverse relationships

Usage:
  ppds metadata relationship [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  create  Create a new Dataverse relationship
  update  Update an existing Dataverse relationship
  delete  Delete a Dataverse relationship
```

## `ppds metadata relationships`

```text
Description:
  List relationships for an entity

Usage:
  ppds metadata relationships <entity> [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')

Options:
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -t, --type <type>                    Filter by relationship type: OneToMany, ManyToOne, ManyToMany
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata table`

```text
Description:
  Create, update, or delete Dataverse tables (deprecated - use 'entity')

Usage:
  ppds metadata table [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  create  Create a new Dataverse table (entity)
  update  Update an existing Dataverse table (entity)
  delete  Delete a Dataverse table (entity)
```

## `ppds metadata attribute add-option`

```text
Description:
  Add an option to a column's local option set

Usage:
  ppds metadata attribute add-option [options]

Options:
  -s, --solution <solution>            Solution unique name (required for value derivation when --option has no explicit value)
  -e, --entity <entity>                [Required] Logical name of the entity
  -c, --column <column>                [Required] Logical name of the Choice/Choices column
  --option <option>                    [Required] Option to add: "Label[:Value][:#Color]"
  --publish                            Publish the entity after the change
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata attribute create`

```text
Description:
  Create a new attribute on a Dataverse table (for Choice/Choices columns use --option to define a local option set, or --choice to attach a global one)

Usage:
  ppds metadata attribute create [options]

Options:
  -s, --solution <solution>                                                                                   [Required] Solution unique name containing the table
  -e, --entity <entity>                                                                                       [Required] Logical name of the entity to add the attribute to
  --name <name>                                                                                               [Required] Schema name for the new attribute (e.g., new_MyColumn)
  --display-name <display-name>                                                                               [Required] Display name of the attribute
  --type <BigInt|Boolean|Choice|Choices|DateTime|Decimal|Double|File|Image|Integer|Lookup|Memo|Money|String>  [Required] Column type: String, Memo, Integer, BigInt, Decimal, Double, Money, Boolean, DateTime, Choice, Choices, Image, File, Lookup
  --description <description>                                                                                 Description of the attribute
  --required-level <required-level>                                                                           Requirement level: None, Recommended, or Required
  --max-length <max-length>                                                                                   Maximum length for String/Memo columns
  --min-value <min-value>                                                                                     Minimum value for numeric columns
  --max-value <max-value>                                                                                     Maximum value for numeric columns
  --precision <precision>                                                                                     Precision for Decimal, Double, and Money columns
  --format <format>                                                                                           Format for String, Integer, or DateTime columns
  --date-time-behavior <date-time-behavior>                                                                   DateTime behavior: UserLocal, DateOnly, or TimeZoneIndependent
  --choice <choice>                                                                                           Attach the Choice/Choices column to an existing GLOBAL option set by name (mutually exclusive with --option/--options/--options-file)
  --options <options>                                                                                         [Legacy] Local Choice options as CSV: "Label1=1,Label2=2"
  --option <option>                                                                                           Local Choice option "Label[:Value][:#Color]" - repeatable; value derived from --solution when omitted
  --options-file <options-file>                                                                               Path to a JSON file of local Choice options: [{"label":"..","value":1,"color":"#RRGGBB"}]
  --default-value <default-value>                                                                             Default value for Choice or Boolean columns
  --true-label <true-label>                                                                                   Label for the true value of a Boolean column
  --false-label <false-label>                                                                                 Label for the false value of a Boolean column
  --max-size-kb <max-size-kb>                                                                                 Maximum file size in KB for Image/File columns
  --dry-run                                                                                                   Validate only, do not persist changes
  --publish                                                                                                   Publish the entity after the attribute is created
  -p, --profile <profile>                                                                                     Authentication profile name
  -env, --environment <environment>                                                                           Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                                                                                                 Show only warnings and errors
  -v, --verbose                                                                                               Show detailed output including debug messages
  --debug                                                                                                     Show trace-level diagnostic output
  --correlation-id <correlation-id>                                                                           Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>                                                                         Output format [default: Text]
  -?, -h, --help                                                                                              Show help and usage information
```

## `ppds metadata attribute delete`

```text
Description:
  Delete an attribute from a Dataverse table

Usage:
  ppds metadata attribute delete [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                [Required] Logical name of the entity containing the attribute
  -c, --column <column>                [Required] Logical name of the attribute to delete
  --force                              Skip confirmation prompt
  --dry-run                            Show dependencies without deleting
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata attribute remove-option`

```text
Description:
  Remove an option from a column's local option set

Usage:
  ppds metadata attribute remove-option [options]

Options:
  -s, --solution <solution>            Solution unique name
  -e, --entity <entity>                [Required] Logical name of the entity
  -c, --column <column>                [Required] Logical name of the Choice/Choices column
  --value <value>                      Target option by value (mutually exclusive with --label)
  --label <label>                      Target option by label (mutually exclusive with --value)
  --force                              Skip confirmation prompt
  --publish                            Publish the entity after the change
  --dry-run                            Validate that the target option exists, without removing it
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata attribute update`

```text
Description:
  Update an existing attribute on a Dataverse table

Usage:
  ppds metadata attribute update [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                [Required] Logical name of the entity containing the attribute
  -c, --column <column>                [Required] Logical name of the attribute to update
  --display-name <display-name>        Updated display name
  --description <description>          Updated description
  --required-level <required-level>    Updated requirement level: None, Recommended, or Required
  --max-length <max-length>            Updated maximum length
  --dry-run                            Validate only, do not persist changes
  --publish                            Publish the entity after the change
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata attribute update-option`

```text
Description:
  Update an option (label/color) on a column's local option set

Usage:
  ppds metadata attribute update-option [options]

Options:
  -s, --solution <solution>            Solution unique name
  -e, --entity <entity>                [Required] Logical name of the entity
  -c, --column <column>                [Required] Logical name of the Choice/Choices column
  --value <value>                      Target option by value (mutually exclusive with --label)
  --label <label>                      Target option by current label (mutually exclusive with --value)
  --new-label <new-label>              New label to apply
  --color <color>                      New hex color (e.g. #FF0000)
  --publish                            Publish the entity after the change
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata choice add-option`

```text
Description:
  Add a new option value to an existing option set

Usage:
  ppds metadata choice add-option [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the option set
  --name <name>                        [Required] Name of the option set
  --label <label>                      [Required] Label for the new option
  --value <value>                      Numeric value for the option (auto-assigned if not specified)
  --color <color>                      Color for the option (hex string, e.g., #FF0000)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata choice create`

```text
Description:
  Create a new global choice (option set)

Usage:
  ppds metadata choice create [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name to add the choice to
  --name <name>                        [Required] Schema name for the global choice
  --display-name <display-name>        [Required] Display name of the global choice
  --options <options>                  [Required] Option definitions: "Label1=1,Label2=2"
  --description <description>          Description of the global choice
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata choice delete`

```text
Description:
  Delete a global choice (option set)

Usage:
  ppds metadata choice delete [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the global choice
  --name <name>                        [Required] Name of the global choice to delete
  --force                              Skip confirmation prompt
  --dry-run                            Show dependencies without deleting
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata choice remove-option`

```text
Description:
  Remove an option value from an option set

Usage:
  ppds metadata choice remove-option [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the option set
  --name <name>                        [Required] Name of the option set
  --value <value>                      [Required] Numeric value of the option to remove
  --force                              Skip confirmation prompt
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata choice reorder`

```text
Description:
  Reorder option values in an option set

Usage:
  ppds metadata choice reorder [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the option set
  --name <name>                        [Required] Name of the option set
  --order <order>                      [Required] Comma-separated list of option values in the desired order: "1,3,2,4"
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata choice update`

```text
Description:
  Update an existing global choice (option set)

Usage:
  ppds metadata choice update [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the global choice
  --name <name>                        [Required] Name of the global choice to update
  --display-name <display-name>        Updated display name
  --description <description>          Updated description
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata choice update-option`

```text
Description:
  Update an existing option value in an option set

Usage:
  ppds metadata choice update-option [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the option set
  --name <name>                        [Required] Name of the option set
  --value <value>                      [Required] Numeric value of the option to update
  --label <label>                      [Required] New label for the option
  --color <color>                      New color for the option (hex string, e.g., #FF0000)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata column create`

```text
Description:
  Create a new column (attribute) on a Dataverse table

Usage:
  ppds metadata column create [options]

Options:
  -s, --solution <solution>                                                                                   [Required] Solution unique name containing the table
  -e, --entity <entity>                                                                                       [Required] Logical name of the entity to add the column to
  --name <name>                                                                                               [Required] Schema name for the new column (e.g., new_MyColumn)
  --display-name <display-name>                                                                               [Required] Display name of the column
  --type <BigInt|Boolean|Choice|Choices|DateTime|Decimal|Double|File|Image|Integer|Lookup|Memo|Money|String>  [Required] Column type: String, Memo, Integer, BigInt, Decimal, Double, Money, Boolean, DateTime, Choice, Choices, Image, File, Lookup
  --description <description>                                                                                 Description of the column
  --required-level <required-level>                                                                           Requirement level: None, Recommended, or Required
  --max-length <max-length>                                                                                   Maximum length for String/Memo columns
  --min-value <min-value>                                                                                     Minimum value for numeric columns
  --max-value <max-value>                                                                                     Maximum value for numeric columns
  --precision <precision>                                                                                     Precision for Decimal, Double, and Money columns
  --format <format>                                                                                           Format for String, Integer, or DateTime columns
  --date-time-behavior <date-time-behavior>                                                                   DateTime behavior: UserLocal, DateOnly, or TimeZoneIndependent
  --option-set-name <option-set-name>                                                                         Name of an existing global option set for Choice/Choices columns
  --options <options>                                                                                         Option definitions for Choice/Choices columns: "Label1=1,Label2=2"
  --default-value <default-value>                                                                             Default value for Choice or Boolean columns
  --true-label <true-label>                                                                                   Label for the true value of a Boolean column
  --false-label <false-label>                                                                                 Label for the false value of a Boolean column
  --max-size-kb <max-size-kb>                                                                                 Maximum file size in KB for Image/File columns
  --dry-run                                                                                                   Validate only, do not persist changes
  -p, --profile <profile>                                                                                     Authentication profile name
  -env, --environment <environment>                                                                           Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                                                                                                 Show only warnings and errors
  -v, --verbose                                                                                               Show detailed output including debug messages
  --debug                                                                                                     Show trace-level diagnostic output
  --correlation-id <correlation-id>                                                                           Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>                                                                         Output format [default: Text]
  -?, -h, --help                                                                                              Show help and usage information
```

## `ppds metadata column delete`

```text
Description:
  Delete a column (attribute) from a Dataverse table

Usage:
  ppds metadata column delete [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                [Required] Logical name of the entity containing the column
  -c, --column <column>                [Required] Logical name of the column to delete
  --force                              Skip confirmation prompt
  --dry-run                            Show dependencies without deleting
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata column update`

```text
Description:
  Update an existing column (attribute) on a Dataverse table

Usage:
  ppds metadata column update [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                [Required] Logical name of the entity containing the column
  -c, --column <column>                [Required] Logical name of the column to update
  --display-name <display-name>        Updated display name
  --description <description>          Updated description
  --required-level <required-level>    Updated requirement level: None, Recommended, or Required
  --max-length <max-length>            Updated maximum length
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata entity add-statusreason`

```text
Description:
  Add a new status reason to an entity's statuscode attribute

Usage:
  ppds metadata entity <entity> add-statusreason [<entity>] [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')
  <entity>  Logical name of the entity (alternative to --entity)

Options:
  -e, --entity <entity>                Logical name of the entity (alternative to the positional <entity>)
  --label <label>                      [Required] Display label for the new status reason
  --value <value>                      Explicit option value (mutually exclusive with --solution for derivation)
  -s, --solution <solution>            [Required when --value is omitted] Solution unique name; publisher prefix x 10,000 is used to derive the option value
  --state <Active|Inactive>            State the reason belongs to: Active or Inactive (use this OR --state-code, not both)
  --state-code <state-code>            State code directly: 0 (Active) or 1 (Inactive) (use this OR --state, not both)
  --color <color>                      Hex color for the status reason (e.g., #FF0000)
  --publish                            Publish the entity after the change
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata entity create`

```text
Description:
  Create a new Dataverse table (entity)

Usage:
  ppds metadata entity <entity> create [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')

Options:
  -s, --solution <solution>                  [Required] Solution unique name to add the table to
  --name <name>                              [Required] Schema name for the new table (e.g., new_MyTable)
  --display-name <display-name>              [Required] Display name of the table
  --plural-name <plural-name>                [Required] Plural display name of the table
  --ownership <OrganizationOwned|UserOwned>  [Required] Ownership type: UserOwned or OrganizationOwned
  --description <description>                Description of the table
  --dry-run                                  Validate only, do not persist changes
  --publish                                  Publish the entity after it is created
  -p, --profile <profile>                    Authentication profile name
  -env, --environment <environment>          Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                                Show only warnings and errors
  -v, --verbose                              Show detailed output including debug messages
  --debug                                    Show trace-level diagnostic output
  --correlation-id <correlation-id>          Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>        Output format [default: Text]
  -?, -h, --help                             Show help and usage information
```

## `ppds metadata entity delete`

```text
Description:
  Delete a Dataverse table (entity)

Usage:
  ppds metadata entity <entity> delete [<entity>] [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')
  <entity>  Logical name of the entity (alternative to --entity)

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                Logical name of the entity (alternative to the positional <entity>)
  --force                              Skip confirmation prompt
  --dry-run                            Show dependencies without deleting
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata entity list-statusreasons`

```text
Description:
  List all status reasons for an entity's statuscode attribute

Usage:
  ppds metadata entity <entity> list-statusreasons [<entity>] [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')
  <entity>  Logical name of the entity (alternative to --entity)

Options:
  -e, --entity <entity>                Logical name of the entity (alternative to the positional <entity>)
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata entity remove-statusreason`

```text
Description:
  Remove a status reason from an entity's statuscode attribute

Usage:
  ppds metadata entity <entity> remove-statusreason [<entity>] [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')
  <entity>  Logical name of the entity (alternative to --entity)

Options:
  -e, --entity <entity>                Logical name of the entity (alternative to the positional <entity>)
  --value <value>                      Target status reason by option value (mutually exclusive with --label)
  --label <label>                      Target status reason by label (mutually exclusive with --value)
  -s, --solution <solution>            Solution unique name
  --force                              Skip confirmation prompt
  --publish                            Publish the entity after the change
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata entity update`

```text
Description:
  Update an existing Dataverse table (entity)

Usage:
  ppds metadata entity <entity> update [<entity>] [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')
  <entity>  Logical name of the entity (alternative to --entity)

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                Logical name of the entity (alternative to the positional <entity>)
  --display-name <display-name>        Updated display name
  --plural-name <plural-name>          Updated plural display name
  --description <description>          Updated description
  --icon-small <icon-small>            16x16 icon: web resource logical name (e.g. new_icons/myentity16.png). Use empty string to clear.
  --icon-medium <icon-medium>          32x32 icon: web resource logical name. Use empty string to clear.
  --icon-vector <icon-vector>          SVG vector icon: web resource logical name (primary icon in modern Dataverse). Use empty string to clear.
  --dry-run                            Validate only, do not persist changes
  --publish                            Publish the entity after the change
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata entity update-statusreason`

```text
Description:
  Update an existing status reason on an entity

Usage:
  ppds metadata entity <entity> update-statusreason [<entity>] [options]

Arguments:
  <entity>  The entity logical name (e.g., 'account')
  <entity>  Logical name of the entity (alternative to --entity)

Options:
  -e, --entity <entity>                Logical name of the entity (alternative to the positional <entity>)
  --value <value>                      Target status reason by option value (mutually exclusive with --label)
  --label <label>                      Target status reason by current label (mutually exclusive with --value)
  --new-label <new-label>              New label to apply to the status reason
  --color <color>                      New hex color for the status reason (e.g., #FF0000)
  -s, --solution <solution>            Solution unique name
  --publish                            Publish the entity after the change
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata key create`

```text
Description:
  Create an alternate key on a Dataverse table

Usage:
  ppds metadata key create [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                [Required] Logical name of the entity to add the key to
  --name <name>                        [Required] Schema name for the alternate key
  --display-name <display-name>        [Required] Display name of the alternate key
  --attributes <attributes>            [Required] Comma-separated list of attribute logical names: "attr1,attr2"
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata key delete`

```text
Description:
  Delete an alternate key from a Dataverse table

Usage:
  ppds metadata key delete [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                [Required] Logical name of the entity containing the key
  --name <name>                        [Required] Logical name of the key to delete
  --force                              Skip confirmation prompt
  --dry-run                            Show dependencies without deleting
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata key reactivate`

```text
Description:
  Reactivate a failed alternate key

Usage:
  ppds metadata key reactivate [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                [Required] Logical name of the entity containing the key
  --name <name>                        [Required] Logical name of the key to reactivate
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata optionset add-option`

```text
Description:
  Add a new option value to an existing option set

Usage:
  ppds metadata optionset [<name>] add-option [options]

Arguments:
  <name>  The option set name (e.g., 'new_customstatus')

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the option set
  --name <name>                        [Required] Name of the option set
  --label <label>                      [Required] Label for the new option
  --value <value>                      Numeric value for the option (auto-assigned if not specified)
  --color <color>                      Color for the option (hex string, e.g., #FF0000)
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata optionset create`

```text
Description:
  Create a new global option set

Usage:
  ppds metadata optionset [<name>] create [options]

Arguments:
  <name>  The option set name (e.g., 'new_customstatus')

Options:
  -s, --solution <solution>            [Required] Solution unique name to add the option set to
  --name <name>                        [Required] Schema name for the global option set
  --display-name <display-name>        [Required] Display name of the global option set
  --options <options>                  [Required] Option definitions: "Label1=1,Label2=2"
  --description <description>          Description of the global option set
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata optionset delete`

```text
Description:
  Delete a global option set

Usage:
  ppds metadata optionset [<name>] delete [options]

Arguments:
  <name>  The option set name (e.g., 'new_customstatus')

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the global option set
  --name <name>                        [Required] Name of the global option set to delete
  --force                              Skip confirmation prompt
  --dry-run                            Show dependencies without deleting
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata optionset remove-option`

```text
Description:
  Remove an option value from an option set

Usage:
  ppds metadata optionset [<name>] remove-option [options]

Arguments:
  <name>  The option set name (e.g., 'new_customstatus')

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the option set
  --name <name>                        [Required] Name of the option set
  --value <value>                      Target option by value (mutually exclusive with --label)
  --label <label>                      Target option by label (mutually exclusive with --value)
  --force                              Skip confirmation prompt
  --dry-run                            Validate that the target option exists, without removing it
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata optionset reorder`

```text
Description:
  Reorder option values in an option set

Usage:
  ppds metadata optionset [<name>] reorder [options]

Arguments:
  <name>  The option set name (e.g., 'new_customstatus')

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the option set
  --name <name>                        [Required] Name of the option set
  --order <order>                      [Required] Comma-separated list of option values in the desired order: "1,3,2,4"
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata optionset update`

```text
Description:
  Update an existing global option set

Usage:
  ppds metadata optionset [<name>] update [options]

Arguments:
  <name>  The option set name (e.g., 'new_customstatus')

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the global option set
  --name <name>                        [Required] Name of the global option set to update
  --display-name <display-name>        Updated display name
  --description <description>          Updated description
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata optionset update-option`

```text
Description:
  Update an existing option value in an option set

Usage:
  ppds metadata optionset [<name>] update-option [options]

Arguments:
  <name>  The option set name (e.g., 'new_customstatus')

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the option set
  --name <name>                        [Required] Name of the option set
  --value <value>                      Target option by value (mutually exclusive with --label)
  --label <label>                      Target option by current label (mutually exclusive with --value)
  --new-label <new-label>              New label to apply
  --color <color>                      New hex color (e.g. #FF0000)
  --dry-run                            Validate only, do not persist changes
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata relationship create`

```text
Description:
  Create a new Dataverse relationship

Usage:
  ppds metadata relationship create [options]

Options:
  -s, --solution <solution>                                                  [Required] Solution unique name to add the relationship to
  --from <from>                                                              [Required] Source entity logical name (referenced/parent for 1:N, entity1 for N:N)
  --to <to>                                                                  [Required] Target entity logical name (referencing/child for 1:N, entity2 for N:N)
  --type <many-to-many|one-to-many>                                          [Required] Relationship type: one-to-many or many-to-many
  --name <name>                                                              [Required] Schema name for the relationship
  --lookup-name <lookup-name>                                                Schema name of the lookup column (one-to-many only)
  --lookup-display-name <lookup-display-name>                                Display name of the lookup column (one-to-many only)
  --intersect-entity <intersect-entity>                                      Schema name of the intersect entity (many-to-many only). Defaults to --name.
  --cascade-delete <Active|Cascade|NoCascade|RemoveLink|Restrict|UserOwned>  Cascade behavior for delete: Cascade, Active, NoCascade, RemoveLink, Restrict
  --cascade-assign <Active|Cascade|NoCascade|RemoveLink|Restrict|UserOwned>  Cascade behavior for assign: Cascade, Active, NoCascade, UserOwned
  --dry-run                                                                  Validate only, do not persist changes
  -p, --profile <profile>                                                    Authentication profile name
  -env, --environment <environment>                                          Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                                                                Show only warnings and errors
  -v, --verbose                                                              Show detailed output including debug messages
  --debug                                                                    Show trace-level diagnostic output
  --correlation-id <correlation-id>                                          Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>                                        Output format [default: Text]
  -?, -h, --help                                                             Show help and usage information
```

## `ppds metadata relationship delete`

```text
Description:
  Delete a Dataverse relationship

Usage:
  ppds metadata relationship delete [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the relationship
  --name <name>                        [Required] Schema name of the relationship to delete
  --force                              Skip confirmation prompt
  --dry-run                            Show dependencies without deleting
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata relationship update`

```text
Description:
  Update an existing Dataverse relationship

Usage:
  ppds metadata relationship update [options]

Options:
  -s, --solution <solution>                                                    [Required] Solution unique name containing the relationship
  --name <name>                                                                [Required] Schema name of the relationship to update
  --cascade-delete <Active|Cascade|NoCascade|RemoveLink|Restrict|UserOwned>    Updated cascade behavior for delete
  --cascade-assign <Active|Cascade|NoCascade|RemoveLink|Restrict|UserOwned>    Updated cascade behavior for assign
  --cascade-merge <Active|Cascade|NoCascade|RemoveLink|Restrict|UserOwned>     Updated cascade behavior for merge
  --cascade-reparent <Active|Cascade|NoCascade|RemoveLink|Restrict|UserOwned>  Updated cascade behavior for reparent
  --cascade-share <Active|Cascade|NoCascade|RemoveLink|Restrict|UserOwned>     Updated cascade behavior for share
  --cascade-unshare <Active|Cascade|NoCascade|RemoveLink|Restrict|UserOwned>   Updated cascade behavior for unshare
  --dry-run                                                                    Validate only, do not persist changes
  -p, --profile <profile>                                                      Authentication profile name
  -env, --environment <environment>                                            Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                                                                  Show only warnings and errors
  -v, --verbose                                                                Show detailed output including debug messages
  --debug                                                                      Show trace-level diagnostic output
  --correlation-id <correlation-id>                                            Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>                                          Output format [default: Text]
  -?, -h, --help                                                               Show help and usage information
```

## `ppds metadata table create`

```text
Description:
  Create a new Dataverse table (entity)

Usage:
  ppds metadata table create [options]

Options:
  -s, --solution <solution>                  [Required] Solution unique name to add the table to
  --name <name>                              [Required] Schema name for the new table (e.g., new_MyTable)
  --display-name <display-name>              [Required] Display name of the table
  --plural-name <plural-name>                [Required] Plural display name of the table
  --ownership <OrganizationOwned|UserOwned>  [Required] Ownership type: UserOwned or OrganizationOwned
  --description <description>                Description of the table
  --dry-run                                  Validate only, do not persist changes
  --publish                                  Publish the entity after it is created
  -p, --profile <profile>                    Authentication profile name
  -env, --environment <environment>          Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                                Show only warnings and errors
  -v, --verbose                              Show detailed output including debug messages
  --debug                                    Show trace-level diagnostic output
  --correlation-id <correlation-id>          Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>        Output format [default: Text]
  -?, -h, --help                             Show help and usage information
```

## `ppds metadata table delete`

```text
Description:
  Delete a Dataverse table (entity)

Usage:
  ppds metadata table delete [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                [Required] Logical name of the entity to delete
  --force                              Skip confirmation prompt
  --dry-run                            Show dependencies without deleting
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds metadata table update`

```text
Description:
  Update an existing Dataverse table (entity)

Usage:
  ppds metadata table update [options]

Options:
  -s, --solution <solution>            [Required] Solution unique name containing the table
  -e, --entity <entity>                [Required] Logical name of the entity to update
  --display-name <display-name>        Updated display name
  --plural-name <plural-name>          Updated plural display name
  --description <description>          Updated description
  --icon-small <icon-small>            16x16 icon: web resource logical name. Use empty string to clear.
  --icon-medium <icon-medium>          32x32 icon: web resource logical name. Use empty string to clear.
  --icon-vector <icon-vector>          SVG vector icon: web resource logical name. Use empty string to clear.
  --dry-run                            Validate only, do not persist changes
  --publish                            Publish the entity after the change
  -p, --profile <profile>              Authentication profile name
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

