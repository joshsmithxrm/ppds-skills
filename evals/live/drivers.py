#!/usr/bin/env python3
"""Agent drivers for the live-eval suite — zero third-party deps.

A driver runs a task prompt against an agent that has the PPDS skills loaded
and returns a normalized `AgentRun`: which skills triggered, the commands the
agent proposed, and its final answer. The runner's deterministic assertions
read only the `AgentRun`, so adding another host (e.g. Copilot CLI) is just
another driver that returns the same shape.

`ClaudeCodeDriver` shells out to `claude -p ... --output-format stream-json`.
It is intentionally defensive about the transcript shape (Claude Code's
stream-json has evolved) and degrades to a clear "unavailable" result when the
CLI is absent, so the suite can be invoked anywhere.

Safety: the default permission mode is `plan` — read-only. The agent loads
skills and *proposes* `ppds ...` commands without executing anything against
Dataverse. No auth profile is provided either, so even with execution enabled
a command cannot mutate an environment.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_DIR = ROOT / "skills"

# The driver runs in a bare sandbox — no auth profile, no real files, no
# selected environment. Without framing, the agent correctly stops to ask
# ("I can't see that CSV", "which environment?") and never emits the routing
# command, so the eval can't observe what it would actually run. This preamble
# isolates the signal the suite measures — routing — by asking for the concrete
# command under the assumption that prerequisites are met. It does NOT tell the
# agent which command to use.
# NOTE: this MUST stay a single line (no newlines). On Windows a newline inside
# an argv string truncates the `claude -p <prompt>` argument, so the task after
# the newline is dropped and the agent answers "the task is missing".
PLANNING_PREAMBLE = (
    "You are advising a developer on exactly how to perform the task below with "
    "the Power Platform Developer Suite (PPDS). This is a planning exercise: "
    "assume an auth profile is already created and the correct environment is "
    "selected, and that any files or paths mentioned already exist. Do NOT stop "
    "to ask clarifying questions and do NOT run exploratory shell commands to "
    "discover prerequisites; give the specific `ppds ...` command(s) you would "
    "run, including the flags, and call out any safety steps (dry-run, "
    "confirmation) inline. The task: "
)


@dataclass
class AgentRun:
    prompt: str
    final_text: str = ""
    tool_calls: list[dict] = field(default_factory=list)  # [{name, input}]
    skills_invoked: list[str] = field(default_factory=list)
    command_strings: list[str] = field(default_factory=list)
    raw: str = ""
    ok: bool = True
    error: str | None = None

    def scope_text(self, scope: str) -> str:
        """Concatenated text for an assertion `scope`.

        `all` is the agent's OUTPUT — the commands it proposed plus its final
        answer. It deliberately EXCLUDES `self.raw` (the whole transcript),
        because the transcript embeds the loaded SKILL.md text: a `not_contains`
        for `pac ` would otherwise always fail against a skill body that itself
        documents "don't use `pac`", and a `contains` would pass on the skill
        text rather than on the agent actually choosing the command. `raw` is
        kept only for debugging.
        """
        commands = "\n".join(self.command_strings)
        if scope == "commands":
            return commands
        if scope == "text":
            return self.final_text
        return "\n".join([commands, self.final_text])  # "all" = agent output


# ---------------------------------------------------------------------------
# stream-json parsing (tolerant of multiple Claude Code transcript shapes)
# ---------------------------------------------------------------------------

# Known skill names, used to identify which skill a `Skill` tool-use loaded
# (the exact input field name is not contractually documented, so we scan the
# input values rather than key on a field name).
_KNOWN_SKILLS = sorted(p.name for p in SKILLS_DIR.glob("ppds-*") if p.is_dir())


def _iter_tool_uses(obj: dict):
    """Yield {name, input} tool_use blocks from any known transcript node."""
    # Shape A: full assistant message — {"type":"assistant","message":{"content":[...]}}
    msg = obj.get("message")
    if isinstance(msg, dict):
        for block in msg.get("content", []) or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield {"name": block.get("name", ""), "input": block.get("input", {})}
    # Shape B: wrapped raw API event — {"type":"stream_event","event":{...}}
    event = obj.get("event")
    if isinstance(event, dict):
        cb = event.get("content_block")
        if isinstance(cb, dict) and cb.get("type") == "tool_use":
            yield {"name": cb.get("name", ""), "input": cb.get("input", {})}
    # Shape C: a bare content_block_start at top level
    if obj.get("type") == "content_block_start":
        cb = obj.get("content_block")
        if isinstance(cb, dict) and cb.get("type") == "tool_use":
            yield {"name": cb.get("name", ""), "input": cb.get("input", {})}


def _iter_text(obj: dict):
    """Yield assistant text fragments from any known transcript node."""
    msg = obj.get("message")
    if isinstance(msg, dict):
        for block in msg.get("content", []) or []:
            if isinstance(block, dict) and block.get("type") == "text":
                yield block.get("text", "")
    if obj.get("type") == "result" and isinstance(obj.get("result"), str):
        yield obj["result"]


def _input_values(value) -> list[str]:
    """Flatten a tool input (dict/list/scalar) into a list of string values."""
    out: list[str] = []
    if isinstance(value, dict):
        for v in value.values():
            out.extend(_input_values(v))
    elif isinstance(value, list):
        for v in value:
            out.extend(_input_values(v))
    elif value is not None:
        out.append(str(value))
    return out


def _command_from_tool(name: str, inp) -> str | None:
    """Best-effort command string for a tool_use, for the `commands` scope."""
    if name in ("Bash", "BashOutput"):
        if isinstance(inp, dict) and isinstance(inp.get("command"), str):
            return inp["command"]
    if name.startswith("ppds_") or name.startswith("mcp__"):
        # An MCP tool call — the tool name itself is the routing signal.
        args = " ".join(_input_values(inp))
        return f"{name} {args}".strip()
    return None


def parse_stream_json(text: str, prompt: str) -> AgentRun:
    run = AgentRun(prompt=prompt, raw=text)
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if not isinstance(obj, dict):
            continue
        for tu in _iter_tool_uses(obj):
            run.tool_calls.append(tu)
            name, inp = tu["name"], tu.get("input", {})
            if name == "Skill":
                for val in _input_values(inp):
                    for skill in _KNOWN_SKILLS:
                        if skill in val and skill not in run.skills_invoked:
                            run.skills_invoked.append(skill)
            cmd = _command_from_tool(name, inp)
            if cmd:
                run.command_strings.append(cmd)
            # In plan mode the agent presents its intended commands inside the
            # ExitPlanMode plan rather than executing them — fold it into the
            # final answer so routing assertions see the proposal.
            if name == "ExitPlanMode" and isinstance(inp, dict):
                plan = inp.get("plan")
                if isinstance(plan, str) and plan:
                    run.final_text += "\n" + plan
        for frag in _iter_text(obj):
            if frag:
                run.final_text += frag
    return run


# ---------------------------------------------------------------------------
# Claude Code driver
# ---------------------------------------------------------------------------


def _stage_skills(dest: Path) -> int:
    """Copy the repo's skills into <dest>/.claude/skills for discovery."""
    skills_root = dest / ".claude" / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    n = 0
    for skill_dir in SKILLS_DIR.glob("ppds-*"):
        if skill_dir.is_dir():
            shutil.copytree(skill_dir, skills_root / skill_dir.name)
            n += 1
    return n


