#!/usr/bin/env python3
"""Capture CLI help plus explicit alias derivations; never call normal handlers.

Only the first spelling in each command row is executed. Other shown spellings
derive their text from that exact canonical node, including nested alias paths.
Use a fresh --out directory in automation. This recorder never deletes old data.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from collections import deque
from pathlib import Path

from cli_capture_format import (
    MAX_DEPTH, MAX_NODES, MAX_TEXT_BYTES, MAX_TOTAL_BYTES, NUM, PRE, VERSION, WORD,
    effective_version, expand_aliases, node_filename, parse_command_groups,
    parse_subcommands, require,
)


def run_text(argv: list[str]) -> str:
    result = subprocess.run(argv, capture_output=True, text=True, timeout=120,
                            encoding="utf-8", errors="strict", stdin=subprocess.DEVNULL)
    require(result.returncode == 0, "CLI help/version process failed")
    require(not result.stderr, "CLI help/version produced stderr")
    text = result.stdout
    require(isinstance(text, str) and bool(text.strip()), "CLI help/version output is empty")
    require(len(text.encode("utf-8")) <= MAX_TEXT_BYTES, "CLI output exceeds size bound")
    return text


def run_help(argv: list[str]) -> str:
    return run_text(argv + ["--help"])


def capture_tree(root_cmd: str) -> tuple[dict, dict, dict]:
    canonical_help: dict[str, str] = {}
    queue = deque([[]])
    total_bytes = 0
    while queue:
        parts = queue.popleft()
        path = " ".join(["ppds"] + parts)
        require(path not in canonical_help, "Duplicate canonical command path")
        require(len(canonical_help) < MAX_NODES and len(parts) < MAX_DEPTH, "Canonical command bound exceeded")
        sys.stderr.write(f"capturing: {path} --help\n")
        text = run_help([root_cmd] + parts)
        total_bytes += len(text.encode("utf-8"))
        require(total_bytes <= MAX_TOTAL_BYTES, "Total CLI capture size bound exceeded")
        canonical_help[path] = text
        for child in parse_subcommands(text):
            queue.append(parts + [child])
    return expand_aliases(canonical_help)


def write_text(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root-cmd", default="ppds")
    ap.add_argument("--out", default="captured-help")
    ap.add_argument("--expected-version", default=os.environ.get("TARGET_CLI_VERSION"))
    args = ap.parse_args()
    version_raw = run_text([args.root_cmd, "--version"]).strip()
    version = effective_version(version_raw, args.expected_version)
    tree, texts, sources = capture_tree(args.root_cmd)
    counts = {
        "canonical_runtime_capture_count": len(set(sources.values())),
        "alias_expanded_command_path_count": len(sources),
        "alias_derived_path_count": sum(path != source for path, source in sources.items()),
    }
    manifest = {
        "tool": "ppds", "cli_version": version, "cli_version_raw": version_raw,
        "requested_package_version": args.expected_version,
        "capture_platform": f"{platform.system()} {platform.machine()}",
        **counts, "command_tree": tree,
    }
    alias_record = {**counts, "paths": sources,
        "derivation": "Only exact shown spellings of the same canonical parent are expanded; derived text is unchanged canonical help, not an independent alias invocation."}
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for path, text in texts.items():
        write_text(out_dir / node_filename(path.split(" ")), text)
    for filename, data in (("manifest.json", manifest), ("alias-provenance.json", alias_record)):
        write_text(out_dir / filename, json.dumps(data, indent=2) + "\n")
    sys.stderr.write(f"done: {counts['canonical_runtime_capture_count']} actual CLI nodes, {len(tree)} paths at {version}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
