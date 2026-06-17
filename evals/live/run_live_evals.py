#!/usr/bin/env python3
"""Live (behavioral) eval runner for the PPDS skills package — issue #4.

Where the static suite (`evals/check_skills.py`) proves the skills *cite* only
real commands/flags, this suite measures whether an agent, given a real task,
actually loads the right skill and routes PPDS correctly. It drives a headless
agent that has the skills loaded, captures what it proposes, and checks
per-scenario assertions:

  - skill_loaded  — deterministic: the expected skill triggered
  - contains / not_contains — deterministic substring checks (right routing;
    no `pac`, no hallucinated flags)
  - semantic      — LLM-judged: safety model respected, CLI/MCP routing sound

Priority levels: a failing P1 fails the run (exit 1); P2/P3 are informational.
Cost-aware and opt-in — it shells out to `claude` for both the agent under
test and the semantic judge (so a Claude Code subscription is enough; no
Anthropic API key). It degrades gracefully: if `claude` is not on PATH the
suite is skipped (exit 0); the semantic judge skips the same way, while the
deterministic assertions still run.

Usage:
    python evals/live/run_live_evals.py [--filter ppds-query] [--list]
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import judge  # noqa: E402
from drivers import AgentRun, ClaudeCodeDriver  # noqa: E402

SCENARIOS_DIR = HERE / "scenarios"
VALID_PRIORITIES = {"P1", "P2", "P3"}


@dataclass
class AssertionResult:
    type: str
    priority: str
    passed: bool
    skipped: bool
    detail: str


# ---------------------------------------------------------------------------
# Assertion evaluation
# ---------------------------------------------------------------------------


def _needles(a: dict) -> list[str]:
    if "value" in a:
        return [str(a["value"])]
    if "any" in a:
        return [str(x) for x in a["any"]]
    if "all" in a:
        return [str(x) for x in a["all"]]
    return []


def _present(needle: str, hay: str, ignore_case: bool) -> bool:
    return (needle.lower() in hay.lower()) if ignore_case else (needle in hay)


def evaluate(a: dict, run: AgentRun, default_priority: str) -> AssertionResult:
    atype = a.get("type", "")
    priority = a.get("priority", default_priority)
    if priority not in VALID_PRIORITIES:
        priority = default_priority
    scope = a.get("scope", "all")
    ignore_case = bool(a.get("ignore_case", False))

    if atype == "skill_loaded":
        want = a.get("skill", "")
        ok = want in run.skills_invoked
        return AssertionResult(
            atype, priority, ok, False,
            f"expected skill {want!r}; loaded {run.skills_invoked or '[]'}",
        )

    if atype in ("contains", "not_contains"):
        hay = run.scope_text(scope)
        needles = _needles(a)
        mode = "all" if "all" in a else "any"  # value -> single -> any semantics
        hits = [n for n in needles if _present(n, hay, ignore_case)]
        if atype == "contains":
            ok = (len(hits) == len(needles)) if mode == "all" else bool(hits)
            return AssertionResult(
                atype, priority, ok, False,
                f"scope={scope} mode={mode} found {hits or '[]'} of {needles}",
            )
        # not_contains: fail if any needle present
        ok = not hits
        return AssertionResult(
            atype, priority, ok, False,
            f"scope={scope} forbidden present: {hits or '[]'}",
        )

    if atype == "semantic":
        if not judge.available():
            return AssertionResult(atype, priority, False, True, "no `claude` CLI")
        v = judge.judge(
            a.get("rubric", ""), run.prompt, run.command_strings, run.final_text
        )
        if v.error:
            return AssertionResult(atype, priority, False, True, f"judge error: {v.error}")
        if v.skipped:
            return AssertionResult(atype, priority, False, True, v.reason)
        return AssertionResult(
            atype, priority, v.passed, False, f"({v.confidence}) {v.reason}",
        )

    return AssertionResult(atype or "unknown", priority, False, False, "unknown assertion type")


# ---------------------------------------------------------------------------
# Loading + running
# ---------------------------------------------------------------------------


def load_scenarios(filter_skill: str | None) -> list[dict]:
    files = sorted(SCENARIOS_DIR.glob("*.json"))
    out = []
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        if filter_skill and data.get("skill") != filter_skill:
            continue
        data["_file"] = f.name
        out.append(data)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--filter", help="only run scenarios for this skill")
    ap.add_argument("--list", action="store_true", help="list scenarios and exit")
    args = ap.parse_args()

    files = load_scenarios(args.filter)
    if not files:
        sys.stderr.write(f"no scenario files in {SCENARIOS_DIR}\n")
        return 1

    if args.list:
        for data in files:
            for sc in data.get("scenarios", []):
                print(f"{data['skill']:20} {sc.get('priority','P2'):3} {sc['id']}")
        return 0

    driver = ClaudeCodeDriver()
    ok, why = driver.available()
    if not ok:
        sys.stderr.write(f"note: live evals skipped — {why}\n")
        return 0

    if not judge.available():
        sys.stderr.write(
            "note: no `claude` CLI — semantic assertions will be skipped\n"
        )

    p1_fail = 0
    p1_total = 0
    soft_fail = 0
    skipped = 0
    n_scenarios = 0

    for data in files:
        skill = data["skill"]
        for sc in data.get("scenarios", []):
            n_scenarios += 1
            default_priority = sc.get("priority", "P2")
            print(f"\n=== [{skill}] {sc['id']} ===")
            run = driver.run(sc["prompt"])
            if not run.ok:
                print(f"  DRIVER ERROR: {run.error}")
            print(
                f"  skills_loaded={run.skills_invoked or '[]'} "
                f"commands={len(run.command_strings)}"
            )
            for a in sc.get("assertions", []):
                r = evaluate(a, run, default_priority)
                if r.priority == "P1":
                    p1_total += 1
                if r.skipped:
                    skipped += 1
                    mark = "SKIP"
                elif r.passed:
                    mark = "PASS"
                else:
                    mark = "FAIL"
                    if r.priority == "P1":
                        p1_fail += 1
                    else:
                        soft_fail += 1
                print(f"  [{mark}] {r.priority} {r.type}: {r.detail}")

    print(
        f"\n{n_scenarios} scenarios | P1 {p1_total - p1_fail}/{p1_total} passed "
        f"| {soft_fail} soft (P2/P3) failures | {skipped} skipped"
    )
    if p1_fail:
        sys.stderr.write(f"\nFAIL: {p1_fail} P1 assertion(s) failed\n")
        return 1
    print("OK: all P1 assertions passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
