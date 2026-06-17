# Live-eval scenario schema

Each `scenarios/<skill>.json` file is one object:

```jsonc
{
  "skill": "ppds-query",            // the skill these scenarios primarily exercise
  "description": "Free-text note for maintainers.",
  "scenarios": [ /* Scenario objects */ ]
}
```

A **Scenario** is one task prompt plus a list of assertions:

```jsonc
{
  "id": "count-accounts",           // unique within the file; used in reports
  "priority": "P1",                 // default priority for assertions that omit one
  "prompt": "How many account records are in my Dataverse environment?",
  "assertions": [ /* Assertion objects */ ]
}
```

`prompt` is what the agent is asked. The harness drives an agent that has the
PPDS skills loaded, captures what it proposes (skills triggered + commands it
would run), and checks the assertions. **Nothing is executed against
Dataverse** — the agent runs with tool execution disabled, so the harness
judges the *commands it constructs*, not their results.

## Assertion types

Every assertion has a `type` and an optional `priority` (`P1` | `P2` | `P3`;
inherits the scenario's `priority` if omitted). **A failing `P1` fails the
run** (exit 1); `P2`/`P3` are reported but non-fatal.

**Priority convention** (calibrated against real headless runs): `P1` gates
only the signals that are *reliably observable* when driving `claude -p` in
plan mode — **command-level routing** (`contains` of a `ppds <command>`) and
**anti-patterns** (`not_contains` over actual commands). Everything that an
agent can get right without it showing up deterministically is `P2`
(informational): `skill_loaded` (the agent often routes correctly from a
skill's in-context *description* without opening the full file), exact-flag
`contains` (plan prose names the command but not always every flag), and
MCP-tool-name `contains` (the CLI driver can't emit MCP calls). The
LLM-judged `semantic` assertion is where flag- and intent-level correctness is
checked rigorously — make it `P1` when that nuance is the whole point (it is
*skipped*, never failed, when no `claude` CLI is available).

`scope` selects what text the assertion looks at (default `all`):

| scope | what it covers |
|-------|----------------|
| `commands` | the command strings the agent proposed: `Bash` tool inputs, plus any `ppds_*` MCP tool names it called |
| `text` | the agent's final user-facing answer |
| `all` | commands + text — the agent's **output**. It deliberately excludes the raw transcript, which embeds the loaded `SKILL.md` text; otherwise a `not_contains` for `pac ` would always fail against a skill body that documents "don't use `pac`", and a `contains` could pass on the skill text rather than on the agent actually choosing the command |

### `skill_loaded`
Deterministic. Passes if the named skill was triggered during the run.
```jsonc
{ "type": "skill_loaded", "skill": "ppds-query", "priority": "P2" }
```

### `contains`
Deterministic substring match within `scope`. Use `value` for one substring or
`any` / `all` for a list (`any` = at least one present; `all` = every one
present). `ignore_case` (default `false`) lower-cases both sides.
```jsonc
{ "type": "contains", "scope": "all", "any": ["ppds query sql", "ppds_query_sql"], "priority": "P1" }
{ "type": "contains", "scope": "all", "value": "count(", "ignore_case": true, "priority": "P2" }
```

### `not_contains`
Deterministic. Fails if any listed substring appears in `scope`. Use for
anti-patterns (routing to `pac`, MS skills, or a hallucinated flag).
```jsonc
{ "type": "not_contains", "scope": "commands", "any": ["pac ", " --limit"], "priority": "P1" }
```

### `semantic`
LLM-judged via `judge.py`, which drives the **same `claude` CLI** the agent
runs on — so it works on a Claude Code subscription, no API key. `rubric`
states, in one sentence, what a correct response must do. The judge sees the
prompt, the proposed commands, and the final answer, and returns pass/fail +
confidence + reason. **Skipped (not failed)** when no `claude` CLI is
available, so the deterministic layer still runs everywhere.
```jsonc
{ "type": "semantic",
  "rubric": "Routes to the SQL->FetchXML engine with a COUNT aggregate and does not invent a --limit flag (the engine paginates, there is no --limit on `ppds query sql`).",
  "priority": "P2" }
```

## Authoring rules

- **Every command fragment in a `contains` assertion must be a real PPDS
  surface** — a command/flag present in `captured-help/`, or an `ppds_*` MCP
  tool in `mcp-tools.json`. The review step validates this; an eval that
  asserts a hallucinated flag is itself a bug.
- **`contains` uses `scope: "all"`; `not_contains` uses `scope: "commands"`.**
  The driver runs in `plan` mode (read-only), so a correct agent describes its
  intended `ppds ...` command in its plan prose — and often *names* an
  anti-pattern there too, to explain it's avoiding it ("use `ppds auth create`,
  not `pac auth create`"). Positive routing (`contains`) should count that
  naming as evidence, so it looks at the whole output (`all`). Negative
  anti-patterns (`not_contains`) must NOT penalize a correct agent for
  mentioning `pac` in prose — they match only the agent's actual proposed
  command invocations (`commands`). The LLM-judged `semantic` assertion is the
  robust anti-pattern check when prose nuance matters.
- Prefer 1 `skill_loaded` + 1–2 `contains` (the routing target) + 1
  `not_contains` (the anti-pattern) + at most 1 `semantic` per scenario.
- Make `P1` assertions the load-bearing routing facts; reserve `P2`/`P3` for
  nuance the agent *should* get but that shouldn't fail CI.
