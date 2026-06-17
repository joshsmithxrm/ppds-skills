# `ppds data` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds data`

```text
Description:
  Data operations: export, import, copy, analyze, schema, users, load, update, delete, truncate

Usage:
  ppds data [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  export    Export data from Dataverse to a ZIP file
  import    Import data from a ZIP file into Dataverse
  copy      Copy data from source to target Dataverse environment
  analyze   Analyze schema and display dependency graph
  schema    Generate a migration schema from Dataverse metadata
  users     Generate user mapping file from source to target environment
  load      Load CSV data into a Dataverse entity
  update    Update records in a Dataverse entity (fails if record doesn't exist)
  delete    Delete records from a Dataverse entity
  truncate  Delete ALL records from an entity (DANGEROUS - use with caution)
```

## `ppds data analyze`

```text
Description:
  Analyze schema and display dependency graph

Usage:
  ppds data analyze [options]

Options:
  -s, --schema <schema>                [Required] Path to schema.xml file
  -f, --output-format <Csv|Json|Text>  Output format: text or json [default: Text]
  -v, --verbose                        Enable verbose logging output
  --debug                              Enable diagnostic logging output
  -?, -h, --help                       Show help and usage information
```

## `ppds data copy`

```text
Description:
  Copy data from source to target Dataverse environment

Usage:
  ppds data copy [options]

Options:
  -s, --schema <schema>                   [Required] Path to schema.xml file
  -sp, --source-profile <source-profile>  Authentication profile for source environment (defaults to active profile)
  -tp, --target-profile <target-profile>  Authentication profile(s) for target environment - comma-separated for parallel imports (defaults to active profile)
  -se, --source-env <source-env>          [Required] Source environment - accepts URL, friendly name, unique name, or ID
  -te, --target-env <target-env>          [Required] Target environment - accepts URL, friendly name, unique name, or ID
  --temp-dir <temp-dir>                   Temporary directory for intermediate data file (default: system temp)
  --parallel <parallel>                   Maximum concurrent entity exports (only applies when schema contains multiple entities) [default: 64]
  --batch-size <batch-size>               Records per API request (all records are exported; this controls request size) [default: 5000]
  --bypass-plugins <all|async|sync>       Bypass custom plugin execution on target: sync, async, or all (requires prvBypassCustomBusinessLogic privilege)
  --bypass-flows                          Bypass Power Automate flow triggers on target (no special privilege required)
  --skip-missing-columns                  Skip columns that exist in source but not in target environment (prevents schema mismatch errors)
  --continue-on-error                     Continue import on individual record failures
  --strip-owner-fields                    Strip ownership fields (ownerid, createdby, modifiedby) allowing Dataverse to assign current user
  -u, --user-mapping <user-mapping>       Path to user mapping XML file for remapping user references
  -f, --output-format <Csv|Json|Text>     Output format [default: Text]
  -v, --verbose                           Enable verbose logging output
  --debug                                 Enable diagnostic logging output
  -?, -h, --help                          Show help and usage information
```

## `ppds data delete`

```text
Description:
  Delete records from a Dataverse entity

Usage:
  ppds data delete [options]

Options:
  -e, --entity <entity>                [Required] Target entity logical name
  --id <id>                            Record ID (GUID) to delete
  -k, --key <key>                      Alternate key field(s) for lookup. Format: field=value or field1=value1,field2=value2 for composite keys.
  --file <file>                        Path to file containing record IDs (JSON array or CSV with ID column)
  --id-column <id-column>              Column name containing record IDs in CSV file (default: entity primary key)
  --filter <filter>                    SQL-like filter expression to match records for deletion (e.g., "name like '%test%'")
  --force                              Skip confirmation prompt (required for non-interactive execution)
  --dry-run                            Preview records that would be deleted without actually deleting
  --limit <limit>                      Maximum number of records to delete (fails if query returns more)
  --batch-size <batch-size>            Records per batch (default: 100) [default: 100]
  --bypass-plugins <all|async|sync>    Bypass custom plugin execution: sync, async, or all (requires prvBypassCustomBusinessLogic privilege)
  --bypass-flows                       Bypass Power Automate flow triggers
  --continue-on-error                  Continue deleting on individual record failures
  -p, --profile <profile>              Profile name(s). For high-throughput pooling, specify multiple Application User profiles comma-separated (e.g., app1,app2,app3) - each profile multiplies API quota.
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds data export`

