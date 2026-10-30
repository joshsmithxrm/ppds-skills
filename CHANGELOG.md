# Changelog

All notable changes to this package are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html): MAJOR =
skill renames/removals, MINOR = new skills or capabilities, PATCH = fixes.

## [0.1.2] - Unreleased

### Changed

- Re-captured 271 CLI command nodes and 41 MCP tools from commit
  `6fec5a6909900b5356defdef3eea893fdaece685`: CLI `1.4.2` and
  MCP `1.2.2`. Regenerated references and all seven tested-version
  pins from actual output of a local stable-version simulation; retained
  source/binary provenance. These are not captures of public packages.
- Added four regression scenarios for complete view payloads, managed-view
  verification recovery, net48 acceptance, and unsafe reference-cache advice.
  The free harness validates their structure; semantic model runs are separate.

### Fixed

- Pin Linux static checks, release recapture, and opt-in live evals to Ubuntu
  24.04, which has setup-python artifacts
  for the documented Python 3.8 floor; Ubuntu 26.04 setup fails before evals.
- Preserve required static-check names independently of the runner image.
- Include candidate provenance in the core skill's references so copy-only
  installs retain it; reject relative links outside the installed skills tree.
- Correct view terminology to `savedquery`, qualify managed-layer editing,
  and document complete view payloads, related-column identities, intended
  draft verification, partial-write inspection, and scoped publication.
- Explain the CLI maintenance candidate's `net48` package acceptance,
  supported-framework and signing requirements for loose assemblies, package
  identity validation, and protected reference-cache recovery.
- Document the bounded Timeline FormXML validation correction without
  promising support for arbitrary unknown control parameters.

This release is in preparation. Candidate capture provenance and final
public-artifact recapture are recorded separately; no package publication is
implied by these manifest version changes.

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

[0.1.2]: https://github.com/joshsmithxrm/ppds-skills/compare/v0.1.1...codex/maintenance-skills-20261029
[0.1.1]: https://github.com/joshsmithxrm/ppds-skills/releases/tag/v0.1.1
[0.1.0]: https://github.com/joshsmithxrm/ppds-skills/releases/tag/v0.1.0
