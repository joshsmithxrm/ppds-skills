"""Pure CLI help/version validation and exact shown-alias expansion.

Safe for the artifact writer: this module performs no I/O or process launch.
"""
from __future__ import annotations

import re
from collections import deque

WORD = re.compile(r"[a-z][a-z0-9-]*")
NUM = r"(?:0|[1-9][0-9]*)"
PRE = r"(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
VERSION = re.compile(rf"{NUM}\.{NUM}\.{NUM}(?:-{PRE}(?:\.{PRE})*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?")
MAX_NODES = 1000
MAX_DEPTH = 12
MAX_TEXT_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 32 * 1024 * 1024


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def effective_version(raw: str, expected: str | None = None) -> str:
    require(isinstance(raw, str) and VERSION.fullmatch(raw) is not None, "Invalid CLI version output")
    version = raw.split("+", 1)[0]
    if expected is not None:
        require(isinstance(expected, str) and VERSION.fullmatch(expected) is not None, "Invalid requested CLI version")
        # --version is the informational assembly version, whose +build suffix
        # may identify a source commit rather than the selected NuGet package.
        require(version == expected.split("+", 1)[0], "Effective CLI version differs from requested package")
    return version


def parse_command_groups(help_text: str) -> list[list[str]]:
    require(isinstance(help_text, str) and bool(help_text.strip()), "Empty help text")
    require("Usage:\n" in help_text.replace("\r\n", "\n"), "Missing CLI Usage section")
    groups: list[list[str]] = []
    seen: set[str] = set()
    inside = False
    headers = 0
    for line in help_text.splitlines():
        if re.fullmatch(r"Commands:\s*", line):
            headers += 1
            require(headers == 1, "Duplicate Commands section")
            inside = True
            continue
        if not inside or not line.strip():
            continue
        if not line.startswith("  "):
            inside = False
            continue
        if line.startswith("    "):
            require(bool(groups), "Command continuation without command")
            continue
        column = re.split(r"\s{2,}", line[2:])[0]
        name_column = column.split("<", 1)[0].strip()
        aliases = [value.strip() for value in name_column.split(",")]
        require(bool(aliases) and all(WORD.fullmatch(value) for value in aliases), "Invalid command column")
        require(len(set(aliases)) == len(aliases) and not seen.intersection(aliases), "Duplicate command spelling")
        seen.update(aliases)
        groups.append(aliases)
    require(not headers or bool(groups), "Empty Commands section")
    return groups


def parse_subcommands(help_text: str) -> list[str]:
    """Compatibility helper: return only each row's executed spelling."""
    return [group[0] for group in parse_command_groups(help_text)]


def node_filename(path_parts: list[str]) -> str:
    require(bool(path_parts) and all(WORD.fullmatch(part) for part in path_parts), "Unsafe command path")
    return "_".join(path_parts) + ".txt"


def expand_aliases(canonical_help: dict[str, str]) -> tuple[dict, dict, dict]:
    """Pure expansion: return command_tree, path->text, path->executed path."""
    require(isinstance(canonical_help, dict) and "ppds" in canonical_help, "Missing root help")
    require(len(canonical_help) <= MAX_NODES, "Canonical node bound exceeded")
    groups = {path: parse_command_groups(text) for path, text in canonical_help.items()}
    for path in canonical_help:
        parts = path.split(" ")
        require(parts[0] == "ppds" and len(parts) <= MAX_DEPTH, "Invalid canonical command depth/root")
        node_filename(parts)
    tree, texts, sources = {}, {}, {}
    queue = deque([("ppds", "ppds")])
    used: set[str] = set()
    while queue:
        path, source = queue.popleft()
        require(path not in tree, "Duplicate expanded command path")
        require(len(tree) < MAX_NODES and len(path.split(" ")) <= MAX_DEPTH, "Expanded command bound exceeded")
        require(source in canonical_help, "Missing canonical child help")
        used.add(source)
        tree[path] = [alias for group in groups[source] for alias in group]
        texts[path] = canonical_help[source]
        sources[path] = source
        for group in groups[source]:
            for alias in group:
                queue.append((path + " " + alias, source + " " + group[0]))
    require(used == set(canonical_help), "Unreachable canonical help node")
    return tree, texts, sources
