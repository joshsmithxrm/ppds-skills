#!/usr/bin/env python3
"""Print the latest STABLE PPDS.Cli version published on NuGet.

Used by .github/workflows/recapture-on-release.yml to decide whether a newer
release exists than the one in captured-help/manifest.json. Prerelease
versions (anything with a '-' suffix: -rc.N, -beta, ...) are excluded, since
the package only re-captures against stable releases. Prints nothing (empty)
and exits 0 if the feed is unreachable or has no stable version, so the caller
treats it as "no new release" rather than failing the job.

Usage:
    python tools/latest_stable_cli.py [--package PPDS.Cli]
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request

FLATCONTAINER = "https://api.nuget.org/v3-flatcontainer/{pkg}/index.json"


def latest_stable(package: str) -> str:
    url = FLATCONTAINER.format(pkg=package.lower())
    with urllib.request.urlopen(url, timeout=60) as resp:
        versions = json.load(resp).get("versions", [])
    # NuGet's flat-container index is sorted ascending by SemVer, so the last
    # entry without a prerelease suffix is the newest stable release.
    stable = [v for v in versions if "-" not in v]
    return stable[-1] if stable else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--package", default="PPDS.Cli")
    args = ap.parse_args()
    try:
        print(latest_stable(args.package))
    except Exception as exc:  # network/feed problems => "no new release"
        sys.stderr.write(f"warning: could not resolve latest stable: {exc}\n")
        print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
