# `ppds-mcp-server` — tool reference

<!-- GENERATED from a live tools/list call against ppds-mcp-server 1.0.0.0. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_mcp_tools.py && python tools/generate_flag_tables.py -->

Captured from the released **ppds-mcp-server 1.0.0.0** (41 tools). Any `ppds_*` tool not listed here does not exist on this server version.

| Tool | Description |
|------|-------------|
| `ppds_auth_who` | Get the current authentication profile context including identity, connected environment, and token status. Use this to understand which Dataverse environment queries will run against. |
| `ppds_connection_references_analyze` | Analyze connection references for orphaned references (not used by any flow) and orphaned flows (referencing missing connection references). Useful for deployment cleanup. |
| `ppds_connection_references_get` | Get full details of a specific connection reference including dependent flows and connection info. Use the logicalName from ppds_connection_references_list. |
| `ppds_connection_references_list` | List connection references in the current environment. Shows connector bindings and whether connections are bound. Optionally filter by solution name. |
| `ppds_custom_apis_list` | List all Custom APIs registered in the Dataverse environment. Custom APIs are developer-defined messages that extend the Dataverse API surface with custom business logic. Returns each API with its request parameters and response properties. |
| `ppds_data_analyze` | Analyze data for a Dataverse entity. Returns record count, primary attributes, and sample records. Use this to understand the data in an entity before querying. |
| `ppds_data_providers_list` | List all virtual entity data sources and data providers registered in the Dataverse environment. Data providers implement plugin-based virtual entity adapters that connect Dataverse virtual entities to external data sources. Returns both data source definitions and their associated data provider plugin bindings. |
| `ppds_data_schema` | Get the schema (fields/attributes) for a Dataverse entity. Returns attribute names, types, and metadata. Use this to understand entity structure before querying. |
| `ppds_env_list` | List available Dataverse environments. Use this to discover which environments are accessible with the current authentication profile. The currently selected environment is marked with isActive=true. |
| `ppds_env_select` | Select a Dataverse environment for subsequent queries. You can specify the environment by URL (e.g., 'https://contoso.crm.dynamics.com'), display name (e.g., 'Contoso Production'), or unique name. All subsequent ppds tools will use this environment. |
| `ppds_environment_variables_get` | Get full details of a specific environment variable including description, type, and values. Use the schemaName from ppds_environment_variables_list. |
| `ppds_environment_variables_list` | List environment variable definitions and their current values. Shows default vs current values, type, and override status. Optionally filter by solution name. |
| `ppds_environment_variables_set` | Set the current value of an environment variable. Creates the value record if none exists. AI agents can use this to fix misconfigurations during deployment troubleshooting. |
| `ppds_import_jobs_get` | Get full details of a specific import job including the XML import log. Use the id from ppds_import_jobs_list. The import log XML contains detailed component-level success/failure information for troubleshooting failed imports. |
| `ppds_import_jobs_list` | List recent solution import jobs for the current environment. Shows import status, progress, solution name, and timing. Use this to check if a solution import succeeded or failed. |
| `ppds_metadata_add_column` | Adds a new column (attribute) to an existing Dataverse table. Supports all standard column types. Use dry-run to validate before committing. |
| `ppds_metadata_add_option_value` | Adds a new option value to an existing option set (global or local choice). Returns the assigned integer value. |
| `ppds_metadata_create_choice` | Creates a new global choice (option set) in the specified solution. Options are provided as a JSON array of {label, value} objects. Supports dry-run mode. |
| `ppds_metadata_create_key` | Creates an alternate key on a Dataverse table. Attributes can be provided as a comma-separated list or a JSON array of column logical names. Supports dry-run mode. |
| `ppds_metadata_create_relationship` | Creates a relationship (one-to-many or many-to-many) between two Dataverse tables. For one-to-many, a lookup column is created on the referencing entity. Supports dry-run mode. |
| `ppds_metadata_create_table` | Creates a new Dataverse table (entity) in the specified solution. Supports dry-run mode for validation without persisting changes. Use ppds_metadata_entities to verify the table was created. |
| `ppds_metadata_entities` | Lists all entities (tables) in the connected Dataverse environment. Returns entity logical names, display names, schema names, and ownership type. Use this to discover available entities before querying with ppds_metadata_entity for full details. |
| `ppds_metadata_entity` | Get detailed metadata for a Dataverse entity including attributes, relationships, and keys. Use this to understand entity structure, field types, and how entities relate to each other. |
| `ppds_metadata_update_choice` | Updates an existing global choice (option set). Only the provided optional fields are changed; omitted fields remain unchanged. Supports dry-run mode. |
| `ppds_metadata_update_column` | Updates an existing column (attribute) on a Dataverse table. Only the provided optional fields are changed; omitted fields remain unchanged. Supports dry-run mode. |
| `ppds_metadata_update_relationship` | Updates an existing Dataverse relationship's cascade configuration. Only the provided optional fields are changed; omitted fields remain unchanged. Supports dry-run mode. |
| `ppds_metadata_update_table` | Updates an existing Dataverse table (entity). Only the provided optional fields are changed; omitted fields remain unchanged. Supports dry-run mode. |
| `ppds_plugin_traces_delete` | Delete plugin trace logs. Provide exactly one mode: specific IDs for targeted deletion, olderThanDays for age-based cleanup, or filter parameters (typeName, messageName, primaryEntity, errorsOnly) for criteria-based deletion. |
| `ppds_plugin_traces_get` | Get detailed information about a specific plugin trace including the full message block (trace output) and exception details. Use the trace ID from ppds_plugin_traces_list. |
| `ppds_plugin_traces_list` | List plugin trace logs from Dataverse. Use this to find plugin execution logs, identify errors, and debug plugin behavior. Requires trace logging to be enabled in the environment. |
| `ppds_plugin_traces_timeline` | Build an execution timeline showing all plugin executions for a single transaction. Use the correlationId from ppds_plugin_traces_list to see how plugins chain together and identify performance bottlenecks. |
| `ppds_plugins_get` | Get detailed information for a specific plugin registration entity (assembly, package, type, step, or image). Use ppds_plugins_list first to discover entity names/IDs. |
| `ppds_plugins_list` | List registered plugin assemblies in the Dataverse environment. Shows plugin types and their registered steps (message/entity/stage combinations). By default excludes hidden system assemblies and Microsoft.* assemblies. |
| `ppds_query_fetch` | Execute a FetchXML query against Dataverse. Use this when you have raw FetchXML or need advanced query features not available in SQL. Prefer ppds_query_sql for simpler queries. |
| `ppds_query_sql` | Execute a SQL SELECT query against Dataverse. The SQL is transpiled to FetchXML internally. Supports JOINs, WHERE, ORDER BY, TOP, and aggregate functions. Example: SELECT name, revenue FROM account WHERE statecode = 0 ORDER BY revenue DESC |
| `ppds_service_endpoints_list` | List all service endpoints and webhooks registered in the Dataverse environment. Includes Azure Service Bus (Queue, Topic, EventHub), REST endpoints, and HTTP webhooks. Used for event-driven integrations that receive Dataverse change notifications. |
| `ppds_solutions_components` | Get components of a Dataverse solution. Returns entities, workflows, plugins, and other components. Use the solution id from ppds_solutions_list. Optionally filter by component type code. |
| `ppds_solutions_list` | List Dataverse solutions for the current environment. Shows solution name, version, publisher, and managed status. Use includeManaged to also show managed (system) solutions. |
| `ppds_web_resources_get` | Get web resource content for viewing or analysis. Returns decoded text content for text types (JS, HTML, CSS, XML, etc.) and metadata-only for binary types (PNG, JPG, GIF). Use the id from ppds_web_resources_list. |
| `ppds_web_resources_list` | List web resources in a Dataverse environment, optionally filtered by solution. Returns name, type, managed status, and modification info. Use textOnly=true (default) to exclude binary types like images. Supports pagination via maxRows and nextPageToken parameters — when more records exist the response includes a nextPageToken to pass on the next call. |
| `ppds_web_resources_publish` | Publish specific web resources to make changes live. After updating web resource content, you must publish for changes to take effect. Provide one or more web resource IDs. |
