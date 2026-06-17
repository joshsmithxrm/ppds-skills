# PPDS Skills

[![skill-evals](https://github.com/joshsmithxrm/ppds-skills/actions/workflows/evals.yml/badge.svg)](https://github.com/joshsmithxrm/ppds-skills/actions/workflows/evals.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Claude%20Code%20%7C%20Copilot%20CLI-8A2BE2)](https://agentskills.io)
[![Docs](https://img.shields.io/badge/docs-ppds--docs-blue)](https://joshsmithxrm.github.io/ppds-docs/)

A knowledge-layer skills package that teaches AI coding agents (Claude Code,
GitHub Copilot CLI, and any [Agent Skills](https://agentskills.io)-compatible
host) to drive the [Power Platform Developer
Suite](https://github.com/joshsmithxrm/power-platform-developer-suite) (PPDS)
well against Microsoft Dataverse.

Free, MIT-licensed, runs entirely on your machine with zero telemetry — no
hosted broker, no per-call credits, no data leaving your environment.

Skills are Markdown documentation, not code: each `skills/<name>/SKILL.md`
carries frontmatter the agent uses for discovery, a lean body with workflows
and hard safety rules, and a `references/` directory whose CLI flag tables
are **generated verbatim from real `ppds <command> --help` output** — never
hand-written. That last part is the point: exact-flag reference tables are the
technique Microsoft's Dataverse skills package credits for sharply reducing
agent flag hallucination, and the same discipline — an eval that rejects any
command or flag absent from the captured surface — caught 9 real flag/command
errors while these skills were being authored.

## The skills

| Skill | Covers |
|-------|--------|
| `ppds-core` | Install, auth profiles (browser / device code / service principal / managed identity / federated), environment selection, **the safety model** (environment types, dry-run-first, MCP `--read-only` / `--allowed-env`, multi-environment confirmation), error/exit-code interpretation, CLI↔MCP routing |
| `ppds-query` | SQL→FetchXML engine (joins, CTEs, aggregates, window functions), guarded DML, FetchXML fallback, explain/history, TDS routing |
| `ppds-plugins` | Declarative plugin registration (attributes → extract → diff → deploy), Custom APIs, plugin trace debugging recipe (list/get/timeline) |
| `ppds-solutions-alm` | Solution export/import, import jobs, environment variables, connection references, deployment settings |
| `ppds-metadata` | Browse + author tables, columns, relationships, keys, choices; schema compare; views and forms |
| `ppds-data` | Schema-driven bulk export/import/copy, CSV load, bulk update/delete/truncate, user mapping |
| `ppds-webresources` | Pull/edit/push/publish loop with conflict detection |

These skills target the **1.2.0** CLI surface (flag tables captured at
1.2.0-rc.6) and **PPDS.Mcp server 1.0.0**. The exact tested versions live in
each skill's frontmatter (`metadata.ppds_cli_version_tested` /
`ppds_mcp_version_tested`) and are enforced by the eval suite; re-capture
against 1.2.0 stable is tracked in
[#2](https://github.com/joshsmithxrm/ppds-skills/issues/2).

## Prerequisite

```bash
dotnet tool install -g PPDS.Cli    # the `ppds` CLI
dotnet tool install -g PPDS.Mcp    # optional: `ppds-mcp-server`
```

Update later with `dotnet tool update -g PPDS.Cli`. These skills target the
1.2.0 surface; until PPDS 1.2.0 ships stable, add `--prerelease` to install it
(`dotnet tool install -g PPDS.Cli --prerelease`).

## Install — Claude Code

As a plugin (recommended):

```
/plugin marketplace add joshsmithxrm/ppds-skills
/plugin install ppds@ppds-skills
```

Or without the plugin system, copy the skill directories:

```bash
git clone https://github.com/joshsmithxrm/ppds-skills
cp -r ppds-skills/skills/* ~/.claude/skills/          # personal, all projects
# or into a repo:  cp -r ppds-skills/skills/* <your-repo>/.claude/skills/
```

## Install — GitHub Copilot CLI

Copilot CLI reads Agent Skills from `~/.copilot/skills/` (personal) or, per
repo, from `.github/skills/`, `.claude/skills/`, or `.agents/skills/`:

```bash
git clone https://github.com/joshsmithxrm/ppds-skills
mkdir -p ~/.copilot/skills && cp -r ppds-skills/skills/* ~/.copilot/skills/
```

Then in a Copilot session: `/skills list` should show the seven `ppds-*`
skills (`/skills reload` after copying mid-session).

## Smoke test

1. Create an auth profile once: `ppds auth create`
2. Ask your agent: **"List my Dataverse environments."**

The agent should load `ppds-core` and run `ppds env list` (or the
`ppds_env_list` MCP tool) — not a `pac` command, and not an invented flag.
Follow up with "How many accounts are in <env>?" and it should route to
`ppds query sql` with a `COUNT(*)`.

## Evals — static and behavioral

Two layers:

- **Static** (`evals/check_skills.py`, zero-dependency, every PR) — proves the
  skills only *cite* real commands/flags, frontmatter matches the captured
  versions, generated references are fresh, and the plugin manifests agree.
  A capture-freshness check additionally fails **locally** when an installed
  `ppds` differs from the captures — a pre-publish nudge to re-capture (or to
  upgrade your CLI to the targeted surface); it self-skips in CI, which
  installs no CLI to keep the suite zero-dependency.
- **Behavioral** (`evals/live/`) — proves an agent given a real task actually
  loads the right skill and routes PPDS correctly (`SKILL_LOADED` /
  `CONTAINS` / `NOT_CONTAINS` / LLM-judged `semantic`, at P1–P3). The
  mechanical half (harness self-test + scenario validation against the captured
  surface) runs free on every PR; the billed, LLM-judged run is opt-in
  (`.github/workflows/live-evals.yml`, or `python3 evals/live/run_live_evals.py`
  locally). See [evals/live/README.md](evals/live/README.md).

Maintainers: the reference-regeneration and release process (re-capture,
version bump, publish) lives in [CONTRIBUTING.md](CONTRIBUTING.md).

## Conventions

- Frontmatter: `name` (= directory), `description` with a "Use when …"
  trigger clause (≤1024 chars), `license`, and
  `metadata.ppds_cli_version_tested` / `metadata.ppds_mcp_version_tested`.
- `SKILL.md` body ≤150 lines; depth goes to `references/` (loaded on demand).
- Every non-cross-cutting skill ends with a `## Skill boundaries` routing
  table; every skill states CLI↔MCP routing.
- Versioning: semver in `.claude-plugin/plugin.json` +
  `.claude-plugin/marketplace.json` (kept equal by the eval suite). MAJOR =
  skill renames/removals; MINOR = new skills or capabilities; PATCH = fixes.

## Related projects

| Project | Description |
|---------|-------------|
| [power-platform-developer-suite](https://github.com/joshsmithxrm/power-platform-developer-suite) | The PPDS CLI, MCP server, TUI, VS Code extension, and NuGet libraries these skills drive |
| [ppds-docs](https://joshsmithxrm.github.io/ppds-docs/) | PPDS documentation site |
| [VS Code extension](https://marketplace.visualstudio.com/items?itemName=JoshSmithXRM.power-platform-developer-suite) | PPDS in the editor — profiles, solutions browser, `.ppdsnb` notebooks |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how the captured-help layer and
reference tables are regenerated, how to run the evals, and the release
process. By participating you agree to the
[Code of Conduct](CODE_OF_CONDUCT.md). Security reports: see
[SECURITY.md](SECURITY.md).

## Trademarks

This is an independent, community project and is not affiliated with, endorsed
by, or sponsored by Microsoft, Anthropic, or GitHub. Microsoft, Dataverse,
Power Platform, Power Apps, Power Automate, and Dynamics 365 are trademarks of
Microsoft Corporation. Claude and Anthropic are trademarks of Anthropic, PBC.
GitHub and GitHub Copilot are trademarks of GitHub, Inc. All third-party marks
are used nominatively to identify the products this package interoperates with;
their use does not imply endorsement.

## License

MIT — matching PPDS itself. See [LICENSE](LICENSE).