```text
Description:
  Export data from Dataverse to a ZIP file

Usage:
  ppds data export [options]

Options:
  -s, --schema <schema>                                [Required] Path to schema.xml file
  -o, --output <output>                                [Required] Output ZIP file path
  -p, --profile <profile>                              Profile name(s). For high-throughput pooling, specify multiple Application User profiles comma-separated (e.g., app1,app2,app3) - each profile multiplies API quota.
  -env, --environment <environment>                    Override the environment URL. Takes precedence over profile's bound environment.
  --parallel <parallel>                                Maximum concurrent entity exports (only applies when schema contains multiple entities) [default: 64]
  --batch-size <batch-size>                            Records per API request (all records are exported; this controls request size) [default: 5000]
  --page-parallel <page-parallel>                      Partitions per entity for page-level parallelism (0=auto, 1=disabled) [default: 0]
  --page-parallel-threshold <page-parallel-threshold>  Minimum records before page-level parallelism activates [default: 5000]
  -f, --output-format <Csv|Json|Text>                  Output format [default: Text]
  --format <Cmt|Json>                                  Data export format: cmt (CMT-compatible XML ZIP) or json (PPDS-native JSON) [default: Cmt]
  -v, --verbose                                        Enable verbose logging output
  --debug                                              Enable diagnostic logging output
  -?, -h, --help                                       Show help and usage information
```

## `ppds data import`

```text
Description:
  Import data from a ZIP file into Dataverse

Usage:
  ppds data import [options]

Options:
  -d, --data <data>                       [Required] Path to data.zip file
  -p, --profile <profile>                 Profile name(s). For high-throughput pooling, specify multiple Application User profiles comma-separated (e.g., app1,app2,app3) - each profile multiplies API quota.
  -env, --environment <environment>       Override the environment URL. Takes precedence over profile's bound environment.
  --bypass-plugins <all|async|sync>       Bypass custom plugin execution: sync, async, or all (requires prvBypassCustomBusinessLogic privilege)
  --bypass-flows                          Bypass Power Automate flow triggers (no special privilege required)
  --continue-on-error                     Continue import on individual record failures
  -m, --mode <Create|Skip|Update|Upsert>  Import mode: Create, Update, or Upsert [default: Upsert]
  -u, --user-mapping <user-mapping>       Path to user mapping XML file for remapping user references
  --strip-owner-fields                    Strip ownership fields (ownerid, createdby, modifiedby) allowing Dataverse to assign current user
  --skip-missing-columns                  Skip columns that exist in exported data but not in target environment (prevents schema mismatch errors)
  --resolve-lookups                       Enable external lookup resolution (ID check, then name-based query)
  --skip-unresolved-lookups               Null unresolved lookups instead of failing the record [default: True] (requires --resolve-lookups)
  --impersonate-owners                    Preserve record ownership via CallerAADObjectId impersonation (requires --user-mapping)
  -f, --output-format <Csv|Json|Text>     Output format [default: Text]
  -v, --verbose                           Enable verbose logging output
  --debug                                 Enable diagnostic logging output
  --error-report <error-report>           Base path for output files (creates .errors.jsonl, .progress.log, .summary.json). Errors are streamed in real-time.
  -?, -h, --help                          Show help and usage information
```

## `ppds data load`

```text
Description:
  Load CSV data into a Dataverse entity

Usage:
  ppds data load [options]

Options:
  -e, --entity <entity>                  [Required] Target entity logical name
  -f, --file <file>                      [Required] Path to CSV file
  -k, --key <key>                        Alternate key field(s) for upsert. Comma-separated for composite keys.
  -m, --mapping <mapping>                Path to column mapping JSON file
  --generate-mapping <generate-mapping>  Generate mapping template to specified file
  --dry-run                              Validate without writing to Dataverse
  --batch-size <batch-size>              Records per batch (default: 100) [default: 100]
  --bypass-plugins <all|async|sync>      Bypass custom plugin execution: sync, async, or all (requires prvBypassCustomBusinessLogic privilege)
  --bypass-flows                         Bypass Power Automate flow triggers
  --continue-on-error                    Continue loading on individual record failures
  --force                                Force loading even when auto-mapping is incomplete (unmatched columns will be skipped)
  --analyze                              Analyze mapping without loading data (preview which columns match)
  -p, --profile <profile>                Profile name(s). For high-throughput pooling, specify multiple Application User profiles comma-separated (e.g., app1,app2,app3) - each profile multiplies API quota.
  -env, --environment <environment>      Override the environment URL. Takes precedence over profile's bound environment.
  -o, --output-format <Csv|Json|Text>    Output format [default: Text]
  -v, --verbose                          Enable verbose logging output
  --debug                                Enable diagnostic logging output
  -?, -h, --help                         Show help and usage information
```

## `ppds data schema`

