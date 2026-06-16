#!/usr/bin/env python3
"""Static eval suite for the PPDS skills package (AC-06).

Zero-dependency checks, run locally and in CI:

  1. Frontmatter shape — name matches directory, naming rules, description
     length + "Use when" trigger clause, license, version-tested metadata.
  2. Version consistency — metadata.ppds_cli_version_tested must equal the
     CLI version in captured-help/manifest.json; ppds_mcp_version_tested
     must match the captured MCP server version; plugin.json and
     marketplace.json versions must agree.
  3. Code-block correctness — fences balanced and language-tagged; every
     `ppds ...` invocation in code blocks and inline code resolves to a
     command captured in captured-help/, and every `--flag` it uses exists
     in that command's real --help output.
  4. MCP tool names — every `ppds_*` tool mention exists in the captured
     tools/list response (captured-help/mcp-tools.json).
  5. Links — relative markdown links in skill files resolve.
  6. Reference freshness — generated cli-*.md files carry the same CLI
     version as the manifest.
  7. Line cap — SKILL.md files stay within MAX_SKILL_LINES.
  8. Capture freshness — when a `ppds` CLI is on PATH, its `--version` must
     equal the captured manifest version, so captures cannot silently lag the
     installed CLI (the failure that shipped rc.4 tables while rc.6 was
     installed). Skipped (not failed) when `ppds` is absent, preserving the
     zero-dependency contract for minimal CI; set PPDS_SKIP_FRESHNESS=1 to
     force-skip even when the CLI is present.

Exit code 0 = all checks pass; 1 = findings (printed to stderr).

"Wrong | Correct" tables: cells under a column literally named "Wrong" are
exempt from command validation — they exist to show anti-patterns.
"""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
HELP_DIR = ROOT / "captured-help"

MAX_SKILL_LINES = 150
MAX_DESCRIPTION = 1024
MAX_NAME = 64
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MCP_TOOL_RE = re.compile(r"\bppds_[a-z0-9_]+\b")
SHELL_OPERATORS = {"|", "||", "&&", ";", ">", ">>", "<", "2>&1", "&"}
MCP_SERVER_FLAGS = {
    "--read-only",
    "--allowed-env",
    "--profile",
    "--environment",
    "--log-level",
}

errors: list[str] = []


def err(path: Path, line: int | None, msg: str) -> None:
    loc = f"{path.relative_to(ROOT)}"
    if line is not None:
        loc += f":{line}"
    errors.append(f"{loc}: {msg}")


# ---------------------------------------------------------------------------
# Captured surface
# ---------------------------------------------------------------------------


def load_manifest() -> dict:
    return json.loads((HELP_DIR / "manifest.json").read_text(encoding="utf-8"))


def load_mcp() -> dict:
    return json.loads((HELP_DIR / "mcp-tools.json").read_text(encoding="utf-8"))


def options_for(cmd_path: str) -> set[str]:
    """All option aliases (e.g. -f, --output-format) captured for a command."""
    helpfile = HELP_DIR / (cmd_path.replace(" ", "_") + ".txt")
    flags: set[str] = set()
    if not helpfile.is_file():
        return flags
    in_options = False
    for line in helpfile.read_text(encoding="utf-8").splitlines():
        if re.match(r"^Options:\s*$", line):
            in_options = True
            continue
        if in_options:
            if line.strip() and not line.startswith(" "):
                in_options = False
                continue
            m = re.match(r"^  (-[^\s].*?)(?:\s{2,}|$)", line)
            if not m:
                continue
            name_col = m.group(1)
            name_col = name_col.split("<")[0]
            for alias in name_col.split(","):
                alias = alias.strip()
                if alias.startswith("-"):
                    flags.add(alias)
    return flags


# ---------------------------------------------------------------------------
# Frontmatter (strict subset parser — shape itself is part of the contract)
# ---------------------------------------------------------------------------


