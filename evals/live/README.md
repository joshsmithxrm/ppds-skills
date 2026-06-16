# Live (behavioral) evals

The static suite (`evals/check_skills.py`) proves the skills only *cite* real
commands and flags. This suite measures the other half: given a real task, does
an agent that has the skills loaded actually **load the right skill** and
**route PPDS correctly** — instead of inventing a flag or reaching for `pac`?

It mirrors the approach Microsoft's Dataverse-skills package uses for its
LLM-judged scenario evals: per-skill task prompts with `SKILL_LOADED`,
`CONTAINS` / `NOT_CONTAINS`, and `semantic` assertions at priority levels.

```
evals/live/
  scenarios/<skill>.json   one scenario file per skill (the test cases)
  run_live_evals.py        runner: drive agent -> assert -> aggregate by priority
  drivers.py               AgentRun + ClaudeCodeDriver (headless `claude -p`)
  judge.py                 zero-dep Anthropic-API judge for `semantic` assertions
  _selftest.py             offline harness test + scenario validation (no key/CLI)
  schema.md                the scenario-file schema
```

## What runs where

| | When | Needs | Cost |
|--|------|-------|------|
| `_selftest.py` | **every PR** (inside `skill-evals`) | nothing | free |
| `run_live_evals.py` | **manual only** (`live-evals` workflow, or locally) | `claude` CLI + `ANTHROPIC_API_KEY` | billed |

`_selftest.py` unit-tests the parser and assertion engine **and** validates that
every `ppds ...` / `ppds_*` fragment any scenario asserts actually exists in
`captured-help/` — so a scenario can't assert a hallucinated flag and stay
green. That is the load-bearing, always-on guarantee; the billed run is the
quality-deepening layer.

## Running the billed suite locally

```bash
dotnet tool install -g @anthropic-ai/claude-code   # or: npm i -g @anthropic-ai/claude-code
export ANTHROPIC_API_KEY=sk-ant-...                # judge + Claude Code auth
python evals/live/run_live_evals.py                # all skills
python evals/live/run_live_evals.py --filter ppds-query
python evals/live/run_live_evals.py --list         # list scenarios, run nothing
```

Degrades gracefully: no `claude` on PATH → the whole suite is **skipped**
(exit 0); `ANTHROPIC_API_KEY` unset → `semantic` assertions are **skipped**
while the deterministic ones still run.

### How it stays safe

The driver runs `claude -p` in **plan permission mode** — read-only. The agent
loads skills and *proposes* `ppds ...` commands, but nothing executes against
Dataverse, and no auth profile is provided either. The suite judges the
commands the agent **constructs**, never their results.

### Knobs (env)

| var | default | meaning |
|-----|---------|---------|
| `PPDS_LIVE_MODEL` | `opus` | model passed to `claude --model` |
| `PPDS_LIVE_PERMISSION_MODE` | `plan` | `claude --permission-mode` |
| `PPDS_LIVE_MAX_TURNS` | `12` | `claude --max-turns` |
| `PPDS_LIVE_TIMEOUT` | `240` | per-scenario wall-clock seconds |
| `PPDS_JUDGE_MODEL` | `claude-opus-4-8` | semantic-judge model |

## Priority levels

A failing **P1** assertion fails the run (exit 1) — these are the load-bearing
routing facts. **P2 / P3** are reported but non-fatal (nuance the agent should
get, but that shouldn't gate CI). See `schema.md` for the full assertion spec.

## Adding a scenario

Edit the relevant `scenarios/<skill>.json` (schema in `schema.md`), then run
`python evals/live/_selftest.py` — it will reject any assertion that references
a command or flag not in the captured surface before you ever spend a token.
