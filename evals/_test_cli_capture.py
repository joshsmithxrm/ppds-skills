"""Offline CLI recorder controls; subprocess results and help reader are mocked."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import cli_capture_format as capture_format

SPEC = importlib.util.spec_from_file_location("capture_cli_help", ROOT / "tools/capture_cli_help.py")
capture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capture)


def help_text(rows="", command="ppds"):
    return "Description:\n  Example\n\nUsage:\n  " + command + " [options]\n" + ("\nCommands:\n" + rows if rows else "")


class CliCaptureTests(unittest.TestCase):
    def test_pure_format_import_has_no_process_or_recorder_dependency(self):
        spec = importlib.util.spec_from_file_location("isolated_cli_format", ROOT / "tools/cli_capture_format.py")
        pure = importlib.util.module_from_spec(spec)
        with mock.patch.object(subprocess, "run", side_effect=AssertionError("No process launch")), mock.patch.object(subprocess, "Popen", side_effect=AssertionError("No process launch")):
            spec.loader.exec_module(pure)
            tree, _, sources = pure.expand_aliases({"ppds": help_text()})
        self.assertEqual(tree, {"ppds": []})
        self.assertEqual(sources, {"ppds": "ppds"})
        self.assertFalse(hasattr(pure, "subprocess"))
        self.assertFalse(hasattr(pure, "main"))
        self.assertIs(capture.expand_aliases, capture_format.expand_aliases)

    def test_retained_capture_replays_exact_alias_tree_without_product(self):
        directory = ROOT / "captured-help"
        sources = json.loads((directory / "alias-provenance.json").read_text(encoding="utf-8"))["paths"]
        manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
        canonical = {path: (directory / capture.node_filename(path.split(" "))).read_text(encoding="utf-8")
                     for path in set(sources.values())}
        with mock.patch.object(capture.subprocess, "run", side_effect=AssertionError("No product execution")):
            tree, texts, derived = capture.expand_aliases(canonical)
        self.assertEqual(len(canonical), manifest["canonical_runtime_capture_count"])
        self.assertEqual(len(tree), manifest["alias_expanded_command_path_count"])
        self.assertEqual(tree, manifest["command_tree"])
        self.assertEqual(derived, sources)
        for path, source in derived.items():
            self.assertEqual(texts[path], canonical[source])

    def test_nested_aliases_derive_only_from_shown_parent(self):
        canonical = {"ppds": help_text("  group, g  A group\n"),
                     "ppds group": help_text("  child, c <value>  A child\n    Continued description\n"),
                     "ppds group child": help_text()}
        calls = []

        def reader(argv):
            calls.append(argv)
            return canonical[" ".join(["ppds"] + argv[1:])]

        with mock.patch.object(capture, "run_help", side_effect=reader), contextlib.redirect_stderr(io.StringIO()):
            tree, texts, sources = capture.capture_tree("/pinned/ppds")
        self.assertEqual(calls, [["/pinned/ppds"], ["/pinned/ppds", "group"], ["/pinned/ppds", "group", "child"]])
        self.assertEqual(len(tree), 7)
        self.assertEqual(sources["ppds g c"], "ppds group child")
        self.assertEqual(texts["ppds g c"], canonical["ppds group child"])

    def test_malformed_or_duplicate_command_columns_fail(self):
        for rows in ["  bad/name  Bad\n", "  --option  Bad\n", "  good,  Bad\n",
                     "  same, same  Bad\n", "  first, alias  One\n  alias  Two\n",
                     "    No preceding command\n", "", "  child  One\nCommands:\n  other  Two\n"]:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                capture.parse_command_groups("Usage:\n  ppds\nCommands:\n" + rows)
        with self.assertRaises(ValueError):
            capture.parse_command_groups("This is an error, not help")

    def test_missing_unreachable_and_unsafe_nodes_fail(self):
        cases = [{"ppds": help_text("  missing  Missing\n")},
                 {"ppds": help_text(), "ppds orphan": help_text()},
                 {"ppds": help_text(), "ppds bad/name": help_text()}]
        for canonical in cases:
            with self.subTest(canonical=canonical), self.assertRaises(ValueError):
                capture.expand_aliases(canonical)

    def test_node_and_recursive_depth_limits_fail(self):
        canonical = {"ppds": help_text("  a, b  Two names\n"), "ppds a": help_text()}
        with mock.patch.object(capture_format, "MAX_NODES", 2), self.assertRaises(ValueError):
            capture.expand_aliases(canonical)
        with mock.patch.object(capture, "MAX_DEPTH", 3), mock.patch.object(capture, "run_help", return_value=help_text("  again  Repeated\n")), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(ValueError):
                capture.capture_tree("ppds")

    def test_nonzero_stderr_empty_and_oversized_process_output_fail(self):
        for code, stdout, stderr in [(1, "help", ""), (0, "help", "warning"),
                                     (0, "", ""), (0, "   ", ""),
                                     (0, "x" * (capture.MAX_TEXT_BYTES + 1), "")]:
            result = subprocess.CompletedProcess(["fixture"], code, stdout, stderr)
            with self.subTest(code=code, size=len(stdout), stderr=stderr), mock.patch.object(capture.subprocess, "run", return_value=result):
                with self.assertRaises(ValueError):
                    capture.run_help(["fixture"])
        with mock.patch.object(capture.subprocess, "run", side_effect=subprocess.TimeoutExpired("fixture", 120)):
            with self.assertRaises(subprocess.TimeoutExpired):
                capture.run_help(["fixture"])

    def test_exact_requested_version_and_informational_suffix(self):
        self.assertEqual(capture.effective_version("1.5.0+abcdef", "1.5.0"), "1.5.0")
        self.assertEqual(capture.effective_version("1.5.0-rc.2+abcdef", "1.5.0-rc.2+package"), "1.5.0-rc.2")
        for raw, expected in [("1.5.1", "1.5.0"), ("1.5.0", "1.5.*"), ("01.5.0", None),
                              ("1.5.0\nother", None), ("1.5.0-rc.01", None), ("1.5.0", "")]:
            with self.subTest(raw=raw, expected=expected), self.assertRaises(ValueError):
                capture.effective_version(raw, expected)

    def test_main_writes_receipts_only_after_complete_capture(self):
        tree, texts, sources = capture.expand_aliases({"ppds": help_text()})
        with tempfile.TemporaryDirectory(prefix="ppds-cli-capture-fixture-") as directory:
            output = Path(directory) / "out"
            argv = ["capture_cli_help.py", "--out", str(output)]
            with mock.patch.object(capture.sys, "argv", argv), mock.patch.dict(os.environ, {"TARGET_CLI_VERSION": "1.5.0"}), mock.patch.object(capture, "run_text", return_value="1.5.0+source\n"), mock.patch.object(capture, "capture_tree", return_value=(tree, texts, sources)), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(capture.main(), 0)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            aliases = json.loads((output / "alias-provenance.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["cli_version_raw"], "1.5.0+source")
            self.assertEqual(manifest["requested_package_version"], "1.5.0")
            self.assertEqual(manifest["canonical_runtime_capture_count"], 1)
            self.assertEqual(aliases["paths"], {"ppds": "ppds"})
            self.assertNotIn("source_commit", manifest)
            failed = Path(directory) / "failure"
            with mock.patch.object(capture.sys, "argv", ["capture_cli_help.py", "--out", str(failed)]), mock.patch.dict(os.environ, {"TARGET_CLI_VERSION": "1.5.0"}), mock.patch.object(capture, "run_text", return_value="1.5.0\n"), mock.patch.object(capture, "capture_tree", side_effect=ValueError("Incomplete tree")):
                with self.assertRaises(ValueError):
                    capture.main()
            self.assertFalse(failed.exists())


if __name__ == "__main__":
    unittest.main()