def parse_frontmatter(text: str, path: Path) -> dict | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        err(path, 1, "missing frontmatter opening '---'")
        return None
    fm: dict = {}
    current_map: dict | None = None
    end = None
    for i, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            end = i
            break
        if not line.strip():
            continue
        if line.startswith("  ") and current_map is not None:
            m = re.match(r"^  ([A-Za-z0-9_-]+):\s*(.*)$", line)
            if not m:
                err(path, i, f"unparseable metadata line: {line!r}")
                continue
            current_map[m.group(1)] = m.group(2).strip().strip('"').strip("'")
        else:
            m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
            if not m:
                err(path, i, f"unparseable frontmatter line: {line!r}")
                continue
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                current_map = {}
                fm[key] = current_map
            else:
                current_map = None
                fm[key] = val.strip('"').strip("'")
    if end is None:
        err(path, 1, "frontmatter never closed with '---'")
        return None
    fm["_body_start"] = end
    return fm


def check_frontmatter(path: Path, fm: dict, cli_version: str, mcp_version: str) -> None:
    skill_dir = path.parent.name
    name = fm.get("name")
    if name != skill_dir:
        err(path, None, f"frontmatter name {name!r} != directory name {skill_dir!r}")
    if not isinstance(name, str) or not NAME_RE.match(name or "") or len(name or "") > MAX_NAME:
        err(path, None, f"name {name!r} violates naming rules (lowercase, hyphens, <={MAX_NAME} chars)")
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        err(path, None, "missing description")
    else:
        if len(desc) > MAX_DESCRIPTION:
            err(path, None, f"description is {len(desc)} chars (max {MAX_DESCRIPTION})")
        if "Use when" not in desc:
            err(path, None, "description must contain a 'Use when ...' trigger clause")
    if fm.get("license") != "MIT":
        err(path, None, f"license must be 'MIT', got {fm.get('license')!r}")
    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        err(path, None, "missing metadata block")
        return
    tested = meta.get("ppds_cli_version_tested")
    if tested != cli_version:
        err(
            path,
            None,
            f"metadata.ppds_cli_version_tested {tested!r} != captured CLI version {cli_version!r}"
            " — re-run tools/capture_cli_help.py + tools/generate_flag_tables.py and update",
        )
    mcp_tested = meta.get("ppds_mcp_version_tested")
    if mcp_tested is None:
        err(path, None, "missing metadata.ppds_mcp_version_tested")
    elif not (mcp_version == mcp_tested or mcp_version.startswith(mcp_tested + ".")):
        err(
            path,
            None,
            f"metadata.ppds_mcp_version_tested {mcp_tested!r} does not match captured MCP server version {mcp_version!r}",
        )


# ---------------------------------------------------------------------------
# ppds invocation validation
# ---------------------------------------------------------------------------


def resolve_command(tokens: list[str], tree: dict) -> tuple[str | None, list[str]]:
    """Longest-prefix match of tokens against the captured command tree.

    Returns (command_path, remaining_tokens). tokens[0] is 'ppds'.
    """
    path = "ppds"
    i = 1
    while i < len(tokens):
        tok = tokens[i]
        if tok.startswith("-") or tok.startswith("<") or tok.startswith("$"):
            break
        candidate = f"{path} {tok}"
        if candidate in tree:
            path = candidate
            i += 1
            continue
        break
    return path, tokens[i:]


def check_ppds_invocation(
    path: Path, line_no: int, cmdline: str, tree: dict
) -> None:
    try:
        tokens = shlex.split(cmdline, posix=True)
    except ValueError:
        tokens = cmdline.split()
    # Trim at shell operators. shlex.split keeps space-less redirections and
    # pipes attached to a token ('ppds auth list >/dev/null' -> '>/dev/null',
    # 'ppds auth list 2>/dev/null' -> '2>/dev/null'), so match the exact
    # operator tokens AND any token that starts with a redirection/pipe/sep.
    argv: list[str] = []
    for tok in tokens:
        if tok in SHELL_OPERATORS or any(
            tok.startswith(op) for op in (">", "2>", "<", "|", "&", ";")
        ):
            break
        argv.append(tok)
    if not argv:
        return

    prog = argv[0]
    if prog == "ppds-mcp-server":
        for tok in argv[1:]:
            if tok.startswith("--") and tok.split("=")[0] not in MCP_SERVER_FLAGS:
                err(path, line_no, f"unknown ppds-mcp-server flag {tok!r}")
        return
    if prog != "ppds":
        return

    cmd_path, rest = resolve_command(argv, tree)
    subcommands = set(tree.get(cmd_path, []))
    # If the next token looks like a subcommand attempt that didn't resolve,
    # the command itself is wrong (hallucinated path).
    if rest and not rest[0].startswith(("-", "<", "$", "'", '"')):
        helpfile = HELP_DIR / (cmd_path.replace(" ", "_") + ".txt")
        help_text = helpfile.read_text(encoding="utf-8") if helpfile.is_file() else ""
        has_args = "Arguments:" in help_text
        if subcommands and rest[0] not in subcommands and not has_args:
            err(
                path,
                line_no,
                f"'{cmd_path} {rest[0]}' is not a captured command"
                f" (known subcommands of '{cmd_path}': {sorted(subcommands)})",
            )
            return
    valid_flags = options_for(cmd_path)
    for tok in rest:
        if not tok.startswith("-"):
            continue
        flag = tok.split("=")[0]
        if flag not in valid_flags:
            err(
                path,
                line_no,
                f"flag {flag!r} not in captured --help for '{cmd_path}'"
                f" (valid: {sorted(valid_flags)})",
            )


