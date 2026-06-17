# Security Policy

## Scope

This repository ships **documentation skills** — Markdown that teaches AI
coding agents to drive the Power Platform Developer Suite (PPDS). It contains
no runtime that connects to Dataverse. The CLI and MCP server that perform the
actual operations (auth, DML, bulk delete, solution import) live in a separate
project:
[power-platform-developer-suite](https://github.com/joshsmithxrm/power-platform-developer-suite).

- A vulnerability in the **PPDS CLI or MCP server** → report it against the
  [power-platform-developer-suite](https://github.com/joshsmithxrm/power-platform-developer-suite/security)
  repository, not here.
- A problem in **these skills** — for example, guidance that would lead an
  agent to take an unsafe action against a Dataverse environment — → report it
  here, privately, as below.

## Reporting a vulnerability

Please report privately via GitHub Security Advisories: open the **Security**
tab of this repository and choose **Report a vulnerability**. Do not open a
public issue for a security report.

You can expect an acknowledgement within a few days.

## Supported versions

Fixes are made against the latest released version (currently the 0.1.x line).
