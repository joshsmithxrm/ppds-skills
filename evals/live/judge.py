#!/usr/bin/env python3
"""LLM judge for `semantic` live-eval assertions — drives Claude Code.

The judge runs on the SAME `claude` CLI the driver uses, so the semantic layer
works on a Claude Code subscription with no Anthropic API key. (The driver
already depends on `claude`; requiring a separate `ANTHROPIC_API_KEY` would make
this layer permanently dead in a subscription-only environment.)

The judge prompt embeds the agent's multi-line answer, so it is passed via
STDIN — never as an argv string, where a newline truncates the prompt on
Windows. The judge runs in a clean temp dir with no skills staged, so it is
pure reasoning with no tool use.

Gracefully degrades: `available()` is False when `claude` is not on PATH, and
the runner then reports semantic assertions as skipped rather than failed.

Env:
  PPDS_JUDGE_MODEL    judge model passed to `claude --model` (default: sonnet)
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass

DEFAULT_MODEL = "sonnet"


@dataclass
class Verdict:
    passed: bool
    confidence: int
    reason: str
    skipped: bool = False
    error: str | None = None


def _exe() -> str | None:
    return shutil.which("claude")


def available() -> bool:
    return _exe() is not None


def _model() -> str:
    return os.environ.get("PPDS_JUDGE_MODEL", DEFAULT_MODEL)


_INSTR = (
    "You are an impartial evaluator of an AI coding agent that drives the Power "
    "Platform Developer Suite (PPDS) CLI / MCP server against Microsoft "
    "Dataverse. You are given a user task, the commands the agent proposed, and "
    "its final answer. Decide ONLY whether the agent's response satisfies the "
    "stated rubric. Judge routing and command construction, not whether the "
    "command actually ran. Be strict: if the agent routed to the wrong tool "
    "(`pac`, a Microsoft skill), invented a flag, or ignored a safety rule the "
    "rubric names, it fails."
)


def _prompt(rubric: str, task: str, commands: list[str], final_text: str) -> str:
    cmd_block = "\n".join(f"- {c}" for c in commands) or "(none captured)"
    answer = (final_text or "").strip() or "(no final answer captured)"
    return (
        f"{_INSTR}\n\n"
        f"RUBRIC (the response passes only if this holds):\n{rubric}\n\n"
        f"USER TASK:\n{task}\n\n"
        f"COMMANDS THE AGENT PROPOSED:\n{cmd_block}\n\n"
        f"AGENT'S FINAL ANSWER:\n{answer}\n\n"
        "Respond with ONLY a JSON object, no prose and no markdown fences: "
        '{"passed": true or false, "confidence": 0-100 integer, '
        '"reason": "one or two sentences"}'
    )


def _extract_verdict(text: str) -> Verdict:
    """Pull the first JSON object out of the judge's reply."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return Verdict(False, 0, "", error=f"no JSON in judge reply: {text[:160]}")
    try:
        parsed = json.loads(m.group(0))
        return Verdict(
            bool(parsed["passed"]),
            int(parsed.get("confidence", 0)),
            str(parsed.get("reason", "")),
        )
    except (ValueError, KeyError, TypeError) as e:
        return Verdict(False, 0, "", error=f"unparseable verdict: {e}: {text[:160]}")


def judge(
    rubric: str,
    task: str,
    commands: list[str],
    final_text: str,
    timeout: int = 180,
) -> Verdict:
    """Return a Verdict for one semantic assertion, via `claude -p`."""
    exe = _exe()
    if not exe:
        return Verdict(False, 0, "no `claude` CLI", skipped=True)

    prompt = _prompt(rubric, task, commands, final_text)
    workdir = tempfile.mkdtemp(prefix="ppds-judge-")
    try:
        proc = subprocess.run(
            [
                exe,
                "-p",
                "--output-format",
                "json",
                "--model",
                _model(),
                "--max-turns",
                "1",
            ],
            input=prompt,  # via stdin — avoids the Windows argv-newline truncation
            cwd=workdir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        return Verdict(False, 0, "", error=f"judge call failed: {e}")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    out = (proc.stdout or "").strip()
    if not out:
        return Verdict(False, 0, "", error=f"empty judge reply (exit {proc.returncode})")
    # `--output-format json` wraps the reply in an envelope whose `result` holds
    # the final text; fall back to the raw stdout if it isn't that shape.
    try:
        env = json.loads(out)
        result = env.get("result", out) if isinstance(env, dict) else out
    except ValueError:
        result = out
    return _extract_verdict(result if isinstance(result, str) else json.dumps(result))
