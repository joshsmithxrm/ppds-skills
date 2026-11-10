"""Proposed stdlib resolver controls; no install/feed/live/credential operations."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
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
        self.script = run_block(self.workflow, "Resolve current vs target CLI version")
        self.bash = shutil.which("bash")
        self.assertIsNotNone(self.bash, "Existing Linux/Windows Bash test dependency is required")

    def resolve(self, current="1.4.2", forced="", latest="1.5.0"):
        with tempfile.TemporaryDirectory(prefix="ppds-version-proposal-") as directory:
            owned = Path(directory)
            output, calls = owned / "outputs", owned / "calls"
            output.write_text("", encoding="utf-8")
            calls.write_text("", encoding="utf-8")
            allowed = {"SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT", "SYSTEMDRIVE"}
            env = {key: value for key, value in os.environ.items() if key.upper() in allowed}
            env.update({"PATH": str(Path(self.bash).parent), "HOME": owned.as_posix(),
                "USERPROFILE": owned.as_posix(), "LC_ALL": "C", "GITHUB_OUTPUT": output.as_posix(),
                "CALL_LOG": calls.as_posix(), "FIXTURE_CURRENT": current, "FIXTURE_LATEST": latest,
                "REQUESTED_CLI_VERSION": forced, "TEST_PYTHON": Path(sys.executable).as_posix(),
                "REAL_COMPARATOR": (ROOT / "tools/cli_newer_than.py").as_posix()})
            # Replace only network/file-read Python commands. The unchanged actual
            # pure comparator decides ordering; it cannot install or call a feed.
            stub = """python() {
  case "$1" in
    -c) printf '%s' "$FIXTURE_CURRENT" ;;
    tools/latest_stable_cli.py) printf 'feed\\n' >> "$CALL_LOG"; printf '%s' "$FIXTURE_LATEST" ;;
    tools/cli_newer_than.py) printf 'compare\\n' >> "$CALL_LOG"; "$TEST_PYTHON" -E -S -B "$REAL_COMPARATOR" "$2" "$3" ;;
    *) return 97 ;;
  esac
}
"""
            result = subprocess.run([self.bash, "--noprofile", "--norc", "-c", stub + self.script],
                cwd=str(owned), env=env, stdin=subprocess.DEVNULL, capture_output=True,
                encoding="utf-8", timeout=10, check=False)
            self.assertFalse((owned / "PROPOSAL_MUST_NOT_RUN").exists())
            return result, output.read_text(encoding="utf-8"), calls.read_text(encoding="utf-8")

    def test_latest_stable_and_stable_over_rc_keep_selection(self):
        for current in ["1.4.2", "1.5.0-rc.6"]:
            with self.subTest(current=current):
                result, output, calls = self.resolve(current=current)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output, "current=%s\ntarget=1.5.0\nproceed=true\n" % current)
                self.assertEqual(calls, "feed\ncompare\n")

    def test_forced_literal_ignores_feed_and_keeps_prereleases(self):
        for target in ["1.5.0-rc.1", "1.5.0-alpha.0.28+abc123", "1.5.0+build.1"]:
            with self.subTest(target=target):
                result, output, calls = self.resolve(forced=target, latest="9.9.9")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output, "current=1.4.2\ntarget=%s\nproceed=true\n" % target)
                self.assertEqual(calls, "compare\n")

    def test_empty_feed_equal_and_older_keep_noop(self):
        for current, forced, latest, expected_calls in [
            ("1.4.2", "", "", "feed\n"), ("1.5.0", "1.5.0", "9.9.9", "compare\n"),
            ("1.5.0", "1.4.2", "9.9.9", "compare\n")]:
            with self.subTest(current=current, forced=forced, latest=latest):
                result, output, calls = self.resolve(current, forced, latest)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output, "current=%s\ntarget=%s\nproceed=false\n" % (current, forced or latest))
                self.assertEqual(calls, expected_calls)

    def test_invalid_forced_feed_and_current_write_no_outputs(self):
        bad_values = ["1.5.0\nproceed=true", "1.5.0\rproceed=true", '1.5.0"; touch PROPOSAL_MUST_NOT_RUN; #',
            '$(touch PROPOSAL_MUST_NOT_RUN)', '`touch PROPOSAL_MUST_NOT_RUN`', "1.5.*", "[1.5.0,2.0.0)",
            "v1.5.0", " 1.5.0", "1.5.0 ", "01.5.0", "1.5.0-rc.01", "1.5.0-", "1.5.0+", "１.5.0"]
        for value in bad_values:
            for source in ["forced", "feed", "current"]:
                with self.subTest(source=source, value=value):
                    inputs = {"forced": {"forced": value}, "feed": {"latest": value},
                              "current": {"current": value}}[source]
                    result, output, calls = self.resolve(**inputs)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(output, "")
                    self.assertNotIn("compare\n", calls)

    def test_expressions_stay_in_env_and_install_consumes_quoted_data(self):
        self.assertIn("          REQUESTED_CLI_VERSION: ${{ inputs.cli_version }}", self.workflow)
        self.assertIn("          TARGET_CLI_VERSION: ${{ steps.ver.outputs.target }}", self.workflow)
        self.assertNotIn("${{", self.script)
        install = run_block(self.workflow, "Install released PPDS tools")
        self.assertNotIn("${{", install)
        self.assertIn('PPDS.Cli --version "$TARGET_CLI_VERSION"', install)


if __name__ == "__main__":
    unittest.main()
