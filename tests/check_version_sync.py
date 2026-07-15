#!/usr/bin/env python3
"""Guard the single-version promise.

The version string lives in five places (pyproject, the detector, the plugin
manifest, the README badge line, and the website). The 0.4.0 release fixed a
drift where the same page carried both v0.3.0 and v0.3.1 — this check stops
that from ever happening again.

Usage: python3 tests/check_version_sync.py   (exit 0 in sync, 1 on drift)
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

_SEMVER = r"(\d+\.\d+\.\d+)"


def _read(rel):
    with open(os.path.join(_ROOT, rel), encoding="utf-8") as f:
        return f.read()


def _first(rel, pattern, label):
    """Yield (label, version) for the first match of pattern in the file."""
    m = re.search(pattern, _read(rel), re.M)
    yield label, (m.group(1) if m else None)


def _versions():
    # pyproject.toml — [project] version = "X.Y.Z"
    yield from _first("pyproject.toml",
                      r'^version\s*=\s*"' + _SEMVER + '"',
                      "pyproject.toml [project] version")
    # scripts/flag_slop.py — __version__ = "X.Y.Z"
    yield from _first(os.path.join("scripts", "flag_slop.py"),
                      r'^__version__\s*=\s*"' + _SEMVER + '"',
                      "scripts/flag_slop.py __version__")
    # .claude-plugin/plugin.json — "version": "X.Y.Z"
    yield from _first(os.path.join(".claude-plugin", "plugin.json"),
                      r'"version"\s*:\s*"' + _SEMVER + '"',
                      ".claude-plugin/plugin.json version")
    # README.md — the "**Version X.Y.Z**" badge line
    yield from _first("README.md",
                      r"\*\*Version " + _SEMVER + r"\*\*",
                      "README.md version line")
    # docs/index.html — every vX.Y.Z / X.Y.Z marker on the page must agree
    # (softwareVersion in the JSON-LD, the hero eyebrow, the footer).
    html = _read(os.path.join("docs", "index.html"))
    hits = [(m.start(), m.group(1))
            for m in re.finditer(r"\bv?" + _SEMVER + r"\b", html)]
    if not hits:
        yield "docs/index.html version markers", None
    for pos, ver in hits:
        line = html.count("\n", 0, pos) + 1
        yield "docs/index.html line %d" % line, ver


def main():
    found = list(_versions())
    reference = next((v for _, v in found if v), None)
    missing = [label for label, v in found if v is None]
    drifted = [(label, v) for label, v in found if v and v != reference]
    if missing or drifted:
        print("VERSION DRIFT (every source must carry the same version):")
        for label in missing:
            print("  %s: no version string found" % label)
        for label, v in drifted:
            print("  %s: %s (expected %s)" % (label, v, reference))
        return 1
    print("version sync OK — all %d sources at %s" % (len(found), reference))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
