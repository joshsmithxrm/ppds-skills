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

`scope` selects what text the assertion looks at (default `all`):

| scope | what it covers |
|-------|----------------|
| `commands` | the command strings the agent proposed: `Bash` tool inputs, plus any `ppds_*` MCP tool names it called |
| `text` | the agent's final user-facing answer |
| `all` | commands + text + the raw transcript |

### `skill_loaded`
Deterministic. Passes if the named skill was triggered during the run.
```jsonc
{ "type": "skill_loaded", "skill": "ppds-query", "priority": "P1" }
```

### `contains`
Deterministic substring match within `scope`. Use `value` for one substring or
`any` / `all` for a list (`any` = at least one present; `all` = every one
present). `ignore_case` (default `false`) lower-cases both sides.
```jsonc
{ "type": "contains", "scope": "commands", "any": ["ppds query sql", "ppds_query_sql"], "priority": "P1" }
{ "type": "contains", "scope": "commands", "value": "count(", "ignore_case": true, "priority": "P2" }
```

### `not_contains`
Deterministic. Fails if any listed substring appears in `scope`. Use for
anti-patterns (routing to `pac`, MS skills, or a hallucinated flag).
```jsonc
{ "type": "not_contains", "scope": "all", "any": ["pac ", " --limit"], "priority": "P1" }
```

### `semantic`
LLM-judged via `judge.py`. `rubric` states, in one sentence, what a correct
response must do. The judge sees the prompt, the proposed commands, and the
final answer, and returns pass/fail + confidence + reason. **Skipped (not
failed)** when no `ANTHROPIC_API_KEY` is set, so the deterministic layer still
runs everywhere.
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
- **Prefer `scope: "all"` for command fragments.** The default driver runs in
  `plan` permission mode (read-only — nothing executes against Dataverse), so
  the agent's proposed `ppds ...` command usually lands in its plan text rather
  than an executed `Bash` tool input. `scope: "all"` matches it in either
  place; reserve `scope: "commands"` for runs with execution enabled.
- Prefer 1 `skill_loaded` + 1–2 `contains` (the routing target) + 1
  `not_contains` (the anti-pattern) + at most 1 `semantic` per scenario.
- Make `P1` assertions the load-bearing routing facts; reserve `P2`/`P3` for
  nuance the agent *should* get but that shouldn't fail CI.
