"""Offline data-handoff checks; fake product pipes, no installs or network calls."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "evals"))
import recapture_artifact as artifact
from _test_mcp_capture import FakeProcess, raw_frames, sample_frames
from mcp_capture_format import fixed_requests, validate_capture


def encoded(value):
    return (json.dumps(value, indent=2) + "\n").encode("utf-8")


def expected_binding(cli="1.5.0", mcp="1.3.0"):
    return {"repository": "test/skills", "source_sha": "a" * 40, "source_tree": "b" * 40,
        "workflow_ref": "test/skills/.github/workflows/recapture-on-release.yml@refs/heads/main",
        "run_id": "123", "run_attempt": "2", "cli_version": cli, "mcp_version": mcp}


def package(role, version):
    return {"package_id": "PPDS." + ("Cli" if role == "cli" else "Mcp"),
        "package_version": version, "repository_url": "https://example.invalid/source",
        "repository_commit": "c" * 40,
        "installed_files_sha256": {"1.0/tools/" + ("ppds.dll" if role == "cli" else "ppds-mcp-server.dll"): "d" * 64}}


def packet_sample():
    frames = sample_frames()
    pins = artifact.source_pins(ROOT)
    data = {
        "manifest.json": encoded({"cli_version": "1.5.0", "cli_version_raw": "1.5.0+" + "c" * 40,
                                  "requested_package_version": "1.5.0", "command_tree": {"ppds": []},
                                  "canonical_runtime_capture_count": 1, "alias_expanded_command_path_count": 1, "alias_derived_path_count": 0}),
        "alias-provenance.json": encoded({"paths": {"ppds": "ppds"}, "canonical_runtime_capture_count": 1,
                                         "alias_expanded_command_path_count": 1, "alias_derived_path_count": 0}),
        "mcp-tools.json": encoded(validate_capture(frames, "1.3.0")),
        "mcp-protocol-frames.json": encoded(frames), "mcp-protocol-requests.json": encoded(fixed_requests()),
        "mcp-stdout.jsonl": raw_frames(frames), "mcp-stderr.txt": b"",
    }
    receipt = {"schema_version": 1, "requested_package_version": "1.3.0", "effective_server_version": "1.3.0",
        "protocol_version": "2025-03-26", "argv": ["ppds-mcp-server", "--read-only"], "python_version": "3.14.10",
        "shutdown": {"strategy": "stdin-close", "returncode": 0, "descendant_shutdown_proven": False},
        "sha256": {name: artifact.sha(raw) for name, raw in data.items() if name.startswith("mcp-")},
        "recorder_source_sha256": {name: pins["tools/" + name] for name in ("capture_mcp_tools.py", "mcp_capture_format.py")}}
    data["mcp-capture-receipt.json"] = encoded(receipt)
    data["ppds.txt"] = b"Usage:\n  ppds [options]\n"
    files = {"captured-help/" + name: {"sha256": artifact.sha(raw), "text": raw.decode("utf-8")}
             for name, raw in data.items()}
    for name in artifact.REFERENCES:
        raw = b"<!-- GENERATED -->\nFixture reference\n"
        files[name] = {"sha256": artifact.sha(raw), "text": raw.decode()}
    return {"schema_version": 1, "binding": expected_binding(), "source_sha256": pins,
        "package_observations": {role: package(role, "1.5.0" if role == "cli" else "1.3.0") for role in ("cli", "mcp")},
        "files": files}


def update_json(packet, name, change):
    path = "captured-help/" + name
    value = json.loads(packet["files"][path]["text"])
    change(value)
    raw = encoded(value)
    packet["files"][path] = {"sha256": artifact.sha(raw), "text": raw.decode()}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ArtifactTests(unittest.TestCase):
    def test_complete_data_validates_without_subprocess(self):
        with mock.patch.object(subprocess, "run", side_effect=AssertionError("No process expected")):
            data = artifact.validate(packet_sample(), expected_binding(), ROOT)
        self.assertEqual(len(data), len(artifact.REFERENCES) + len(artifact.CAPTURE_DATA) + 1)

    def test_binding_and_source_changes_rejected(self):
        for key in expected_binding():
            with self.subTest(key=key):
                packet = packet_sample()
                packet["binding"][key] += "x"
                with self.assertRaises(ValueError):
                    artifact.validate(packet, expected_binding(), ROOT)
        packet = packet_sample()
        packet["source_sha256"]["tools/recapture_artifact.py"] = "0" * 64
        with self.assertRaises(ValueError):
            artifact.validate(packet, expected_binding(), ROOT)

    def test_arbitrary_missing_traversal_and_hash_modified_files_rejected(self):
        for path in ("tools/recapture_artifact.py", ".github/workflows/evals.yml", "../escape.txt",
                     "captured-help/../escape.txt", "skills/ppds-core/SKILL.md", "captured-help/extra.json"):
            packet = packet_sample()
            packet["files"][path] = {"text": "data", "sha256": artifact.sha(b"data")}
            with self.subTest(path=path), self.assertRaises(ValueError):
                artifact.validate(packet, expected_binding(), ROOT)
        packet = packet_sample()
        del packet["files"]["captured-help/ppds.txt"]
        with self.assertRaises(ValueError):
            artifact.validate(packet, expected_binding(), ROOT)
        packet = packet_sample()
        packet["files"]["captured-help/ppds.txt"]["text"] += "changed"
        with self.assertRaises(ValueError):
            artifact.validate(packet, expected_binding(), ROOT)

    def test_receipts_frames_versions_and_schemas_must_agree(self):
        mutations = [
            ("mcp-capture-receipt.json", lambda x: x.update(effective_server_version="9.0.0")),
            ("mcp-capture-receipt.json", lambda x: x.update(requested_package_version="9.0.0")),
            ("mcp-capture-receipt.json", lambda x: x.update(python_version="3.14.3")),
            ("mcp-capture-receipt.json", lambda x: x["shutdown"].update(returncode=42)),
            ("mcp-capture-receipt.json", lambda x: x["sha256"].update({"mcp-stdout.jsonl": "0" * 64})),
            ("mcp-capture-receipt.json", lambda x: x["recorder_source_sha256"].update({"capture_mcp_tools.py": "0" * 64})),
            ("mcp-tools.json", lambda x: x["tools"][0]["inputSchema"].update(properties={"forged": {"type": "string"}})),
            ("mcp-tools.json", lambda x: x.update(tool_count=1)),
            ("mcp-protocol-requests.json", lambda x: x[2].update(method="tools/call")),
            ("mcp-protocol-requests.json", lambda x: x[0].update(id=True)),
            ("manifest.json", lambda x: x.update(cli_version="9.0.0")),
            ("alias-provenance.json", lambda x: x["paths"].update({"ppds": "ppds missing"})),
        ]
        for name, change in mutations:
            packet = packet_sample()
            update_json(packet, name, change)
            with self.subTest(name=name), self.assertRaises(ValueError):
                artifact.validate(packet, expected_binding(), ROOT)

    def test_apply_rejects_before_any_checkout_write(self):
        with tempfile.TemporaryDirectory(prefix="ppds-handoff-") as directory:
            target = Path(directory) / "target"
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            before = {p.relative_to(target).as_posix(): artifact.sha(p.read_bytes())
                      for p in target.rglob("*") if p.is_file()}
            packet = packet_sample()
            update_json(packet, "mcp-tools.json", lambda x: x.update(tool_count=999))
            with self.assertRaises(ValueError):
                artifact.apply(packet, expected_binding(), target)
            after = {p.relative_to(target).as_posix(): artifact.sha(p.read_bytes())
                     for p in target.rglob("*") if p.is_file()}
            self.assertEqual(before, after)

    def test_prepare_fake_capture_pack_apply_and_static_gate(self):
        """Real staging/generator/writer flow; product calls are in-memory doubles.

        Existing alpha capture bytes are fixture inputs, not a new product run.
        The mocked runtime field is synthetic and makes no 3.14.10 execution claim.
        """
        with tempfile.TemporaryDirectory(prefix="ppds-handoff-flow-") as directory:
            owned = Path(directory)
            stage, target, store = [owned / name for name in ("stage", "target", "store")]
            with mock.patch.object(sys, "argv", ["recapture_artifact.py", "prepare", "--stage", str(stage)]):
                artifact.main()
            self.assertFalse((stage / "captured-help").exists())
            cli = load_module("fixture_cli", stage / "tools/capture_cli_help.py")
            mcp = load_module("fixture_mcp", stage / "tools/capture_mcp_tools.py")
            generator = load_module("fixture_generator", stage / "tools/generate_flag_tables.py")
            bump = load_module("fixture_bump", stage / "tools/recapture.py")
            manifest = json.loads((ROOT / "captured-help/manifest.json").read_text(encoding="utf-8"))
            frames = json.loads((ROOT / "captured-help/mcp-protocol-frames.json").read_text(encoding="utf-8"))
            cli_version, mcp_version = manifest["cli_version"], frames[0]["result"]["serverInfo"]["version"]
            expected = expected_binding(cli_version, mcp_version)
            calls = []

            def cli_process(argv, **kwargs):
                calls.append(argv)
                self.assertEqual(argv[0], "ppds")
                self.assertIn(argv[-1], ("--help", "--version"))
                text = manifest["cli_version_raw"] if argv[-1] == "--version" else (
                    ROOT / "captured-help" / ("_".join(argv[:-1]) + ".txt")).read_text(encoding="utf-8")
                return subprocess.CompletedProcess(argv, 0, text, "")

            with contextlib.redirect_stderr(io.StringIO()), mock.patch.dict(os.environ, {
                    "TARGET_CLI_VERSION": cli_version, "TARGET_MCP_VERSION": mcp_version}):
                with mock.patch.object(sys, "argv", ["capture_cli_help.py", "--out", str(stage / "captured-help")]), \
                        mock.patch.object(cli.subprocess, "run", side_effect=cli_process), \
                        mock.patch.object(cli.platform, "system", return_value="Synthetic fixture"), \
                        mock.patch.object(cli.platform, "machine", return_value="test"):
                    cli.main()
                process = FakeProcess(stdout=raw_frames(frames))
                with mock.patch.object(sys, "argv", ["capture_mcp_tools.py", "--out", str(stage / "captured-help")]), \
                        mock.patch.object(mcp.subprocess, "Popen", return_value=process), \
                        mock.patch.object(mcp.sys, "version", "3.14.10 synthetic fixture"):
                    mcp.main()
                generator.main()
                bump.bump_frontmatter(*bump.captured_versions())
            self.assertEqual(len(calls), manifest["canonical_runtime_capture_count"] + 1)
            self.assertEqual([json.loads(line)["method"] for line in process.sent.splitlines()],
                             ["initialize", "notifications/initialized", "tools/list"])
            for role, version, package_id, binary in (("cli", cli_version, "PPDS.Cli", "ppds.dll"),
                ("mcp", mcp_version, "PPDS.Mcp", "ppds-mcp-server.dll")):
                package_dir = store / package_id.lower() / version / package_id.lower() / version
                (package_dir / "tools/net10.0/any").mkdir(parents=True)
                (package_dir / (package_id.lower() + ".nuspec")).write_text(
                    '<package><metadata><id>' + package_id + '</id><version>' + version +
                    '</version><repository url="https://example.invalid/source" commit="' + "c" * 40 +
                    '" /></metadata></package>', encoding="utf-8")
                (package_dir / "tools/net10.0/any" / binary).write_bytes(b"synthetic binary, never executed")
            packet = artifact.pack(stage, store, ROOT, expected)
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            original_skill = (target / "skills/ppds-core/SKILL.md").read_bytes()
            paths = artifact.apply(packet, expected, target)
            self.assertEqual((target / "skills/ppds-core/SKILL.md").read_bytes(), original_skill)
            self.assertFalse((target / "captured-help/platform-contracts.json").exists())
            self.assertNotIn("tools/recapture_artifact.py", paths)
            env = dict(os.environ, PPDS_SKIP_FRESHNESS="1")
            for checkout in (stage, target):
                checked = subprocess.run([sys.executable, str(checkout / "evals/check_skills.py")],
                    env=env, capture_output=True, text=True, timeout=30, encoding="utf-8")
                self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_workflow_writer_has_no_product_or_artifact_code_execution(self):
        workflow = (ROOT / ".github/workflows/recapture-on-release.yml").read_text(encoding="utf-8")
        producer, writer = workflow.split("\n  write-pr:\n", 1)
        self.assertNotIn("contents: write", producer)
        self.assertNotIn("GH_TOKEN:", producer)
        self.assertNotIn("pull-requests: write", producer)
        self.assertEqual(workflow.count("persist-credentials: false"), 2)
        self.assertEqual(workflow.count("if: github.ref == format('refs/heads/{0}', github.event.repository.default_branch)"), 2)
        self.assertEqual(workflow.count("ref: ${{ github.sha }}"), 2)
        for forbidden in ("dotnet tool", "recapture.py", "capture_mcp_tools.py", "capture_cli_help.py",
                          "generate_flag_tables.py", "git add -A", "--force", "workflow_run:"):
            self.assertNotIn(forbidden, writer)
        self.assertIn("--pathspec-from-file=", writer)
        self.assertIn("artifact-ids: ${{ needs.capture.outputs.artifact_id }}", writer)
        self.assertIn("--body-file", writer)
        self.assertIn("--draft", writer)


if __name__ == "__main__":
    unittest.main()
