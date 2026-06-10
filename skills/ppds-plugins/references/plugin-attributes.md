# PPDS.Plugins attributes — declarative registration source of truth

Source of truth: the public `PPDS.Plugins` NuGet package (targets `net462`,
the Dataverse sandbox framework) and its attribute sources. Install in the
plugin project:

```bash
dotnet add package PPDS.Plugins
```

Registration metadata lives **next to the code** as attributes; the CLI
extracts it from the compiled assembly. No Plugin Registration Tool clicks.

## `[PluginStep]` — SDK message registration (one per step; repeatable)

```csharp
using Microsoft.Xrm.Sdk;
using PPDS.Plugins;

[PluginStep(
    Message = "Update",
    EntityLogicalName = "account",
    Stage = PluginStage.PostOperation,
    Mode = PluginMode.Synchronous,
    FilteringAttributes = "name,telephone1")]
[PluginImage(
    ImageType = PluginImageType.PreImage,
    Name = "PreImage",
    Attributes = "name,telephone1")]
public class AccountUpdatePlugin : IPlugin
{
    public void Execute(IServiceProvider serviceProvider) { /* ... */ }
}
```

Properties (verified against the released attribute source):

| Property | Type / values | Notes |
|----------|---------------|-------|
| `Message` | string | `Create`, `Update`, `Delete`, `Retrieve`, `RetrieveMultiple`, `Associate`, ... |
| `EntityLogicalName` | string | primary entity logical name |
| `SecondaryEntityLogicalName` | string? | for messages with a secondary entity |
| `Stage` | `PluginStage.PreValidation` / `PreOperation` / `PostOperation` | pipeline stage |
| `Mode` | `PluginMode.Synchronous` (default) / `Asynchronous` | |
| `FilteringAttributes` | string? | comma-separated; Update-class messages |
| `ExecutionOrder` | int (default 1) | rank within stage |
| `Name`, `Description` | string? | step display name / description |
| `UnsecureConfiguration` | string? | step unsecure config |
| `AsyncAutoDelete` | bool | delete async job on success |
| `Deployment` | `PluginDeployment.ServerOnly` (default) / `Offline` / `Both` | |
| `RunAsUser` | string? | calling user by default; user GUID/email to impersonate |
| `CanBeBypassed` | bool (default true) | participates in bypass-plugins scenarios |
| `CanUseReadOnlyConnection` | bool | step may run on read replica |
| `InvocationSource` | `PluginInvocationSource.Parent` (default) / `Child` | |
| `StepId` | string? | correlates with `[PluginImage(StepId=...)]` when a class has multiple steps |

## `[PluginImage]` — pre/post entity images

| Property | Type / values |
|----------|---------------|
| `ImageType` | `PluginImageType.PreImage` / `PostImage` / `Both` |
| `Name` | string — the key used in `context.PreEntityImages[...]` |
| `Attributes` | string? comma-separated (null = all attributes) |
| `EntityAlias` | string? |
| `StepId` | string? — bind the image to a specific `[PluginStep]` |
| `Description`, `MessagePropertyName` | string? |

## `[CustomApi]` + `[CustomApiParameter]` — Custom API declaration

| `[CustomApi]` property | Type / values |
|------------------------|---------------|
| `UniqueName`, `DisplayName` | string (required) |
| `Name`, `Description` | string? |
| `BindingType` | `ApiBindingType.Global` (default) / `Entity` / `EntityCollection` |
| `BoundEntity` | string? — required when bound |
| `IsFunction` | bool — function (GET, no side effects) vs action |
| `IsPrivate` | bool |
| `ExecutePrivilegeName` | string? |
| `AllowedProcessingStepType` | `ApiProcessingStepType.None` (default) / `AsyncOnly` / `SyncAndAsync` |

| `[CustomApiParameter]` property | Type / values |
|--------------------------------|---------------|
| `Name` | string (required) |
| `UniqueName`, `DisplayName`, `Description` | string? |
| `Type` | `ApiParameterType.*` (String, Guid, Integer, Boolean, DateTime, Decimal, Entity, EntityCollection, EntityReference, Float, Money, Picklist, StringArray) |
| `LogicalEntityName` | string? — for entity-typed parameters |
| `IsOptional` | bool |
| `Direction` | `ParameterDirection.Input` (default) / `Output` |

## Known doc drift (trust the captured CLI help)

The PPDS.Plugins package README shows an `--assembly` flag on the deploy
command; the released CLI takes `--config <registrations.json>` (required) —
produce that file with `ppds plugins extract` first. Flags as shipped:
[cli-plugins.md](cli-plugins.md).
