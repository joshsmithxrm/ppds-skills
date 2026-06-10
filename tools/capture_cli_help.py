#!/usr/bin/env python3
"""Capture the full `ppds` CLI --help surface by walking the command tree.

Output goes to captured-help/ as one .txt file per command node, plus
captured-help/manifest.json recording the CLI version the capture was
generated from. The eval suite and the flag-table generator both consume
this tree; skills never hand-write flag references.

Usage:
    python tools/capture_cli_help.py [--root-cmd ppds] [--out captured-help]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

COMMANDS_HEADER = re.compile(r"^Commands:\s*$")


def run_help(argv: list[str]) -> str:
    """Run `<argv> --help` and return help text (stderr banner included)."""
    result = subprocess.run(
        argv + ["--help"],
        capture_output=True,
        text=True,
        timeout=120,
        encoding="utf-8",
        errors="replace",
    )
    out = result.stdout or ""
    if result.stderr and result.stderr.strip() and not out:
        out = result.stderr
    return out


def parse_subcommands(help_text: str) -> list[str]:
    """Extract subcommand names from a System.CommandLine help screen."""
    subs: list[str] = []
    in_commands = False
    for line in help_text.splitlines():
        if COMMANDS_HEADER.match(line):
            in_commands = True
            continue
        if not in_commands:
            continue
        if line.strip() == "":
            continue
        if not line.startswith("  "):
            in_commands = False
            continue
        # Wrapped description continuation lines are indented deeper than
        # the two-space command column.
        if line.startswith("    "):
            continue
        token = line[2:]
        # Cut at the two-space gap separating name column from description.
        name_col = re.split(r"\s{2,}", token)[0]
        # Strip <arg> placeholders: "import <path>" -> "import"
        name_part = name_col.split("<")[0].strip()
        # "ls, list" -> canonical long alias is the last one
        aliases = [a.strip() for a in name_part.split(",") if a.strip()]
        if not aliases:
            continue
        canonical = aliases[-1]
        if canonical.startswith("-"):
            continue
        subs.append(canonical)
    return subs


def node_filename(path_parts: list[str]) -> str:
    return "_".join(path_parts) + ".txt"


def walk(root_cmd: str, out_dir: Path) -> dict:
    captured: dict[str, list[str]] = {}
    queue: list[list[str]] = [[root_cmd]]
    while queue:
        parts = queue.pop(0)
        rel = " ".join(parts)
        sys.stderr.write(f"capturing: {rel} --help\n")
        text = run_help(parts)
        if not text.strip():
            sys.stderr.write(f"  WARNING: empty help for {rel}\n")
            continue
        (out_dir / node_filename(parts)).write_text(text, encoding="utf-8")
        subs = parse_subcommands(text)
        captured[rel] = subs
        for s in subs:
            queue.append(parts + [s])
    return captured


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root-cmd", default="ppds")
    ap.add_argument("--out", default="captured-help")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    version_raw = subprocess.run(
        [args.root_cmd, "--version"],
        capture_output=True,
        text=True,
        timeout=120,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()
    # "1.2.0-rc.4+044d93aec2..." -> "1.2.0-rc.4"
    version = version_raw.split("+")[0].strip()

    tree = walk(args.root_cmd, out_dir)

    manifest = {
        "tool": args.root_cmd,
        "cli_version": version,
        "cli_version_raw": version_raw,
        "command_tree": tree,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    sys.stderr.write(
        f"done: {len(tree)} command nodes captured at CLI version {version}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
