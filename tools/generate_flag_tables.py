#!/usr/bin/env python3
"""Generate per-skill CLI reference files from the captured --help tree.

Reads captured-help/manifest.json + the per-command .txt files and emits
skills/<skill>/references/cli-<group>.md with the captured help embedded
VERBATIM. No hand-transcription of flags ever happens in this repo: the
reference files are regenerated from a fresh capture whenever the CLI
version changes.

Usage:
    python tools/capture_cli_help.py          # refresh captured-help/
    python tools/generate_flag_tables.py      # refresh skill references
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# skill -> list of top-level ppds command groups whose captured help is
# embedded in that skill's references directory (one file per group).
SKILL_GROUPS: dict[str, list[str]] = {
    "ppds-core": ["auth", "env", "users", "roles", "logs"],
    "ppds-query": ["query"],
    "ppds-plugins": ["plugins", "plugintraces", "custom-apis", "service-endpoints"],
    "ppds-solutions-alm": [
        "solutions",
        "importjobs",
        "environmentvariables",
        "connectionreferences",
        "connections",
        "deployment-settings",
        "publish",
    ],
    "ppds-metadata": ["metadata", "schema", "views", "forms"],
    "ppds-data": ["data"],
    "ppds-webresources": ["webresources"],
}

ROOT = Path(__file__).resolve().parent.parent
HELP_DIR = ROOT / "captured-help"
SKILLS_DIR = ROOT / "skills"


def load_manifest() -> dict:
    return json.loads((HELP_DIR / "manifest.json").read_text(encoding="utf-8"))


def node_filename(cmd_path: str) -> str:
    return cmd_path.replace(" ", "_") + ".txt"


def collect_nodes(tree: dict, group: str) -> list[str]:
    """All command paths under `ppds <group>`, breadth-first, parents first."""
    prefix = f"ppds {group}"
    nodes = [p for p in tree if p == prefix or p.startswith(prefix + " ")]
    return sorted(nodes, key=lambda p: (p.count(" "), p))


def emit_group_file(skill: str, group: str, tree: dict, version: str) -> Path | None:
    nodes = collect_nodes(tree, group)
    if not nodes:
        sys.stderr.write(f"WARNING: no captured commands for group '{group}'\n")
        return None

    lines: list[str] = []
    lines.append(f"# `ppds {group}` — command and flag reference")
    lines.append("")
    lines.append(
        f"<!-- GENERATED from `ppds ... --help` output, CLI version {version}. -->"
    )
    lines.append(
        "<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py"
        " && python tools/generate_flag_tables.py -->"
    )
    lines.append("")
    lines.append(
        f"Captured verbatim from PPDS CLI **{version}**. Every flag below is real; "
        "any flag not listed here does not exist on that command."
    )
    lines.append("")
    for node in nodes:
        help_file = HELP_DIR / node_filename(node)
        if not help_file.is_file():
            sys.stderr.write(f"WARNING: missing capture for '{node}'\n")
            continue
        text = help_file.read_text(encoding="utf-8").rstrip()
        lines.append(f"## `{node}`")
        lines.append("")
        lines.append("```text")
        lines.append(text)
        lines.append("```")
        lines.append("")

    out = SKILLS_DIR / skill / "references" / f"cli-{group}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def emit_mcp_tools_file() -> Path | None:
    """Emit the MCP tool reference from the captured tools/list response."""
    src = HELP_DIR / "mcp-tools.json"
    if not src.is_file():
        sys.stderr.write("WARNING: captured-help/mcp-tools.json missing; skipping\n")
        return None
    data = json.loads(src.read_text(encoding="utf-8"))
    server = data.get("server", {})
    version = server.get("version", "unknown")
    lines: list[str] = []
    lines.append("# `ppds-mcp-server` — tool reference")
    lines.append("")
    lines.append(
        f"<!-- GENERATED from a live tools/list call against ppds-mcp-server"
        f" {version}. -->"
    )
    lines.append(
        "<!-- Do not edit by hand. Regenerate: python tools/capture_mcp_tools.py"
        " && python tools/generate_flag_tables.py -->"
    )
    lines.append("")
    lines.append(
        f"Captured from the released **ppds-mcp-server {version}** "
        f"({data.get('tool_count')} tools). Any `ppds_*` tool not listed here "
        "does not exist on this server version."
    )
    lines.append("")
    lines.append("| Tool | Description |")
    lines.append("|------|-------------|")
    for t in data.get("tools", []):
        desc = " ".join((t.get("description") or "").split())
        lines.append(f"| `{t['name']}` | {desc} |")
    out = SKILLS_DIR / "ppds-core" / "references" / "mcp-tools.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> int:
    manifest = load_manifest()
    tree: dict = manifest["command_tree"]
    version: str = manifest["cli_version"]
    written = []
    for skill, groups in SKILL_GROUPS.items():
        for group in groups:
            out = emit_group_file(skill, group, tree, version)
            if out:
                written.append(out)
    mcp_out = emit_mcp_tools_file()
    if mcp_out:
        written.append(mcp_out)
    for p in written:
        sys.stderr.write(f"wrote {p.relative_to(ROOT)}\n")
    sys.stderr.write(f"done: {len(written)} reference files at CLI {version}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
