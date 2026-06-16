---
name: ppds-webresources
description: Manage Dataverse web resources with PPDS — pull JavaScript/CSS/HTML/image web resources to a local folder with tracking metadata, edit locally, push changes back with conflict detection, and publish. Use when the user wants to download web resources for editing, sync local script changes to Dataverse, publish a web resource, or get its Maker portal URL. Read ppds-core first for auth and safety rules.
license: MIT
metadata:
  ppds_cli_version_tested: "1.2.0-rc.6"
  ppds_mcp_version_tested: "1.0.0"
---

# PPDS Web Resources — pull, edit, push, publish

Exact flags: [references/cli-webresources.md](references/cli-webresources.md).

**Surface routing**: the pull/push loop is CLI-only (it manages local
tracking metadata). MCP read/publish tools for shell-less hosts:
`ppds_web_resources_list`, `ppds_web_resources_get`,
`ppds_web_resources_publish`.

## The edit loop

```bash
# 1. Pull to a local folder (writes tracking metadata for conflict detection)
ppds webresources pull ./webres --solution MySolution --type js --strip-prefix

# 2. Edit files locally with normal tooling

# 3. Preview the push (still queries the server for conflicts)
ppds webresources push ./webres --dry-run

# 4. Push + publish (publish is required before apps see the change)
ppds webresources push ./webres --publish
```

Key behaviors (verified against the released CLI):

- `pull` filters: `--solution`, `--type` (`text`, `image`, `data`, or a
  specific type like `js`, `css`, `html`, `png`), `--name` (partial match).
- `--strip-prefix` removes the publisher prefix from local paths
  (`new_/scripts/app.js` → `scripts/app.js`); the prefix is restored on push.
- `push` detects **server conflicts** (someone edited since your pull) and
  **environment mismatch** (folder pulled from a different environment than
  the current connection). `--force` skips both checks — that is a safety
  override: re-pull and merge instead unless the user explicitly accepts
  clobbering (`WebResource.Conflict` is the error code you'll see).
- `push --dry-run` is the preview step the safety model requires.
- Publishing alone (no content change): `ppds webresources publish <names>`.
- Browse/read: `ppds webresources list "<name-pattern>"`,
  `ppds webresources get <name>`, `ppds webresources url <name>`.

## Common mistakes (do not invent these)

| Wrong | Correct |
|-------|---------|
| `ppds webresources upload <file>` | `pull` a folder, edit, `push` the folder |
| `ppds webresources push --file app.js` | push takes the tracked **folder**: `ppds webresources push ./webres` |
| Forgetting publish | `push --publish`, or `ppds webresources publish <names>` afterward |
| `--web-resource-type 3` (numeric API codes) | human types: `--type js`, `--type css`, ... |
| Editing managed web resources | `WebResource.NotEditable` — change them in the unmanaged source solution |

## Skill boundaries

| Need | Use instead |
|------|-------------|
| Ship web resources to another environment | ppds-solutions-alm (solution export/import) |
| Forms that reference these scripts | ppds-metadata (`ppds forms ...`) |
| Auth, environment selection, error codes | ppds-core |
