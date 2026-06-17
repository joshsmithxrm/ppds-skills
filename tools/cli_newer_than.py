#!/usr/bin/env python3
"""Print 'yes' if <candidate> is a strictly newer PPDS version than <baseline>.

A deliberately small SemVer comparison covering the shapes PPDS ships:
`X.Y.Z` and `X.Y.Z-rc.N`. The rule that matters for the re-capture trigger is
that a stable release outranks its own prerelease — `1.2.0` is newer than
`1.2.0-rc.6`, while `1.1.0` is NOT newer than `1.2.0-rc.6`. Used by
recapture-on-release.yml to avoid "downgrade" captures when the pinned version
is an rc ahead of the latest published stable.

Usage:
    python tools/cli_newer_than.py <candidate> <baseline>   # prints yes|no
"""
from __future__ import annotations

import sys


def parse(v: str) -> tuple[tuple[int, ...], tuple[int, ...] | None]:
    """(core ints, prerelease ints|None). None prerelease ranks ABOVE any."""
    core, _, pre = v.partition("-")
    core_t = tuple(int(p) for p in core.split(".") if p.isdigit())
    if not pre:
        return core_t, None
    # "rc.6" -> (6,); keep only numeric identifiers, which is all PPDS uses.
    pre_t = tuple(int(p) for p in pre.split(".") if p.isdigit())
    return core_t, pre_t


def newer(candidate: str, baseline: str) -> bool:
    c_core, c_pre = parse(candidate)
    b_core, b_pre = parse(baseline)
    if c_core != b_core:
        return c_core > b_core
    # Same core: a release (no prerelease) outranks a prerelease.
    if c_pre is None and b_pre is None:
        return False
    if c_pre is None:
        return True   # candidate is the release, baseline is its prerelease
    if b_pre is None:
        return False  # candidate is a prerelease of an already-released core
    return c_pre > b_pre


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        sys.stderr.write("usage: cli_newer_than.py <candidate> <baseline>\n")
        return 2
    print("yes" if newer(argv[0], argv[1]) else "no")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
