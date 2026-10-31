# Changelog

All notable changes to this package are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html): MAJOR =
skill renames/removals, MINOR = new skills or capabilities, PATCH = fixes.

## [Unreleased]

Prepared as Skills 0.2.0; no publication is implied by this branch.

### Added

- Capture 273 CLI command nodes and 45 MCP tools from source candidate
  `6932dcd52a38c5fe65bff19e7ce7d1c2d5709304`, with exact binary hashes and
  offline provenance. These captures do not claim public package availability.
- Bounded MCP Main-form authoring: inspect a draft, add an existing field to an
  existing section, verify phase results, and explicitly publish the table.
- Flow activation guidance covering exact selection, preflight, plan hashes,
  environment acknowledgement, per-flow results and bounded verification.
- Notebook environment isolation and shared form/flow safety guidance, including
  captured targets, profile-safe recovery and cancellation ownership.
- Four regression scenarios for draft/publication boundaries, partial form
  writes, flow activation review and notebook target retention. Free structural
  validation is distinct from opt-in semantic model execution.

### Fixed

- Explain plugin double-fault diagnostics, diff cancellation, web-resource
  publisher-prefix warnings and the managed-form validation boundary.
- Distinguish test-only propagation polling, deterministic update-check tests
  and the required Python status gate from runtime product capabilities.
- Keep source prerelease captures from printing the stable-version cleanup
  notice; alpha versions remain prereleases.

## [0.1.2] - 2026-10-30

### Changed

- Re-captured 271 CLI command nodes and 41 MCP tools from public NuGet
  CLI `1.4.2` and MCP `1.2.2`, release commit
  `60dbd696d28c79447fe6490924a462c91f9b2d35`. Regenerated references
  and verified all seven tested-version pins using the real public tools;
  retained package URLs, package/binary hashes, and source provenance.
  Help bodies and MCP names/descriptions match the reviewed simulation.
- Added four regression scenarios for complete view payloads, managed-view
  verification recovery, net48 acceptance, and unsafe reference-cache advice.
  The free harness validates their structure; semantic model runs are separate.

### Fixed

- Pin Linux static checks, release recapture, and opt-in live evals to Ubuntu
  24.04, which has setup-python artifacts
  for the documented Python 3.8 floor; Ubuntu 26.04 setup fails before evals.
- Preserve required static-check names independently of the runner image.
- Include public capture provenance in the core skill's references so copy-only
  installs retain it; reject relative links outside the installed skills tree.
- Correct view terminology to `savedquery`, qualify managed-layer editing,
  and document complete view payloads, related-column identities, intended
  draft verification, partial-write inspection, and scoped publication.
- Explain the CLI maintenance release's `net48` package acceptance,
  supported-framework and signing requirements for loose assemblies, package
  identity validation, and protected reference-cache recovery.
- Document the bounded Timeline FormXML validation correction without
  promising support for arbitrary unknown control parameters.

The full manual public-artifact recapture ran at equal semantic versions.
It used only CLI help/version and MCP initialize/tools/list in an empty
configuration; no paid evaluations or Dataverse operations were performed.

## [0.1.1] - 2026-06-17

Re-captured against **PPDS CLI 1.2.0 stable** (previously 1.2.0-rc.6). The
released surface is byte-identical to rc.6 — no command or flag changes — so
this is a version-alignment refresh.

### Changed

- `metadata.ppds_cli_version_tested` bumped to `1.2.0` across all seven skills;
  `captured-help/` and the generated references regenerated from 1.2.0 stable.
- README, DESIGN, and `ppds-core` drop the `--prerelease` install guidance now
  that 1.2.0 ships stable; stale `1.2.0-rc.6` references updated.
- MCP pin unchanged (`ppds_mcp_server` still self-reports `1.0.0.0`).

## [0.1.0] - 2026-06-17

Initial public release — seven PPDS skills generated against the 1.2.0 CLI
surface (flag tables captured at 1.2.0-rc.6) and PPDS.Mcp server 1.0.0.

### Added

- `ppds-core` — install, auth profiles, environment selection, the safety
  model, error/exit-code interpretation, CLI↔MCP routing.
- `ppds-query` — SQL→FetchXML engine, guarded DML, FetchXML fallback,
  explain/history, TDS routing.
- `ppds-plugins` — declarative plugin registration, Custom APIs, plugin trace
  debugging.
- `ppds-solutions-alm` — solution export/import, import jobs, environment
  variables, connection references, deployment settings.
- `ppds-metadata` — tables, columns, relationships, keys, choices; schema
  compare; views and forms.
- `ppds-data` — bulk export/import/copy, CSV load, bulk update/delete/truncate,
  user mapping.
- `ppds-webresources` — pull/edit/push/publish loop with conflict detection.
- `captured-help/` verbatim CLI/MCP surface, the `evals/check_skills.py` static
  authoring gate, and the `evals/live/` behavioral eval suite.

[Unreleased]: https://github.com/joshsmithxrm/ppds-skills/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/joshsmithxrm/ppds-skills/releases/tag/v0.1.2
[0.1.1]: https://github.com/joshsmithxrm/ppds-skills/releases/tag/v0.1.1
[0.1.0]: https://github.com/joshsmithxrm/ppds-skills/releases/tag/v0.1.0
