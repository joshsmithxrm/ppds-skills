#!/usr/bin/env python3
"""Re-capture the PPDS surface and bump skill frontmatter to match it.

Assumes the *target* `ppds` / `ppds-mcp-server` are already installed (the CI
workflow or a maintainer does the `dotnet tool update`). This script does the
repo-side half of the re-capture loop in one idempotent step:

  1. tools/capture_cli_help.py      -> captured-help/ + manifest.json
  2. tools/capture_mcp_tools.py     -> captured-help/mcp-tools.json
  3. tools/generate_flag_tables.py  -> skills/*/references/*.md
  4. bump metadata.ppds_cli_version_tested / ppds_mcp_version_tested in every
     skills/*/SKILL.md to the freshly captured versions.

Run against the *currently installed* CLI it is a no-op (zero diff) — that is
the property the automation relies on to prove the machinery works without a
new release. After this runs, `python evals/check_skills.py` should pass; any
prose changes (dropping `--prerelease`, stale rc mentions) remain a manual,
human-reviewed step and are NOT touched here.

Usage:
    python tools/recapture.py              # full: capture + bump
    python tools/recapture.py --no-capture # bump only, from existing manifests
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
HELP_DIR = ROOT / "captured-help"
SKILLS_DIR = ROOT / "skills"

CAPTURE_STEPS = [
    "capture_cli_help.py",
    "capture_mcp_tools.py",
    "generate_flag_tables.py",
]

# Matches a quoted frontmatter version line, preserving indentation + quote char.
_FM_LINE = r'^(?P<indent>\s*){key}:\s*(?P<q>["\']?)(?P<val>[^"\'\r\n]*)(?P=q)\s*$'


def run_captures() -> None:
    for step in CAPTURE_STEPS:
        sys.stderr.write(f"==> {step}\n")
        subprocess.run([sys.executable, str(TOOLS / step)], cwd=ROOT, check=True)


def captured_versions() -> tuple[str, str]:
    cli = json.loads((HELP_DIR / "manifest.json").read_text(encoding="utf-8"))[
        "cli_version"
    ]
    mcp = json.loads((HELP_DIR / "mcp-tools.json").read_text(encoding="utf-8"))[
        "server"
    ]["version"]
    return cli, mcp


def mcp_already_satisfies(current: str, captured: str) -> bool:
    """Same rule check_skills.py applies: an exact match or a dotted prefix
    (frontmatter '1.0.0' satisfies a captured '1.0.0.0')."""
    return captured == current or captured.startswith(current + ".")


def bump_line(text: str, key: str, new_val: str) -> tuple[str, str | None]:
    """Replace the `key:` frontmatter value, returning (text, old_val|None)."""
    pat = re.compile(_FM_LINE.format(key=re.escape(key)), re.MULTILINE)
    m = pat.search(text)
    if not m:
        return text, None
    old = m.group("val")
    q = m.group("q") or '"'
    replacement = f'{m.group("indent")}{key}: {q}{new_val}{q}'
    return text[: m.start()] + replacement + text[m.end():], old


def bump_frontmatter(cli_version: str, mcp_version: str) -> int:
    changed = 0
    for skill in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        original = text

        text, old_cli = bump_line(text, "ppds_cli_version_tested", cli_version)
        if old_cli is None:
            sys.stderr.write(f"WARNING: no ppds_cli_version_tested in {skill.name}\n")

        # Only rewrite the MCP pin if the current value no longer satisfies the
        # captured server version — preserves the intentional '1.0.0' vs
        # '1.0.0.0' shortening the gate already accepts.
        cur_mcp_m = re.search(
            _FM_LINE.format(key="ppds_mcp_version_tested"), text, re.MULTILINE
        )
        cur_mcp = cur_mcp_m.group("val") if cur_mcp_m else None
        if cur_mcp is not None and not mcp_already_satisfies(cur_mcp, mcp_version):
            text, _ = bump_line(text, "ppds_mcp_version_tested", mcp_version)
            sys.stderr.write(
                f"{skill.parent.name}: mcp {cur_mcp!r} -> {mcp_version!r}\n"
            )

        if text != original:
            skill.write_text(text, encoding="utf-8")
            changed += 1
            if old_cli not in (None, cli_version):
                sys.stderr.write(
                    f"{skill.parent.name}: cli {old_cli!r} -> {cli_version!r}\n"
                )
    return changed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--no-capture",
        action="store_true",
        help="skip the capture scripts; bump frontmatter from existing manifests",
    )
    args = ap.parse_args()

    if not args.no_capture:
        run_captures()

    cli_version, mcp_version = captured_versions()
    changed = bump_frontmatter(cli_version, mcp_version)

    sys.stderr.write(
        f"\ndone: captured CLI {cli_version}, MCP {mcp_version}; "
        f"{changed} SKILL.md file(s) updated.\n"
    )
    if "-rc." not in cli_version:
        sys.stderr.write(
            "NOTE: pin is now a STABLE version. check_skills.py no longer flags "
            "rc mentions in prose — manually drop any `--prerelease` guidance and "
            "stale rc references in README.md / DESIGN.md / skills/*/SKILL.md.\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