def wrong_table_cells(line: str, header_cols: list[str]) -> str:
    """Return the line with cells under a 'Wrong' column blanked out."""
    cells = line.split("|")
    out = []
    for idx, cell in enumerate(cells):
        col = idx - 1  # leading empty cell before first |
        if 0 <= col < len(header_cols) and header_cols[col].strip().lower() == "wrong":
            out.append(" " * len(cell))
        else:
            out.append(cell)
    return "|".join(out)


def check_body(path: Path, text: str, tree: dict, mcp_tools: set[str]) -> None:
    lines = text.splitlines()
    in_fence = False
    fence_lang = ""
    header_cols: list[str] = []
    in_table = False

    for i, raw in enumerate(lines, start=1):
        line = raw

        # Track markdown tables to find 'Wrong' columns
        if not in_fence and line.lstrip().startswith("|"):
            cols = [c.strip().strip("*").strip("`") for c in line.strip().strip("|").split("|")]
            if not in_table:
                header_cols = cols
                in_table = True
            if header_cols and any(h.lower() == "wrong" for h in header_cols):
                line = wrong_table_cells(line, header_cols)
        else:
            in_table = False
            header_cols = []

        # Fences
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence:
                in_fence = True
                fence_lang = stripped[3:].strip()
                if not fence_lang:
                    err(path, i, "code fence missing language tag")
            else:
                in_fence = False
                fence_lang = ""
            continue

        # MCP tool mentions anywhere
        for m in MCP_TOOL_RE.finditer(line):
            tool = m.group(0)
            if tool not in mcp_tools:
                err(path, i, f"MCP tool {tool!r} not in captured tools/list")

        candidates: list[str] = []
        if in_fence and fence_lang in ("bash", "sh", "shell", "console"):
            code = line.strip()
            if code.startswith("#") or not code:
                continue
            if code.startswith("$ "):
                code = code[2:]
            if re.match(r"^(ppds|ppds-mcp-server)\b", code):
                candidates.append(code)
        elif not in_fence:
            for m in re.finditer(r"`([^`]+)`", line):
                span = m.group(1)
                if re.match(r"^(ppds|ppds-mcp-server)\s", span):
                    candidates.append(span)

        for cmdline in candidates:
            # Strip trailing prose markers inside inline code like '...'
            cmdline = cmdline.replace("...", "").replace("…", "")
            check_ppds_invocation(path, i, cmdline, tree)

    if in_fence:
        err(path, len(lines), "unclosed code fence at end of file")


def check_links(path: Path, text: str) -> None:
    for i, line in enumerate(text.splitlines(), start=1):
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", line):
            target = m.group(1).split("#")[0].strip()
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            if not (path.parent / target).exists():
                err(path, i, f"broken relative link: {target}")


def check_generated_refs(cli_version: str, mcp_version: str) -> None:
    for ref in SKILLS_DIR.glob("*/references/cli-*.md"):
        head = ref.read_text(encoding="utf-8")[:600]
        if "GENERATED" in head and f"CLI version {cli_version}" not in head:
            err(
                ref,
                None,
                f"generated reference is stale (expected CLI version {cli_version})"
                " — re-run tools/generate_flag_tables.py",
            )
    for ref in SKILLS_DIR.glob("*/references/mcp-tools.md"):
        head = ref.read_text(encoding="utf-8")[:600]
        if "GENERATED" in head and f"ppds-mcp-server {mcp_version}" not in head:
            err(
                ref,
                None,
                f"generated reference is stale (expected MCP version {mcp_version})"
                " — re-run tools/capture_mcp_tools.py + tools/generate_flag_tables.py",
            )


