#!/usr/bin/env python3
"""Guard: docs/slop.js must carry the same rule inventory as flag_slop.py.

The in-browser scorer is a hand-port of the Python detector. Behaviour can differ
slightly on regex-engine edge cases, but the *inventory* must not drift — every
rule type and every severity weight has to exist on both sides, with identical
weight values. This catches the real failure mode: adding a rule to the Python
detector (and the eval) but forgetting the website tool, or vice versa.

Pure stdlib, no Node required — parses slop.js as text.

Usage: python3 tests/check_js_parity.py
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "scripts"))

from flag_slop import _RULES, _WEIGHTS  # noqa: E402

# empower + emdash are sentence-aware (not in _RULES) but are real rule types.
_SPECIAL = {"empower", "emdash"}


def py_inventory():
    types = {t[0] for t in _RULES} | _SPECIAL
    return types, dict(_WEIGHTS)


def js_inventory():
    js = open(os.path.join(_ROOT, "docs", "slop.js"), encoding="utf-8").read()
    # weights between the PARITY markers
    block = re.search(r"PARITY:WEIGHTS-START(.*?)PARITY:WEIGHTS-END", js, re.S)
    if not block:
        raise SystemExit("slop.js: PARITY:WEIGHTS markers not found")
    weights = {k: int(v) for k, v in re.findall(r"(\w+):\s*(\d+)", block.group(1))}
    # rule types declared in the RULES array: ["type", ...
    types = set(re.findall(r'\[\s*"(\w+)"\s*,', js)) | _SPECIAL
    return types, weights


def main():
    pt, pw = py_inventory()
    jt, jw = js_inventory()
    problems = []
    if pt != jt:
        problems.append(f"rule TYPES differ:\n  only in python: {sorted(pt - jt)}\n"
                        f"  only in js:     {sorted(jt - pt)}")
    if pw != jw:
        only_py = {k: pw[k] for k in pw if pw.get(k) != jw.get(k)}
        only_js = {k: jw[k] for k in jw if jw.get(k) != pw.get(k)}
        problems.append(f"WEIGHTS differ:\n  python: {only_py}\n  js:     {only_js}")
    missing_w = (pt | jt) - set(pw) - _SPECIAL
    # _SPECIAL types must also have a weight on both sides
    for s in _SPECIAL:
        if s not in pw or s not in jw:
            problems.append(f"special type '{s}' missing a weight")
    if missing_w:
        problems.append(f"types with no weight: {sorted(missing_w)}")

    if problems:
        print("JS PARITY FAIL — docs/slop.js out of sync with flag_slop.py:\n")
        print("\n\n".join(problems))
        return 1
    print(f"js parity OK — {len(pt)} rule types, {len(pw)} weights match")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