```text
Description:
  Generate a migration schema from Dataverse metadata

Usage:
  ppds data schema [options]

Options:
  -e, --entities <entities>                      [Required] Entity logical names to include (comma-separated or multiple -e flags)
  -o, --output <output>                          [Required] Output schema file path
  -p, --profile <profile>                        Profile name(s). For high-throughput pooling, specify multiple Application User profiles comma-separated (e.g., app1,app2,app3) - each profile multiplies API quota.
  -env, --environment <environment>              Override the environment URL. Takes precedence over profile's bound environment.
  --include-audit-fields                         Include audit fields (createdon, createdby, modifiedon, modifiedby, overriddencreatedon)
  --disable-plugins                              Set disableplugins=true on all entities
  -a, --include-attributes <include-attributes>  Only include these attributes (whitelist, comma-separated or multiple flags)
  --exclude-attributes <exclude-attributes>      Exclude these attributes (blacklist, comma-separated)
  --filter <filter>                              SQL-like filter per entity. Format: entity:expression (e.g., "account:statecode = 0"). Repeatable.
  -f, --output-format <Csv|Json|Text>            Output format [default: Text]
  -v, --verbose                                  Enable verbose logging output
  --debug                                        Enable diagnostic logging output
  -?, -h, --help                                 Show help and usage information
```

## `ppds data truncate`

```text
Description:
  Delete ALL records from an entity (DANGEROUS - use with caution)

Usage:
  ppds data truncate [options]

Options:
  -e, --entity <entity>                [Required] Entity logical name to truncate (delete ALL records)
  --dry-run                            Preview record count without deleting
  --force                              Skip confirmation prompt (required for non-interactive execution)
  --batch-size <batch-size>            Records per delete batch (default: 1000) [default: 1000]
  --bypass-plugins <all|async|sync>    Bypass custom plugin execution: sync, async, or all (requires prvBypassCustomBusinessLogic privilege)
  --bypass-flows                       Bypass Power Automate flow triggers
  --continue-on-error                  Continue deleting on individual record failures
  -p, --profile <profile>              Profile name(s). For high-throughput pooling, specify multiple Application User profiles comma-separated (e.g., app1,app2,app3) - each profile multiplies API quota.
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds data update`

```text
Description:
  Update records in a Dataverse entity (fails if record doesn't exist)

Usage:
  ppds data update [options]

Options:
  -e, --entity <entity>                [Required] Target entity logical name
  --id <id>                            Record ID (GUID) to update
  -k, --key <key>                      Alternate key field(s) for lookup. Format: field=value or field1=value1,field2=value2 for composite keys.
  --file <file>                        Path to CSV file containing records to update (must include ID column and columns to update)
  --id-column <id-column>              Column name containing record IDs in CSV file (default: entity primary key)
  --filter <filter>                    SQL-like filter expression to match records for update (e.g., "statecode eq 0")
  -s, --set <set>                      Field values to set. Format: field=value or field1=value1,field2=value2. Required for --id, --key, or --filter modes.
  -m, --mapping <mapping>              Path to column mapping JSON file (for --file mode)
  --force                              Skip confirmation prompt (required for non-interactive execution)
  --dry-run                            Preview records that would be updated without actually updating
  --limit <limit>                      Maximum number of records to update (fails if query returns more)
  --batch-size <batch-size>            Records per batch (default: 100) [default: 100]
  --bypass-plugins <all|async|sync>    Bypass custom plugin execution: sync, async, or all (requires prvBypassCustomBusinessLogic privilege)
  --bypass-flows                       Bypass Power Automate flow triggers
  --continue-on-error                  Continue updating on individual record failures
  -p, --profile <profile>              Profile name(s). For high-throughput pooling, specify multiple Application User profiles comma-separated (e.g., app1,app2,app3) - each profile multiplies API quota.
  -env, --environment <environment>    Override the environment URL. Takes precedence over profile's bound environment.
  -q, --quiet                          Show only warnings and errors
  -v, --verbose                        Show detailed output including debug messages
  --debug                              Show trace-level diagnostic output
  --correlation-id <correlation-id>    Correlation ID for distributed tracing
  -f, --output-format <Csv|Json|Text>  Output format [default: Text]
  -?, -h, --help                       Show help and usage information
```

## `ppds data users`

```text
Description:
  Generate user mapping file from source to target environment

Usage:
  ppds data users [options]

Options:
  -sp, --source-profile <source-profile>  Authentication profile for source environment (defaults to active profile)
  -tp, --target-profile <target-profile>  Authentication profile for target environment (defaults to active profile)
  -se, --source-env <source-env>          [Required] Source environment - accepts URL, friendly name, unique name, or ID
  -te, --target-env <target-env>          [Required] Target environment - accepts URL, friendly name, unique name, or ID
  -o, --output <output>                   [Required] Output user mapping XML file path
  --analyze                               Analyze user differences without generating mapping file
  -f, --output-format <Csv|Json|Text>     Output format [default: Text]
  -v, --verbose                           Enable verbose logging output
  --debug                                 Enable diagnostic logging output
  -?, -h, --help                          Show help and usage information
```

