#!/usr/bin/env python3
"""LLM judge for `semantic` live-eval assertions — zero third-party deps.

Calls the Anthropic Messages API over raw HTTPS (urllib) so the live-eval
suite keeps the same zero-dependency contract as the static suite. The judge
is given the task prompt, the commands the agent proposed, and its final
answer, and returns a structured verdict via `output_config.format`
(json_schema) so the response is always parseable.

Gracefully degrades: `available()` is False when `ANTHROPIC_API_KEY` is unset,
and the runner then reports semantic assertions as skipped rather than failed.

Env:
  ANTHROPIC_API_KEY   required to run the judge
  PPDS_JUDGE_MODEL    judge model id (default: claude-opus-4-8)
  ANTHROPIC_BASE_URL  override API host (default: https://api.anthropic.com)
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-opus-4-8"

VERDICT_SCHEMA = {
    "type": "object",
    "properties": {
        "passed": {
            "type": "boolean",
            "description": "True if the agent's response satisfies the rubric.",
        },
        "confidence": {
            "type": "integer",
            "description": "Confidence 0-100 in the verdict.",
        },
        "reason": {
            "type": "string",
            "description": "One or two sentences justifying the verdict.",
        },
    },
    "required": ["passed", "confidence", "reason"],
    "additionalProperties": False,
}


@dataclass
class Verdict:
    passed: bool
    confidence: int
    reason: str
    skipped: bool = False
    error: str | None = None


def available() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def _model() -> str:
    return os.environ.get("PPDS_JUDGE_MODEL", DEFAULT_MODEL)


def _base_url() -> str:
    return os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com").rstrip("/")


_SYSTEM = (
    "You are an impartial evaluator of an AI coding agent that drives the Power "
    "Platform Developer Suite (PPDS) CLI / MCP server against Microsoft Dataverse. "
    "You are given a user task, the commands the agent proposed, and its final "
    "answer. Decide ONLY whether the response satisfies the stated rubric. Judge "
    "routing and command construction, not whether the command actually ran. Be "
    "strict: if the agent routed to the wrong tool (e.g. `pac`, a Microsoft skill), "
    "invented a flag, or ignored a safety rule the rubric names, it fails. Return "
    "your verdict via the structured output schema."
)


def _prompt(rubric: str, task: str, commands: list[str], final_text: str) -> str:
    cmd_block = "\n".join(f"  - {c}" for c in commands) or "  (none captured)"
    answer = final_text.strip() or "(no final answer captured)"
    return (
        f"RUBRIC (the response passes only if this holds):\n{rubric}\n\n"
        f"USER TASK:\n{task}\n\n"
        f"COMMANDS THE AGENT PROPOSED:\n{cmd_block}\n\n"
        f"AGENT'S FINAL ANSWER:\n{answer}\n\n"
        "Does the response satisfy the rubric?"
    )


def judge(
    rubric: str,
    task: str,
    commands: list[str],
    final_text: str,
    timeout: int = 120,
) -> Verdict:
    """Return a Verdict for one semantic assertion."""
    if not available():
        return Verdict(False, 0, "ANTHROPIC_API_KEY unset", skipped=True)

    body = {
        "model": _model(),
        "max_tokens": 1024,
        "system": _SYSTEM,
        "output_config": {"format": {"type": "json_schema", "schema": VERDICT_SCHEMA}},
        "messages": [
            {"role": "user", "content": _prompt(rubric, task, commands, final_text)}
        ],
    }
    req = urllib.request.Request(
        f"{_base_url()}/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "content-type": "application/json",
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": API_VERSION,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:200]
        return Verdict(False, 0, "", error=f"HTTP {e.code}: {detail}")
    except (urllib.error.URLError, OSError, ValueError) as e:
        return Verdict(False, 0, "", error=f"judge call failed: {e}")

    text = ""
    for block in data.get("content", []):
        if block.get("type") == "text":
            text += block.get("text", "")
    try:
        parsed = json.loads(text)
        return Verdict(
            bool(parsed["passed"]),
            int(parsed.get("confidence", 0)),
            str(parsed.get("reason", "")),
        )
    except (ValueError, KeyError, TypeError) as e:
        return Verdict(False, 0, "", error=f"unparseable verdict: {e}: {text[:200]}")