class ClaudeCodeDriver:
    """Drives `claude -p` headless with the PPDS skills staged for discovery."""

    name = "claude-code"

    def __init__(
        self,
        model: str | None = None,
        permission_mode: str | None = None,
        max_turns: int = 12,
        timeout: int = 240,
    ):
        self.exe = shutil.which("claude")
        self.model = model or os.environ.get("PPDS_LIVE_MODEL", "opus")
        self.permission_mode = permission_mode or os.environ.get(
            "PPDS_LIVE_PERMISSION_MODE", "plan"
        )
        self.max_turns = int(os.environ.get("PPDS_LIVE_MAX_TURNS", max_turns))
        self.timeout = int(os.environ.get("PPDS_LIVE_TIMEOUT", timeout))

    def available(self) -> tuple[bool, str]:
        if not self.exe:
            return False, "`claude` CLI not on PATH"
        return True, ""

    def run(self, prompt: str) -> AgentRun:
        ok, why = self.available()
        if not ok:
            return AgentRun(prompt=prompt, ok=False, error=why)

        workdir = Path(tempfile.mkdtemp(prefix="ppds-live-"))
        try:
            staged = _stage_skills(workdir)
            if staged == 0:
                return AgentRun(prompt=prompt, ok=False, error="no skills staged")
            argv = [
                self.exe,
                "-p",
                PLANNING_PREAMBLE + prompt,
                "--output-format",
                "stream-json",
                "--verbose",
                "--permission-mode",
                self.permission_mode,
                "--model",
                self.model,
                "--max-turns",
                str(self.max_turns),
            ]
            try:
                proc = subprocess.run(
                    argv,
                    cwd=str(workdir),
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=self.timeout,
                )
            except subprocess.TimeoutExpired as e:
                partial = e.stdout or ""
                run = parse_stream_json(
                    partial if isinstance(partial, str) else "", prompt
                )
                run.ok = False
                run.error = f"timed out after {self.timeout}s"
                return run
            run = parse_stream_json(proc.stdout or "", prompt)
            if not run.tool_calls and not run.final_text:
                run.ok = False
                run.error = (
                    f"empty transcript (exit {proc.returncode}): "
                    f"{(proc.stderr or '')[:200]}"
                )
            return run
        finally:
            shutil.rmtree(workdir, ignore_errors=True)
