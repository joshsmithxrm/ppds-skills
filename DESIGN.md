# Design notes

Why this package looks the way it does.

## The problem: flag hallucination

AI coding agents are good at *intent* ("export this solution") but routinely
invent CLI flags that don't exist, or fall back to a different tool (`pac`)
when unsure. For a package that drives destructive operations against live
Dataverse environments, a hallucinated flag is worse than a refusal.

## The approach: the reference IS the real `--help`

Rather than hand-write flag tables (which drift from the tool), this package
generates them verbatim from the released CLI:

- `tools/capture_cli_help.py` walks the CLI's full command tree (271 nodes at
  1.2.0) into `captured-help/*.txt` + `manifest.json`.
- `tools/capture_mcp_tools.py` records the MCP server's actual `tools/list`
  response (41 tools at 1.0.0).
- `tools/generate_flag_tables.py` embeds those captures **verbatim** into
  `skills/*/references/cli-*.md` and `mcp-tools.md`.

The eval suite (`evals/check_skills.py`) then closes the loop: hand-written
prose cannot reference a command, flag, or MCP tool the captures don't
contain. During authoring this caught 9 real errors — e.g. a `--filter` that
is actually `--assembly`, an `--orphaned` that is actually `--unbound`, and a
README example (`deploy --assembly`) that had drifted from the shipped CLI.

## Skill decomposition

Seven skills map onto PPDS's noun groups:

| Area | Skill |
|------|-------|
| connect/auth + environment management | `ppds-core` |
| query (SQL / FetchXML) + DML | `ppds-query` |
| plugin work + plugin traces | `ppds-plugins` |
| solutions / ALM | `ppds-solutions-alm` |
| metadata authoring | `ppds-metadata` |
| data CRUD / bulk | `ppds-data` |
| web resources | `ppds-webresources` |

`ppds-core` is the cross-cutting router and the home of the safety model; the
other six are domain skills, each ending in a `## Skill boundaries` routing
table. Because skill loading is the host's discretion, the highest-blast-radius
operations (DML, truncate/delete, solution import) restate their confirmation
contract inline rather than relying on `ppds-core` being in context.

## Scope

**In scope:** the PPDS CLI and MCP surfaces over Microsoft Dataverse.

**Out of scope:** routing into Microsoft's own skills/MCP or the Python SDKs;
Power Apps / Power Automate / business-rules authoring; replacing the engine
repository's internal skills.

## Versioning and the captured surface

Each `SKILL.md` pins the exact CLI/MCP versions it was generated against in
frontmatter, enforced by the eval suite against the captured manifest. The
captures track a specific release; see [CONTRIBUTING.md](CONTRIBUTING.md) for
the re-capture process.
