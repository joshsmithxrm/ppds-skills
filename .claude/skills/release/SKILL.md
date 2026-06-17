---
name: release
description: Cut a PPDS Skills package release — get the recapture, decide the version bump, clean up prose, update CHANGELOG, tag + GitHub Release. Use when PPDS ships a new stable CLI/MCP that the skills package must track, or to publish any skills-package version bump.
---

# Release (PPDS Skills package)

A *lightweight* release flow for **this** package — not the multi-surface engine
release. There is no NuGet/npm publish pipeline: users install from the repo /
plugin marketplace, so "release" means a reviewed version bump on `main` plus a
tag and GitHub Release. The mechanical capture is automated; this skill covers
the judgment + finalization the automation deliberately leaves to a human.

## When

- A new **stable** PPDS CLI/MCP shipped (the usual trigger — the engine's
  `release` skill §8 dispatches the recapture automatically), or
- any change warranting a published version bump.

## 1. Get the recapture

Preferred — let the automation produce the PR:

```bash
gh workflow run recapture-on-release.yml
```

It installs the released CLI/MCP, regenerates `captured-help/` + references, bumps
the frontmatter pins, runs the gate, and opens a PR. **Gotchas:** the *Allow
GitHub Actions to create and approve PRs* repo setting must be on, and a
bot-opened PR shows no CI — **close/reopen it** to fire `skill-evals`.

Offline alternative: `dotnet tool update -g PPDS.Cli && dotnet tool update -g PPDS.Mcp`
then `python3 tools/recapture.py`. See CONTRIBUTING "Regenerating the references".

## 2. Read the capture diff → decide the version bump

Diff `captured-help/` against the previous tag. Per the package's semver
(`plugin.json` / `marketplace.json`):

- **PATCH** — captures byte-identical, or only version strings moved (pure
  alignment, e.g. `rc` → stable).
- **MINOR** — new commands / flags / MCP tools (new documented capability), or
  new skill content.
- **MAJOR** — a skill renamed or removed.

## 3. Prose cleanup the gate can't catch

`check_skills.py::check_prose_version_drift` early-returns on a **stable** pin, so
hand-check these when moving rc → stable:

- **Drop** `--prerelease` install guidance and stale `rc` mentions in `README.md`,
  `DESIGN.md`, `skills/*/SKILL.md`, and hand-written `skills/*/references/*.md`.
- **Leave alone:** `CHANGELOG.md` (immutable history) and `CONTRIBUTING.md`
  (intentionally version-agnostic runbook guidance).
- Note the MCP pin: `ppds-mcp-server` may self-report a version that lags its
  NuGet package; the pin tracks the **self-reported** version, so only bump
  `ppds_mcp_version_tested` if the captured `serverInfo.version` actually changed.

## 4. Version + CHANGELOG

- Bump `version` in `.claude-plugin/plugin.json` **and** the `marketplace.json`
  plugin entry — the eval enforces they match.
- Add a `CHANGELOG.md` entry (Keep a Changelog sections) **and** the `[X.Y.Z]`
  release-link footer.

## 5. Gate + merge

```bash
python3 evals/check_skills.py    # must pass: validates against the new capture
```

Open the PR, link/close the tracking issue (e.g. `Closes #N`), resolve any review
threads (conversation resolution is required to merge). Squash-merge.

## 6. Tag + GitHub Release

```bash
git checkout main && git pull          # main now at the squash-merged release
git tag -a vX.Y.Z -m "release: X.Y.Z"
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" --notes "<the CHANGELOG X.Y.Z section>"
```

## References

- `CONTRIBUTING.md` — "Regenerating the references" + "Release process".
- `.github/workflows/recapture-on-release.yml` — the recapture automation.
- Engine `release` skill §8 — what triggers our recapture on a PPDS stable.