def check_plugin_versions() -> None:
    plugin_file = ROOT / ".claude-plugin" / "plugin.json"
    marketplace_file = ROOT / ".claude-plugin" / "marketplace.json"
    if not plugin_file.is_file():
        err(plugin_file, None, "missing plugin manifest")
        return
    plugin = json.loads(plugin_file.read_text(encoding="utf-8"))
    if marketplace_file.is_file():
        marketplace = json.loads(marketplace_file.read_text(encoding="utf-8"))
        for entry in marketplace.get("plugins", []):
            if entry.get("name") == plugin.get("name"):
                if entry.get("version") not in (None, plugin.get("version")):
                    err(
                        marketplace_file,
                        None,
                        f"marketplace version {entry.get('version')!r} !="
                        f" plugin.json version {plugin.get('version')!r}",
                    )


def installed_cli_version(tool: str = "ppds") -> str | None:
    """`<tool> --version` with +build metadata stripped, or None if absent."""
    exe = shutil.which(tool)
    if not exe:
        return None
    try:
        result = subprocess.run(
            [exe, "--version"],
            capture_output=True,
            text=True,
            timeout=60,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return (result.stdout or "").strip().split("+")[0].strip() or None


def check_capture_freshness(cli_version: str) -> None:
    """Fail if the installed `ppds` CLI version differs from the captures.

    Opportunistic: when no `ppds` is on PATH (e.g. minimal CI) the check is
    skipped, keeping the suite zero-dependency. When the CLI *is* present, a
    mismatch means the captured surface no longer matches the tool the skills
    are meant to drive — re-run the capture pipeline before shipping.
    """
    if os.environ.get("PPDS_SKIP_FRESHNESS"):
        sys.stderr.write("note: capture-freshness check skipped (PPDS_SKIP_FRESHNESS)\n")
        return
    installed = installed_cli_version()
    if installed is None:
        sys.stderr.write(
            "note: capture-freshness check skipped (no `ppds` on PATH)\n"
        )
        return
    if installed != cli_version:
        err(
            HELP_DIR / "manifest.json",
            None,
            f"captured CLI version {cli_version!r} != installed `ppds --version`"
            f" {installed!r} — re-run tools/capture_cli_help.py +"
            " tools/capture_mcp_tools.py + tools/generate_flag_tables.py and bump"
            " metadata.ppds_cli_version_tested in skills/*/SKILL.md",
        )


def main() -> int:
    manifest = load_manifest()
    tree: dict = manifest["command_tree"]
    cli_version: str = manifest["cli_version"]
    mcp = load_mcp()
    mcp_version = mcp.get("server", {}).get("version", "")
    mcp_tools = {t["name"] for t in mcp.get("tools", [])}

    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        err(SKILLS_DIR, None, "no skills found")

    for skill in skill_files:
        text = skill.read_text(encoding="utf-8")
        total_lines = len(text.splitlines())
        if total_lines > MAX_SKILL_LINES:
            err(skill, None, f"SKILL.md is {total_lines} lines (max {MAX_SKILL_LINES})")
        fm = parse_frontmatter(text, skill)
        if fm:
            check_frontmatter(skill, fm, cli_version, mcp_version)
            body = "\n".join(text.splitlines()[fm["_body_start"]:])
        else:
            body = text
        check_body(skill, body, tree, mcp_tools)
        check_links(skill, text)

    # Hand-written references get the same body checks (generated ones are
    # verbatim captures — exempt).
    for ref in sorted(SKILLS_DIR.glob("*/references/*.md")):
        head = ref.read_text(encoding="utf-8")[:600]
        if "GENERATED" in head:
            continue
        text = ref.read_text(encoding="utf-8")
        check_body(ref, text, tree, mcp_tools)
        check_links(ref, text)

    check_generated_refs(cli_version, mcp_version)
    check_plugin_versions()
    check_capture_freshness(cli_version)

    if errors:
        for e in errors:
            sys.stderr.write(f"FAIL {e}\n")
        sys.stderr.write(f"\n{len(errors)} finding(s)\n")
        return 1
    print(f"OK: {len(skill_files)} skills validated against CLI {cli_version}, MCP {mcp_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
