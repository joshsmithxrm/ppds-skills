#!/usr/bin/env python3
"""Build/validate a bounded JSON data handoff; never execute artifact content.

The writer uses apply only. It imports the pure MCP format validator, not a
capture script or generator. Package hashes are producer observations, not
independent package authenticity or publication attestations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import xml.etree.ElementTree as ET

from mcp_capture_format import decode_json, fixed_requests, validate_capture
from cli_capture_format import expand_aliases

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE = 4 * 1024 * 1024
MAX_BUNDLE = 32 * 1024 * 1024
GROUPS = {
    "ppds-core": ["auth", "env", "users", "roles", "logs"],
    "ppds-query": ["query"],
    "ppds-plugins": ["plugins", "plugintraces", "custom-apis", "service-endpoints"],
    "ppds-solutions-alm": ["solutions", "importjobs", "environmentvariables",
        "connectionreferences", "connections", "deployment-settings", "publish", "flows"],
    "ppds-metadata": ["metadata", "schema", "views", "forms"],
    "ppds-data": ["data"], "ppds-webresources": ["webresources"],
}
REFERENCES = {"skills/%s/references/cli-%s.md" % (skill, group)
              for skill, groups in GROUPS.items() for group in groups}
REFERENCES.add("skills/ppds-core/references/mcp-tools.md")
CAPTURE_JSON = {"manifest.json", "alias-provenance.json", "mcp-tools.json",
    "mcp-protocol-frames.json", "mcp-protocol-requests.json", "mcp-capture-receipt.json"}
CAPTURE_DATA = CAPTURE_JSON | {"mcp-stdout.jsonl", "mcp-stderr.txt"}
SCRIPTS = {"capture_cli_help.py", "cli_capture_format.py", "capture_mcp_tools.py", "mcp_capture_format.py",
           "generate_flag_tables.py", "recapture.py", "recapture_artifact.py"}
SOURCE_FILES = {"tools/" + name for name in SCRIPTS} | {
    ".github/workflows/recapture-on-release.yml", "evals/check_skills.py"}
VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?", re.ASCII)
WORD = re.compile(r"[a-z][a-z0-9-]*", re.ASCII)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def same_json(left, right):
    # Python considers True == 1; JSON protocol values must remain distinct.
    return json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(right, sort_keys=True, separators=(",", ":"))


def exact_keys(value, keys):
    need(isinstance(value, dict) and set(value) == set(keys), "Unexpected object fields")


def digest(value, length=64):
    return isinstance(value, str) and re.fullmatch("[0-9a-f]{%d}" % length, value) is not None


def regular(path, limit=MAX_FILE):
    """No links/reparse points at any existing component, including destinations."""
    for part in (path,) + tuple(path.parents):
        if part.exists() or part.is_symlink():
            info = part.lstat()
            need(not stat.S_ISLNK(info.st_mode) and
                 not getattr(info, "st_file_attributes", 0) & 0x400, "Linked path refused")
    need(path.is_file(), "Missing regular file: " + str(path))
    need(path.stat().st_size <= limit, "File exceeds data limit")
    return path.read_bytes()


def json_file(path):
    return decode_json(regular(path))


def binding(environment):
    names = {"repository": "GITHUB_REPOSITORY", "source_sha": "GITHUB_SHA",
        "source_tree": "CAPTURE_SOURCE_TREE", "workflow_ref": "GITHUB_WORKFLOW_REF",
        "run_id": "GITHUB_RUN_ID", "run_attempt": "GITHUB_RUN_ATTEMPT",
        "cli_version": "TARGET_CLI_VERSION", "mcp_version": "TARGET_MCP_VERSION"}
    result = {key: environment.get(name, "") for key, name in names.items()}
    need(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", result["repository"]), "Bad repository")
    need(digest(result["source_sha"], 40) and digest(result["source_tree"], 40), "Bad source binding")
    need(result["workflow_ref"].startswith(result["repository"] +
        "/.github/workflows/recapture-on-release.yml@refs/heads/"), "Bad workflow binding")
    for key in ("run_id", "run_attempt"):
        need(re.fullmatch(r"[1-9][0-9]*", result[key]), "Bad run binding")
    for key in ("cli_version", "mcp_version"):
        need(len(result[key]) <= 100 and VERSION.fullmatch(result[key]), "Bad version binding")
    return result


def source_pins(root):
    return {name: sha(regular(root / name)) for name in sorted(SOURCE_FILES)}


def capture_paths(manifest):
    tree = manifest.get("command_tree")
    need(isinstance(tree, dict) and "ppds" in tree and 1 <= len(tree) <= 1000, "Bad CLI command tree")
    paths = set()
    for command, children in tree.items():
        words = command.split(" ")
        need(words[0] == "ppds" and len(words) <= 12 and all(WORD.fullmatch(w) for w in words),
             "Bad CLI command path")
        need(isinstance(children, list) and all(isinstance(c, str) and WORD.fullmatch(c) for c in children)
             and len(children) == len(set(children)), "Bad CLI children")
        if len(words) > 1:
            parent = " ".join(words[:-1])
            need(parent in tree and words[-1] in tree[parent], "Disconnected CLI command")
        need(all(command + " " + c in tree for c in children), "Missing CLI child")
        name = "captured-help/" + "_".join(words) + ".txt"
        need(name not in paths, "CLI path collision")
        paths.add(name)
    return paths | {"captured-help/" + name for name in CAPTURE_DATA} | REFERENCES


def package_receipt(store, package, version, binary):
    package_root = store / package.lower()
    need(package_root.is_dir(), "Installed package store missing")
    candidates = list(package_root.rglob("*.nuspec"))
    need(len(candidates) == 1, "Use an isolated one-version tool installation")
    spec = ET.fromstring(regular(candidates[0]))
    metadata = next((node for node in spec if node.tag.rsplit("}", 1)[-1] == "metadata"), None)
    need(metadata is not None, "Missing package metadata")
    fields = {node.tag.rsplit("}", 1)[-1]: node for node in metadata}
    actual = fields["version"].text
    need(fields["id"].text.lower() == package.lower() and
         actual.split("+", 1)[0] == version.split("+", 1)[0], "Installed package identity differs")
    files = {}
    for path in sorted(package_root.rglob("*")):
        if path.is_dir():
            need(not path.is_symlink() and not getattr(path.lstat(), "st_file_attributes", 0) & 0x400,
                 "Linked package directory")
        else:
            # Installed dependency binaries can exceed the capture text limit.
            need(not path.is_symlink() and not getattr(path.lstat(), "st_file_attributes", 0) & 0x400,
                 "Linked package file")
            files[path.relative_to(package_root).as_posix()] = sha(path.read_bytes())
    need(1 <= len(files) <= 3000 and any(p.endswith("/" + binary) for p in files), "Missing installed tool binary")
    repository = fields.get("repository")
    return {"package_id": package, "package_version": actual,
        "repository_url": repository.attrib.get("url") if repository is not None else None,
        "repository_commit": repository.attrib.get("commit") if repository is not None else None,
        "installed_files_sha256": files}


def pack(stage, store, root, expected):
    manifest = json_file(stage / "captured-help/manifest.json")
    files = {}
    for name in sorted(capture_paths(manifest)):
        data = regular(stage / name)
        files[name] = {"sha256": sha(data), "text": data.decode("utf-8")}
    packet = {"schema_version": 1, "binding": expected, "source_sha256": source_pins(root),
        "package_observations": {
            "cli": package_receipt(store, "PPDS.Cli", expected["cli_version"], "ppds.dll"),
            "mcp": package_receipt(store, "PPDS.Mcp", expected["mcp_version"], "ppds-mcp-server.dll")},
        "files": files}
    validate(packet, expected, root)
    return packet


def validate(packet, expected, root):
    exact_keys(packet, {"schema_version", "binding", "source_sha256", "package_observations", "files"})
    need(type(packet["schema_version"]) is int and packet["schema_version"] == 1, "Unsupported bundle")
    need(packet["binding"] == expected, "Artifact source/run/attempt/pair mismatch")
    need(packet["source_sha256"] == source_pins(root), "Producer source differs from trusted writer source")
    exact_keys(packet["package_observations"], {"cli", "mcp"})
    for role, package, binary in (("cli", "PPDS.Cli", "ppds.dll"), ("mcp", "PPDS.Mcp", "ppds-mcp-server.dll")):
        record = packet["package_observations"][role]
        exact_keys(record, {"package_id", "package_version", "repository_url", "repository_commit", "installed_files_sha256"})
        need(record["package_id"] == package and isinstance(record["package_version"], str) and
             record["package_version"].split("+", 1)[0] == expected[role + "_version"].split("+", 1)[0],
             "Package observation version mismatch")
        for field in ("repository_url", "repository_commit"):
            need(record[field] is None or isinstance(record[field], str) and len(record[field]) <= 2048,
                 "Malformed reported package source")
        hashes = record["installed_files_sha256"]
        need(isinstance(hashes, dict) and 1 <= len(hashes) <= 3000, "Invalid installed file inventory")
        for name, value in hashes.items():
            need(isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_.+/-]+", name) and
                 not name.startswith("/") and all(p not in ("", ".", "..") for p in name.split("/"))
                 and digest(value), "Invalid package file observation")
        need(any(p.endswith("/" + binary) for p in hashes), "Missing package binary hash")
    files = packet["files"]
    need(isinstance(files, dict) and 1 <= len(files) <= 1100, "Bad artifact file inventory")
    data = {}
    total = 0
    for name, value in files.items():
        exact_keys(value, {"sha256", "text"})
        need(isinstance(value["text"], str), "Nontext artifact data")
        raw = value["text"].encode("utf-8")
        total += len(raw)
        need(len(raw) <= MAX_FILE and total <= MAX_BUNDLE and "\0" not in value["text"], "Data exceeds text bounds")
        need(digest(value["sha256"]) and sha(raw) == value["sha256"], "Artifact data hash mismatch")
        data[name] = raw
    manifest = decode_json(data.get("captured-help/manifest.json", b"null"))
    need(isinstance(manifest, dict), "Missing manifest")
    need(set(data) == capture_paths(manifest), "Unexpected or missing artifact paths")
    need(manifest.get("requested_package_version") == expected["cli_version"] and
         manifest.get("cli_version") == expected["cli_version"].split("+", 1)[0] and
         isinstance(manifest.get("cli_version_raw"), str) and
         manifest["cli_version_raw"].split("+", 1)[0] == manifest["cli_version"], "CLI effective version mismatch")
    frames = decode_json(data["captured-help/mcp-protocol-frames.json"])
    projected = validate_capture(frames, expected["mcp_version"])
    need(same_json(decode_json(data["captured-help/mcp-tools.json"]), projected), "MCP schemas differ from protocol frames")
    need(same_json(decode_json(data["captured-help/mcp-protocol-requests.json"]), fixed_requests()), "Unexpected MCP requests")
    raw_stdout = data["captured-help/mcp-stdout.jsonl"]
    need(raw_stdout.endswith(b"\n"), "Unterminated raw protocol frame")
    stdout_frames = [decode_json(line) for line in raw_stdout.splitlines()]
    need(same_json(stdout_frames, frames) and not data["captured-help/mcp-stderr.txt"].strip(), "Protocol stream differs")
    receipt = decode_json(data["captured-help/mcp-capture-receipt.json"])
    exact_keys(receipt, {"schema_version", "requested_package_version", "effective_server_version",
        "protocol_version", "argv", "python_version", "shutdown", "sha256", "recorder_source_sha256"})
    need(type(receipt["schema_version"]) is int and receipt["schema_version"] == 1 and receipt["requested_package_version"] == expected["mcp_version"]
         and receipt["effective_server_version"] == projected["server"]["version"]
         and receipt["protocol_version"] == projected["protocol_version_negotiated"]
         and receipt["argv"] == ["ppds-mcp-server", "--read-only"]
         and receipt["python_version"] == "3.14.10", "MCP capture identity/runtime receipt mismatch")
    exact_keys(receipt["shutdown"], {"strategy", "returncode", "descendant_shutdown_proven"})
    shutdown = receipt["shutdown"]
    need(shutdown["strategy"] in {"already-exited", "stdin-close", "terminate-owned-handle", "kill-owned-handle"}
         and type(shutdown["returncode"]) is int and shutdown["descendant_shutdown_proven"] is False
         and (shutdown["returncode"] == 0 or shutdown["strategy"] in {"terminate-owned-handle", "kill-owned-handle"}),
         "Incomplete MCP shutdown receipt")
    mcp_files = {"mcp-tools.json", "mcp-protocol-frames.json", "mcp-protocol-requests.json",
                 "mcp-stdout.jsonl", "mcp-stderr.txt"}
    need(receipt["sha256"] == {name: sha(data["captured-help/" + name]) for name in mcp_files},
         "MCP receipt hashes differ from data")
    need(receipt["recorder_source_sha256"] == {name: packet["source_sha256"]["tools/" + name]
         for name in ("capture_mcp_tools.py", "mcp_capture_format.py")}, "MCP recorder source mismatch")
    aliases = decode_json(data["captured-help/alias-provenance.json"])
    need(isinstance(aliases, dict) and isinstance(aliases.get("paths"), dict) and
         set(aliases["paths"]) == set(manifest["command_tree"]) and
         all(value in manifest["command_tree"] for value in aliases["paths"].values()), "Incomplete alias provenance")
    canonical = {command: data["captured-help/" + command.replace(" ", "_") + ".txt"].decode("utf-8")
                 for command in set(aliases["paths"].values())}
    tree, expanded_texts, sources = expand_aliases(canonical)
    need(tree == manifest["command_tree"] and sources == aliases["paths"], "Alias derivation differs from shown command spellings")
    for command, text in expanded_texts.items():
        need(data["captured-help/" + command.replace(" ", "_") + ".txt"] == text.encode("utf-8"),
             "Derived alias help differs from its canonical capture")
    counts = {"canonical_runtime_capture_count": len(canonical), "alias_expanded_command_path_count": len(sources),
              "alias_derived_path_count": sum(path != source for path, source in sources.items())}
    for record in (manifest, aliases):
        need(all(type(record.get(key)) is int and record[key] == value for key, value in counts.items()), "CLI capture count mismatch")
    for name in REFERENCES:
        need(b"GENERATED" in data[name][:600] and data[name].strip(), "Missing generated reference marker")
    for name in set(data) - REFERENCES - {"captured-help/" + name for name in CAPTURE_DATA}:
        need(data[name].strip(), "Empty CLI capture")
    return data


def apply(packet, expected, root):
    data = validate(packet, expected, root)
    # Prepare every mutation before changing any checkout byte. SKILL.md contents
    # never come from the producer; only two trusted frontmatter pins may change.
    writes = dict(data)
    for skill in GROUPS:
        name = "skills/%s/SKILL.md" % skill
        text = regular(root / name).decode("utf-8")
        parts = text.split("---", 2)
        need(len(parts) == 3 and not parts[0].strip(), "Missing skill frontmatter")
        for key, version in (("ppds_cli_version_tested", packet["binding"]["cli_version"].split("+", 1)[0]),
                             ("ppds_mcp_version_tested", packet["binding"]["mcp_version"].split("+", 1)[0])):
            pattern = r"(?m)^([ \t]*)" + key + r":[^\r\n]*(\r?)$"
            parts[1], count = re.subn(pattern, lambda m: m[1] + key + ': "' + version + '"' + m[2], parts[1])
            need(count == 1, "Missing/duplicate version pin")
        writes[name] = "---".join(parts).encode("utf-8")
    old = set()
    for path in (root / "captured-help").iterdir():
        regular(path)
        if path.name in CAPTURE_DATA | {"platform-contracts.json"} or re.fullmatch(r"ppds(?:_[a-z][a-z0-9-]*)*\.txt", path.name):
            old.add("captured-help/" + path.name)
        else:
            raise ValueError("Unrecognized existing capture path")
    for name in writes:
        target = root / name
        if target.exists() or target.is_symlink():
            regular(target)
        else:
            need(target.parent.is_dir(), "Unexpected destination directory")
            for parent in (target.parent,) + tuple(target.parent.parents):
                info = parent.lstat()
                need(not parent.is_symlink() and not getattr(info, "st_file_attributes", 0) & 0x400, "Linked destination")
    for name in sorted(old - set(data)):
        (root / name).unlink()
    for name, raw in writes.items():
        (root / name).write_bytes(raw)
    return sorted(set(writes) | old)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--stage", type=Path, required=True)
    seal = sub.add_parser("pack")
    seal.add_argument("--stage", type=Path, required=True)
    seal.add_argument("--store", type=Path, required=True)
    seal.add_argument("--output", type=Path, required=True)
    write = sub.add_parser("apply")
    write.add_argument("--artifact-dir", type=Path, required=True)
    write.add_argument("--sha256", required=True)
    write.add_argument("--paths-output", type=Path, required=True)
    args = parser.parse_args()
    if args.operation == "prepare":
        args.stage.mkdir(parents=True, exist_ok=False)
        (args.stage / "tools").mkdir()
        for name in SCRIPTS:
            (args.stage / "tools" / name).write_bytes(regular(ROOT / "tools" / name))
        shutil.copytree(ROOT / "skills", args.stage / "skills")
        (args.stage / "evals").mkdir()
        (args.stage / "evals/check_skills.py").write_bytes(regular(ROOT / "evals/check_skills.py"))
        shutil.copytree(ROOT / ".claude-plugin", args.stage / ".claude-plugin")
        return 0
    expected = binding(os.environ)
    if args.operation == "pack":
        packet = pack(args.stage, args.store, ROOT, expected)
        raw = (json.dumps(packet, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        need(len(raw) <= MAX_BUNDLE, "Bundle exceeds size bound")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("xb") as stream:
            stream.write(raw)
        print(sha(raw))
    else:
        need(args.artifact_dir.is_dir() and sorted(p.name for p in args.artifact_dir.iterdir()) == ["bundle.json"],
             "Artifact must contain only bundle.json")
        raw = regular(args.artifact_dir / "bundle.json", MAX_BUNDLE)
        need(digest(args.sha256) and sha(raw) == args.sha256, "Wrong artifact digest")
        paths = apply(decode_json(raw), expected, ROOT)
        args.paths_output.write_bytes(b"".join(name.encode("utf-8") + b"\0" for name in paths))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
