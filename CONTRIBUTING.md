# Contributing to PPDS Skills

Thanks for your interest in improving the PPDS skills package! This repo is a
**knowledge layer**, not application code: it ships Markdown
[Agent Skills](https://agentskills.io) that teach AI coding agents to drive the
[Power Platform Developer Suite](https://github.com/joshsmithxrm/power-platform-developer-suite)
(PPDS). Bugs in the `ppds` CLI or MCP server itself belong in the
[engine repository](https://github.com/joshsmithxrm/power-platform-developer-suite/issues),
not here.

## How this repo works

See [DESIGN.md](DESIGN.md) for the rationale. In short, the package's whole
value is that **every command and flag a skill cites is real** — never
hand-written:

1. `tools/capture_cli_help.py` walks `ppds <command> --help` over the full
   command tree into `captured-help/*.txt` + `manifest.json`.
2. `tools/capture_mcp_tools.py` records the MCP server's `tools/list` response
   into `captured-help/mcp-tools.json`.
3. `tools/generate_flag_tables.py` embeds those captures **verbatim** into
   `skills/*/references/cli-*.md` and `mcp-tools.md`.
4. `evals/check_skills.py` closes the loop: prose cannot cite a command, flag,
   or MCP tool that the captures don't contain.

> **The `references/cli-*.md` and `mcp-tools.md` files are GENERATED. Never
> hand-edit them** — your change will be overwritten on the next regenerate and
> the eval suite will reject it. Edit the capture tooling or re-run a capture
> instead.

## Prerequisites

- **Python 3.8+** — the eval suite is zero-dependency (standard library only).
- The **`ppds` CLI** is only needed to *re-capture* the surface (maintainers);
  contributors editing skill prose do not need it — the evals validate against
  the committed `captured-help/`.

## Making changes

- Keep each `SKILL.md` body **≤150 lines**; push depth into `references/`
  (loaded on demand). Enforced by the eval suite.
- Frontmatter: `name` (= directory), a `description` with a "Use when …"
  trigger clause (≤1024 chars), `license`, and the
  `metadata.ppds_cli_version_tested` / `ppds_mcp_version_tested` pins.
- Every non-cross-cutting skill ends with a `## Skill boundaries` table and
  states its CLI↔MCP routing.
- **Run the static evals before every PR:**
  ```bash
  python3 evals/check_skills.py
  ```

## Running the evals

- **Static** (free, every PR):
  ```bash
  python3 evals/check_skills.py      # the authoring gate
  python3 evals/live/_selftest.py    # behavioral-harness self-test
  ```
  If your installed `ppds` version differs from the captures, the
  capture-freshness check will fail locally — re-capture (below), upgrade your
  CLI to match, or set `PPDS_SKIP_FRESHNESS=1` to bypass it for an unrelated
  change.
- **Behavioral / live** (opt-in, **billed** — drives `claude` headless for the
  agent under test and an LLM judge):
  ```bash
  python3 evals/live/run_live_evals.py            # all scenarios
  python3 evals/live/run_live_evals.py --filter ppds-query
  ```
  Run it where `claude` is logged into your subscription. See
  [evals/live/README.md](evals/live/README.md).

## Regenerating the references (maintainers)

Re-capture whenever the installed CLI/MCP surface moves (each new rc, and again
at v1.2.0 stable).

### Automated (preferred)

A new **stable** `PPDS.Cli` on NuGet is picked up by
`.github/workflows/recapture-on-release.yml` — weekly, or on demand:

```bash
gh workflow run recapture-on-release.yml
```

It installs the released CLI/MCP, re-captures, runs `tools/recapture.py` to bump
the frontmatter pins, runs the static gate, and opens a PR for review. It
**never auto-merges**, and it correctly no-ops when the latest stable isn't newer
than the captured version (e.g. while `1.2.0-rc.N` is still ahead of the latest
published stable). Two operational gotchas:

- The repo setting **Settings → Actions → General → "Allow GitHub Actions to
  create and approve pull requests"** must stay **on**, or the final
  PR-creation step fails.
- A `GITHUB_TOKEN`-opened PR does not trigger CI, so the auto-PR shows no
  `skill-evals` checks and can't merge as-is — **close and reopen it** to fire
  the checks. Then review the capture diff and the PR's manual-prose checklist
  (drop any `--prerelease` guidance and stale `rc` mentions — `check_skills.py`
  does **not** catch those once the pin is stable), resolve any review threads,
  and merge.

### Manual (offline, or what the automation runs under the hood)

```bash
dotnet tool update -g PPDS.Cli --prerelease   # or drop --prerelease at stable
dotnet tool update -g PPDS.Mcp --prerelease   # or drop --prerelease at stable
python3 tools/recapture.py                    # 3 capture scripts + frontmatter bump
python3 evals/check_skills.py
```

`tools/recapture.py` wraps `capture_cli_help.py`, `capture_mcp_tools.py`, and
`generate_flag_tables.py`, then bumps `metadata.ppds_cli_version_tested` /
`ppds_mcp_version_tested` in every `skills/*/SKILL.md` from the fresh manifests.
Run against the currently installed CLI it is a no-op (zero diff).

## Branch strategy

- `main` — protected, always releasable.
- `feat/*` — new skills or capabilities.
- `fix/*` — corrections.
- `chore/*` — captures, tooling, docs.

Create your branch from `main`.

## Pull request process

1. Open a PR targeting `main` and fill out the template.
2. Don't hand-edit generated reference tables; run the regenerate loop instead.
3. Make sure `python3 evals/check_skills.py` passes locally.
4. Wait for CI (the `skill-evals` workflow runs on Linux + Windows).
5. Address review feedback; PRs are squash-merged.

Versioning is semver in `.claude-plugin/plugin.json` and
`.claude-plugin/marketplace.json` (kept equal by the eval suite): MAJOR = skill
renames/removals, MINOR = new skills/capabilities, PATCH = fixes.

## Release process

1. Re-capture against the target CLI/MCP versions (above) and bump frontmatter.
2. Bump the version in `plugin.json` **and** the `marketplace.json` plugin
   entry (they must match — the eval enforces it).
3. Add a `CHANGELOG.md` entry.
4. `python3 evals/check_skills.py` must pass.
5. Tag `vX.Y.Z` and cut a GitHub Release.

## Getting help

- **Questions / ideas**: open a
  [Discussion on the main PPDS repo](https://github.com/joshsmithxrm/power-platform-developer-suite/discussions)
  — the skills share the PPDS community hub.
- **Bugs in the skills**: open an
  [Issue](https://github.com/joshsmithxrm/ppds-skills/issues).
- **Bugs in the `ppds` CLI / MCP server**: file them in the
  [engine repo](https://github.com/joshsmithxrm/power-platform-developer-suite/issues).

## License

By contributing, you agree that your contributions will be licensed under the
MIT License.
