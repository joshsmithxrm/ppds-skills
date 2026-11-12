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
   as full tool descriptors (including JSON schemas), raw protocol frames,
   sent requests, and a source/data hash receipt in `captured-help/`.
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

### Manual dispatch (preferred)

After verifying both public package versions, dispatch
`.github/workflows/recapture-on-release.yml` with that exact pair. For example,
substitute the reviewed versions for the values below:

```bash
gh workflow run recapture-on-release.yml -f cli_version=1.5.0 -f mcp_version=1.3.0
```

Dispatch is restricted to the default branch. A `contents: read` producer checks
out the exact dispatch commit with `persist-credentials: false`, installs the
selected tools into an isolated directory, and captures into fresh staging.
It retains complete MCP descriptors and the initialize/tools-list exchange;
partial or paginated responses fail. CLI aliases are explicitly derived from
the exact shown spellings, with counts and a canonical-path map.

After the static gate, the producer uploads one JSON data bundle. A fresh writer
job checks out the same commit without persisted credentials, validates the
repository/source/run/attempt/pair binding and data/source hashes, then applies
only known capture and generated-reference paths. It updates the two version
pins in trusted `SKILL.md` frontmatter; it never executes PPDS or artifact code.
`GH_TOKEN` is supplied only to the final Git/draft-PR shell step; checkout uses
the job token to fetch but does not persist it. Obsolete CLI
captures and the old candidate-only platform record are removed in the proposed
diff, requiring human review.

The workflow **never auto-merges** and has no schedule. Every valid dispatch
captures both tools, including MCP-only or same-pair updates. Versions alone do
not imply a no-op: protocol/runtime/provenance bytes may change. Byte-identical
validated data opens no PR. Package/source hashes in the 14-day run artifact are
producer observations, not independent public-package authenticity proof. Review
public package identity and the resulting capture diff separately; the PR links
the exact run/attempt and bundle hash.
Recapture maintenance uses Python 3.14.10 and .NET SDK 10.0.404. The
`maintainer-runtime` PR job checks those runtimes and runs offline tests with
product calls replaced by offline doubles; consumer static checks retain Python
3.8. These tests establish parser/handoff behavior, not a new stable capture,
public-package identity, or hosted product execution result.
Two operational gotchas:

- The repo setting **Settings → Actions → General → "Allow GitHub Actions to
  create and approve pull requests"** must stay **on**, or the final
  PR-creation step fails.
- A `GITHUB_TOKEN`-opened PR does not trigger CI, so the auto-PR shows no
  `skill-evals` checks and can't merge as-is — **close and reopen it** to fire
  the checks. Then review the capture diff and the PR's manual-prose checklist
  (drop any `--prerelease` guidance and stale `rc` mentions — `check_skills.py`
  does **not** catch those once the pin is stable), resolve any review threads,
  and merge.

### Local recapture

```bash
dotnet tool update -g PPDS.Cli --version "$CLI_VERSION"   # verified exact version
dotnet tool update -g PPDS.Mcp --version "$MCP_VERSION"   # verified exact version
TARGET_CLI_VERSION="$CLI_VERSION" TARGET_MCP_VERSION="$MCP_VERSION" python3 tools/recapture.py
python3 evals/check_skills.py
```

`tools/recapture.py` wraps `capture_cli_help.py`, `capture_mcp_tools.py`, and
`generate_flag_tables.py`, then bumps `metadata.ppds_cli_version_tested` /
`ppds_mcp_version_tested` in every `skills/*/SKILL.md` from the fresh manifests.
It always captures again, even when the version matches the committed pin.
Review obsolete local capture files separately; automation uses a fresh staging
tree. Identical output produces no diff. Both local capture and manual dispatch can
replace candidate captures with public packages of the same version; neither
uses a newer-CLI-only comparison to decide whether to capture.

After a candidate recapture, update
`skills/ppds-core/references/candidate-provenance.json` from the actual source
commit, package and DLL hashes, and capture evidence. Keep the previous record
in the review artifacts. The recapture scripts do not rewrite provenance or
turn simulated version strings into proof of public availability.

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

Agent-driven: the `release` skill (`.claude/skills/release/`) walks these steps
with the version-bump and prose-cleanup judgment baked in. The steps, for
reference:

1. Re-capture against the target CLI/MCP versions (above) and bump frontmatter.
2. Bump the version in `plugin.json` **and** the `marketplace.json` plugin
   entry (they must match — the eval enforces it).
3. Add a `CHANGELOG.md` entry. Keep it `Unreleased` with a comparison link
   during preparation; finalize its date and tag link when publication is approved.
4. `python3 evals/check_skills.py` must pass.
5. Review and merge the PR only when plugin publication is approved. The
   documented marketplace installs from `main`, so merging the version bump
   distributes it before a separate tag or GitHub Release exists.
6. Tag the reviewed merge commit `vX.Y.Z` and cut a GitHub Release.

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
