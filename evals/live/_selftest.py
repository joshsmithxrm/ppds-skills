#!/usr/bin/env python3
"""Offline self-test for the live-eval harness — no API key, no `claude` CLI.

Three layers, all deterministic so they run in CI:
  1. stream-json parser — a synthetic transcript yields the right skills,
     commands, and final text.
  2. assertion engine — each assertion type returns the expected verdict.
  3. scenario validation — every scenarios/*.json conforms to the schema AND
     every `ppds ...` / `ppds_*` fragment it asserts resolves against the
     captured surface (an eval must not assert a hallucinated flag).

Exit 0 = all pass; 1 = failures.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "evals"))

import check_skills  # noqa: E402  (reuse captured-surface validation)
from drivers import AgentRun, parse_stream_json  # noqa: E402
from run_live_evals import VALID_PRIORITIES, evaluate  # noqa: E402

failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


# ---------------------------------------------------------------------------
# 1. Parser
# ---------------------------------------------------------------------------

FIXTURE = "\n".join(
    json.dumps(o)
    for o in [
        {"type": "system", "subtype": "init"},
        {
            "type": "assistant",
            "message": {
                "content": [
                    {"type": "text", "text": "I'll use the query skill."},
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "input": {"command": "ppds-query"},
                    },
                ]
            },
        },
        {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Bash",
                        "input": {"command": "ppds query sql \"SELECT COUNT(*) FROM account\""},
                    }
                ]
            },
        },
        {"type": "result", "result": "There are 42 accounts."},
    ]
)


def test_parser() -> None:
    run = parse_stream_json(FIXTURE, "How many accounts?")
    check("ppds-query" in run.skills_invoked, f"parser: skill not detected: {run.skills_invoked}")
    check(
        any("ppds query sql" in c for c in run.command_strings),
        f"parser: command not captured: {run.command_strings}",
    )
    check("42 accounts" in run.final_text, f"parser: final text wrong: {run.final_text!r}")
    check(len(run.tool_calls) == 2, f"parser: tool_call count {len(run.tool_calls)}")


# ---------------------------------------------------------------------------
# 2. Assertion engine
# ---------------------------------------------------------------------------


def test_assertions() -> None:
    run = parse_stream_json(FIXTURE, "How many accounts?")

    cases = [
        ({"type": "skill_loaded", "skill": "ppds-query"}, True),
        ({"type": "skill_loaded", "skill": "ppds-data"}, False),
        ({"type": "contains", "scope": "all", "value": "ppds query sql"}, True),
        ({"type": "contains", "scope": "commands", "value": "count(", "ignore_case": True}, True),
        ({"type": "contains", "scope": "commands", "value": "count("}, False),  # case-sensitive
        ({"type": "contains", "any": ["pac ", "ppds query sql"]}, True),
        ({"type": "contains", "all": ["ppds query sql", "account"]}, True),
        ({"type": "contains", "all": ["ppds query sql", "nonexistent"]}, False),
        ({"type": "not_contains", "scope": "all", "any": ["pac ", " --limit"]}, True),
        ({"type": "not_contains", "scope": "all", "value": "ppds query sql"}, False),
    ]
    for a, want in cases:
        r = evaluate(a, run, "P1")
        check(r.passed == want and not r.skipped, f"assert {a} -> {r.passed} (want {want}): {r.detail}")

    # semantic without a key must skip, never hard-fail
    r = evaluate({"type": "semantic", "rubric": "x"}, run, "P2")
    check(r.skipped, "semantic without API key should skip")

    # priority inheritance
    r = evaluate({"type": "skill_loaded", "skill": "ppds-query"}, run, "P3")
    check(r.priority == "P3", f"priority inheritance: {r.priority}")


# ---------------------------------------------------------------------------
# 3. Scenario validation (against the captured surface)
# ---------------------------------------------------------------------------

VALID_TYPES = {"skill_loaded", "contains", "not_contains", "semantic"}
VALID_SCOPES = {"commands", "text", "all"}


def _validate_command_needle(needle: str, file_path: Path, label: str, tree: dict, mcp_tools: set) -> None:
    """Validate a positive (`contains`) routing target against the captured
    surface. `file_path` must be a real path under ROOT — `check_skills.err()`
    calls `path.relative_to(ROOT)`, so a bare label would crash it."""
    n = needle.strip()
    if n.startswith("ppds_") or n.startswith("mcp__"):
        tool = n.split()[0]
        if tool not in mcp_tools:
            failures.append(f"{label}: MCP tool {tool!r} not in captured tools/list")
        return
    if n == "ppds" or n.startswith("ppds ") or n.startswith("ppds-mcp-server"):
        before = len(check_skills.errors)
        check_skills.check_ppds_invocation(file_path, 0, n, tree)
        for e in check_skills.errors[before:]:
            failures.append(f"{label}: asserts unreal surface — {e}")


def test_scenarios() -> None:
    scen_dir = HERE / "scenarios"
    files = sorted(scen_dir.glob("*.json")) if scen_dir.is_dir() else []
    if not files:
        sys.stderr.write("note: no scenario files yet — skipping scenario validation\n")
        return

    manifest = check_skills.load_manifest()
    tree = manifest["command_tree"]
    mcp = check_skills.load_mcp()
    mcp_tools = {t["name"] for t in mcp.get("tools", [])}
    skill_dirs = {p.name for p in (ROOT / "skills").glob("ppds-*") if p.is_dir()}

    seen_ids: set[str] = set()
    for f in files:
        where = f.name
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            failures.append(f"{where}: invalid JSON: {e}")
            continue
        skill = data.get("skill")
        if skill not in skill_dirs:
            failures.append(f"{where}: skill {skill!r} is not a real skill dir")
        for sc in data.get("scenarios", []):
            sid = sc.get("id")
            if not sid:
                failures.append(f"{where}: a scenario is missing 'id'")
            elif sid in seen_ids:
                failures.append(f"{where}: duplicate scenario id {sid!r}")
            else:
                seen_ids.add(sid)
            if not sc.get("prompt"):
                failures.append(f"{where}:{sid}: missing prompt")
            if sc.get("priority", "P2") not in VALID_PRIORITIES:
                failures.append(f"{where}:{sid}: bad scenario priority")
            assertions = sc.get("assertions", [])
            if not assertions:
                failures.append(f"{where}:{sid}: no assertions")
            for a in assertions:
                atype = a.get("type")
                if atype not in VALID_TYPES:
                    failures.append(f"{where}:{sid}: bad assertion type {atype!r}")
                if a.get("priority", "P2") not in VALID_PRIORITIES:
                    failures.append(f"{where}:{sid}: bad assertion priority")
                if a.get("scope", "all") not in VALID_SCOPES:
                    failures.append(f"{where}:{sid}: bad scope {a.get('scope')!r}")
                if atype == "skill_loaded" and a.get("skill") not in skill_dirs:
                    failures.append(f"{where}:{sid}: skill_loaded names unreal skill {a.get('skill')!r}")
                if atype == "semantic" and not a.get("rubric"):
                    failures.append(f"{where}:{sid}: semantic assertion missing rubric")
                if atype in ("contains", "not_contains"):
                    needles = []
                    for key in ("value", "any", "all"):
                        if key in a:
                            needles = a[key] if isinstance(a[key], list) else [a[key]]
                    if not needles:
                        failures.append(f"{where}:{sid}: {atype} has no value/any/all")
                    # Only POSITIVE routing targets must exist in the captured
                    # surface. `not_contains` needles are anti-patterns —
                    # deliberately forbidden strings (`pac ...`, `ppds env
                    # switch`, invented flags) — and must NOT be validated.
                    if atype == "contains":
                        for n in needles:
                            _validate_command_needle(str(n), f, f"{where}:{sid}", tree, mcp_tools)


def main() -> int:
    test_parser()
    test_assertions()
    test_scenarios()
    if failures:
        for fmsg in failures:
            sys.stderr.write(f"FAIL {fmsg}\n")
        sys.stderr.write(f"\n{len(failures)} self-test failure(s)\n")
        return 1
    print("OK: live-eval harness self-test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
