# PPDS Skills

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
hand-written. That last part is the point: exact-flag reference tables are
what cut agent flag hallucination from ~58% to ~2.5% in Microsoft's
equivalent package.

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

Versions these skills were generated against: **PPDS CLI 1.2.0-rc.4**,
**PPDS.Mcp server 1.0.0** (recorded per-skill in frontmatter
`metadata.ppds_cli_version_tested`).

## Prerequisite

```bash
dotnet tool install -g PPDS.Cli --prerelease   # the `ppds` CLI
dotnet tool install -g PPDS.Mcp                # optional: `ppds-mcp-server`
```

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

## Regenerating the references (maintainers)

```bash
python tools/capture_cli_help.py       # walks `ppds ... --help` into captured-help/
python tools/capture_mcp_tools.py      # captures MCP tools/list into captured-help/
python tools/generate_flag_tables.py   # rewrites skills/*/references/cli-*.md
python evals/check_skills.py           # static eval suite (also runs in CI)
```

The eval suite fails if a skill cites a command or flag that does not exist
in the captured surface, if frontmatter drifts from the captured versions,
or if generated references go stale. CI: `.github/workflows/evals.yml`.

## Before going public (maintainers)

The current captures are from PPDS CLI **1.2.0-rc.4**. Several command
surfaces are actively changing for **v1.2 stable** (e.g. `--publish` /
`--dry-run` / `--label` on metadata commands, web-resource `create`,
positional entity arguments). Publishing before re-capturing would ship flag
tables that drift from the released CLI — exactly the failure this package
exists to prevent. Do it in this order:

1. **Merge** the initial package to `main` (review complete).
2. **Wait for PPDS CLI v1.2.0 stable** to ship to NuGet.
3. **Install the stable build** (`dotnet tool update -g PPDS.Cli`) and
   **regenerate captures + bump frontmatter** — the tooling is already here:
   ```bash
   python tools/capture_cli_help.py
   python tools/capture_mcp_tools.py
   python tools/generate_flag_tables.py
   # update metadata.ppds_cli_version_tested / ppds_mcp_version_tested in each
   # skills/*/SKILL.md to the stable versions, then:
   python evals/check_skills.py
   ```
4. **Re-run CI** — Actions runs free on public repos, which clears the
   billing block seen on the private repo.
5. **Flip the repo public.**
6. **Submit to the registry / awesome-lists** (tracked in
   [power-platform-developer-suite#1211](https://github.com/joshsmithxrm/power-platform-developer-suite/issues/1211)).

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

## License

MIT — matching PPDS itself.
