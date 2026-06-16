# SPEC — AC traceability for issue #1011

Maps every acceptance criterion of
[power-platform-developer-suite#1011](https://github.com/joshsmithxrm/power-platform-developer-suite/issues/1011)
to its implementation in this repository, for AC-by-AC review.

| AC | Requirement | Status | Where / how |
|----|-------------|--------|-------------|
| AC-01 | Skills package structure (frontmatter token budgets, body token budgets, references directory) defined and documented | **Done** | Conventions section in [README.md](README.md): frontmatter ≤1024-char description with "Use when" triggers (≈Level-1 ~100–200 tokens), body ≤150 lines (well under the Agent Skills 5k-token guidance), unlimited `references/` loaded on demand. Enforced mechanically by [evals/check_skills.py](evals/check_skills.py). |
| AC-02 | Initial skill set covers: connect/auth, plugin work, query (FetchXML/SQL), data CRUD/bulk, metadata, solutions, web resources, plugin traces, environment management | **Done** | 7 skills: connect/auth + environment management → `ppds-core`; query → `ppds-query`; plugin work + plugin traces → `ppds-plugins`; solutions → `ppds-solutions-alm`; metadata → `ppds-metadata`; data CRUD/bulk → `ppds-data`; web resources → `ppds-webresources`. Depth priority per design ratification: core/query/plugins built deepest. |
| AC-03 | Each skill names PPDS surface (CLI command + MCP tool) and routing rules | **Done** | Every SKILL.md has a "Surface routing" paragraph naming CLI commands and the mirroring MCP tools, with the package-wide rule (CLI primary for terminal agents; MCP for shell-less hosts or protocol-level session safety) defined once in `ppds-core` §"Surface routing". MCP tool names are validated against a captured `tools/list` response. |
| AC-04 | Each non-cross-cutting skill has a `## Skill boundaries` section | **Done** | Present in all six non-cross-cutting skills (`ppds-query`, `ppds-plugins`, `ppds-solutions-alm`, `ppds-metadata`, `ppds-data`, `ppds-webresources`). `ppds-core` is the cross-cutting router and carries a "Where to go next" routing table instead. |
| AC-05 | Multi-environment confirmation rule documented as hard rule | **Done** | `ppds-core` §"The safety model — hard rules", rule 2 (restate exact target URL + user confirmation when a session spans environments or uses `--environment` overrides; Production always prompts), grounded in the shipped engine behavior (`cross_env_dml_policy` default ReadOnly, Production protection level). Note: the service-layer confirmation pattern child (#1015) is not yet shipped in PPDS; the skill documents today's shipped guards plus the agent-side hard rule. |
| AC-06 | Static eval suite verifies skills authoring conventions (frontmatter shape, code-block correctness, version-bump consistency) | **Done** | [evals/check_skills.py](evals/check_skills.py), zero-dependency. Checks frontmatter shape/naming/description triggers; code-fence balance + language tags; **every `ppds` invocation and flag in skill bodies and hand-written references must exist in the captured `--help` surface** (`captured-help/`); MCP tool-name existence; relative link integrity; version consistency (skills ↔ captured CLI/MCP versions ↔ plugin.json ↔ marketplace.json); generated-reference freshness; 150-line cap. CI: [.github/workflows/evals.yml](.github/workflows/evals.yml). |
| AC-07 | Install + smoke-test instructions in package README | **Done** | [README.md](README.md): Claude Code (plugin marketplace + manual copy paths) and Copilot CLI (`~/.copilot/skills/`, repo `.github/skills/` etc.), plus the "List my Dataverse environments" smoke test. |
| AC-08 | Distribution path identified and documented | **Done (decision documented)** | Self-hosted GitHub repo as a Claude Code plugin marketplace (`.claude-plugin/marketplace.json` → `/plugin marketplace add joshsmithxrm/ppds-skills`), consumable by Copilot CLI via standard Agent Skills directories. Marketplace listings (claude-plugins-official / awesome-copilot) are a follow-up once the repo is public. |

## Anti-hallucination architecture (design ratification §2)

- `tools/capture_cli_help.py` walks the released CLI's full command tree
  (271 nodes at 1.2.0-rc.6) into `captured-help/*.txt` + `manifest.json`.
- `tools/capture_mcp_tools.py` records the released MCP server's actual
  `tools/list` response (41 tools at 1.0.0) — the repo-HEAD docs describe a
  larger future surface, so the live capture is the truth source.
- `tools/generate_flag_tables.py` embeds the captures **verbatim** into
  `skills/*/references/cli-*.md` (23 files) and `mcp-tools.md`.
- The eval suite closes the loop: hand-written prose cannot reference a
  command, flag, or MCP tool that the captures don't contain. During
  authoring it caught 9 real errors (e.g. a `--filter` that is actually
  `--assembly`, an `--orphaned` that is actually `--unbound`, and a package
  README example — deploy `--assembly` — that drifted from the shipped CLI).

## Out of scope (per #1011)

No routing into MS Skills / MS MCP / Python SDKs; no replacement of the
main repo's internal `.claude/skills/`; no Power Apps / Power Automate /
business-rules skills.
