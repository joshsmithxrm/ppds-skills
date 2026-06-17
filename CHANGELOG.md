# Changelog

All notable changes to this package are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html): MAJOR =
skill renames/removals, MINOR = new skills or capabilities, PATCH = fixes.

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

[0.1.0]: https://github.com/joshsmithxrm/ppds-skills/releases/tag/v0.1.0
