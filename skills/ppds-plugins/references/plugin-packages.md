# Plugin packages and extraction troubleshooting

This guidance covers the CLI 1.4.2 maintenance candidate. Check the installed
version and capture provenance; published 1.4.1 lacks net48 package acceptance
and the protected-cache changes. Preserve ppds-core's environment and mutation
controls. Local extraction does not authorize deployment.

## Framework and package identity

- `PPDS.Plugins` retains its `net462` library target; plugin projects can
  reference it from .NET Framework 4.6.2 through 4.8.
- The candidate accepts package asset groups `lib/net462`, `lib/net471`, and
  `lib/net48`. A package without one of those groups fails local preflight.
- A loose DLL must still target a Dataverse-supported .NET Framework version
  and be strong-name-signed. Repackaging does not make netstandard/modern .NET
  code supported. Do not suggest that fallback for every framework error.
- Extraction/deploy validates one unambiguous primary assembly, official SDK
  and registration-attribute identities, configured runtime `IPlugin` types,
  and package snapshots. A runtime plugin type can have no PPDS attributes;
  that does not imply generated steps. Resolve local identity/configuration
  errors before connecting or uploading.
- Retain the package bytes used for extraction. If the package changes,
  re-extract and preview rather than stripping extraction evidence or reusing
  stale registration JSON. `--reference-dir` helps resolve external ancestry;
  it does not waive identity checks.

Replace placeholders with the reviewed local package/profile/environment:

```text
ppds plugins extract --input <package.nupkg> --output registrations.json
ppds plugins deploy --config registrations.json --dry-run --profile <profile> --environment <environment-url>
```

Review before a separately authorized deployment. If the server lacks expected
state after an upload, inspect before retrying. Unregister/cleanup is a separate
destructive action, not an automatic rollback.

## Reference-cache failures

Single-file installs embed framework references. The candidate stores them
under the OS local application-data directory at
`PPDS/cache/net462-ref/<resource-hash>`. It validates ownership, permissions,
and links before reading or repairing cache contents. Missing/truncated
expected files are restored; complete caches are reused without rewriting.

On an unsafe-storage warning, preserve stderr and use protected local user
storage. Have its owner/administrator correct the reported permission or
ownership problem; do not grant broad write access, disable checks, or run
elevated to work around it. Mutation-capable macOS ACLs are conservatively
rejected. Legacy shared-temp caches are not reused, migrated, or deleted.

Do not promise protection from same-account processes, admin/root, or hostile
filesystems. Expected-file/length checks detect deletion and truncation, not
arbitrary same-length tampering inside the trusted account. Do not prescribe
recursive cache deletion as a generic repair.

Source: [package identity](https://github.com/joshsmithxrm/power-platform-developer-suite/pull/1414),
[net48 acceptance](https://github.com/joshsmithxrm/power-platform-developer-suite/pull/1450),
[cache isolation](https://github.com/joshsmithxrm/power-platform-developer-suite/pull/1471).
