"""Offline controls for manual, exact-pair recapture; no real tools or feeds."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def run_block(workflow, step):
    part = workflow.split("      - name: " + step + "\n", 1)[1].split("\n      - name: ", 1)[0]
    body = part.split("        run: |\n", 1)[1]
    lines = body.rstrip("\n").splitlines()
    if not all(not line or line.startswith("          ") for line in lines):
        raise AssertionError("Unexpected workflow run indentation")
    return "\n".join(line[10:] if line else "" for line in lines) + "\n"


class RecaptureVersionTests(unittest.TestCase):
    def setUp(self):
        self.workflow = (ROOT / ".github/workflows/recapture-on-release.yml").read_text(encoding="utf-8")
        self.script = run_block(self.workflow, "Validate requested tool versions")
        self.install = run_block(self.workflow, "Install released PPDS tools")
        self.bash = shutil.which("bash")
        self.assertIsNotNone(self.bash, "Existing Linux/Windows Bash test dependency is required")

    def invoke(self, script, cli="1.5.0", mcp="1.3.0", tool_exit=0):
        with tempfile.TemporaryDirectory(prefix="ppds-version-pair-") as directory:
            owned = Path(directory)
            output, calls, path = [owned / name for name in ("outputs", "calls", "path")]
            for file in (output, calls, path):
                file.write_text("", encoding="utf-8")
            allowed = {"SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "SYSTEMDRIVE"}
            env = {key: value for key, value in os.environ.items() if key.upper() in allowed}
            env.update({"PATH": str(Path(self.bash).parent), "HOME": owned.as_posix(),
                "USERPROFILE": owned.as_posix(), "LC_ALL": "C", "GITHUB_OUTPUT": output.as_posix(),
                "CALL_LOG": calls.as_posix(), "GITHUB_PATH": path.as_posix(),
                "REQUESTED_CLI_VERSION": cli, "REQUESTED_MCP_VERSION": mcp,
                "TARGET_CLI_VERSION": cli, "TARGET_MCP_VERSION": mcp,
                "FIXTURE_TOOL_EXIT": str(tool_exit)})
            # Any feed/manifest Python call fails. dotnet only records arguments.
            stub = """python() { printf 'unexpected-python\\n' >> "$CALL_LOG"; return 97; }
dotnet() { printf '%s\\n' "$*" >> "$CALL_LOG"; return "$FIXTURE_TOOL_EXIT"; }
"""
            result = subprocess.run([self.bash, "--noprofile", "--norc", "-c", stub + script],
                cwd=str(owned), env=env, stdin=subprocess.DEVNULL, capture_output=True,
                encoding="utf-8", timeout=10, check=False)
            self.assertFalse((owned / "MUST_NOT_RUN").exists())
            return result, output.read_text(encoding="utf-8"), calls.read_text(encoding="utf-8")

    def test_explicit_pairs_need_no_feed_or_current_version(self):
        # MCP-only, identical, older and prerelease selections all reach capture;
        # only the eventual generated diff can be a no-op.
        for cli, mcp in [("1.5.0", "1.3.1"), ("1.5.0", "1.3.0"), ("1.4.1", "1.2.0"),
                         ("1.5.0-rc.1", "1.3.0-alpha.2"), ("1.5.0+build.1", "1.3.0")]:
            with self.subTest(cli=cli, mcp=mcp):
                result, output, calls = self.invoke(self.script, cli, mcp)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output, "cli_version=%s\nmcp_version=%s\n" % (cli, mcp))
                self.assertEqual(calls, "")
        self.assertNotIn("proceed", self.workflow)
        self.assertNotIn("cli_newer_than.py", self.workflow)
        self.assertNotIn("latest_stable_cli.py", self.workflow)

    def test_missing_or_malformed_pair_writes_no_outputs(self):
        bad_values = ["", "1.5.0\nother=true", "1.5.0\rother=true", '1.5.0"; touch MUST_NOT_RUN; #',
            '$(touch MUST_NOT_RUN)', chr(96) + 'touch MUST_NOT_RUN' + chr(96), "1.5.*", "[1.5.0,2.0.0)",
            "v1.5.0", " 1.5.0", "1.5.0 ", "01.5.0", "1.5.0-rc.01", "1.5.0-", "1.5.0+", "\uff11.5.0"]
        for value in bad_values:
            for source in ("cli", "mcp"):
                with self.subTest(source=source, value=value):
                    result, output, calls = self.invoke(self.script, **{source: value})
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(output, "")
                    self.assertEqual(calls, "")

    def test_installer_consumes_both_exact_versions_without_fallback(self):
        for mcp in ("1.3.0", "1.3.1"):
            with self.subTest(mcp=mcp):
                result, _, calls = self.invoke(self.install, mcp=mcp)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(calls, "tool install -g PPDS.Cli --version 1.5.0\n"
                    "tool install -g PPDS.Mcp --version %s\n" % mcp)
        result, _, calls = self.invoke(self.install, tool_exit=42)
        self.assertEqual(result.returncode, 42)
        self.assertEqual(calls, "tool install -g PPDS.Cli --version 1.5.0\n")

    def test_manual_trigger_and_data_boundaries(self):
        trigger = self.workflow.split("\non:\n", 1)[1].split("\npermissions:", 1)[0]
        self.assertIn("  workflow_dispatch:", trigger)
        self.assertNotIn("  schedule:", trigger)
        self.assertEqual(trigger.count("required: true"), 2)
        for tool in ("CLI", "MCP"):
            self.assertIn("REQUESTED_%s_VERSION: ${{ inputs.%s_version }}" % (tool, tool.lower()), self.workflow)
            self.assertIn("TARGET_%s_VERSION: ${{ steps.ver.outputs.%s_version }}" % (tool, tool.lower()), self.workflow)
        self.assertNotIn("${{", self.script)
        self.assertNotIn("${{", self.install)
        self.assertIn('branch="recapture/cli-$TARGET_CLI_VERSION-mcp-$TARGET_MCP_VERSION"', self.workflow)


if __name__ == "__main__":
    unittest.main()
