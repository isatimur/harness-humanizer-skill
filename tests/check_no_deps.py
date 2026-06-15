#!/usr/bin/env python3
"""Guard the zero-dependency promise.

Walks scripts/ and tests/ and fails if anything imports a non-stdlib module.
The skill's whole point is "copy it in and it just works" — no pip, no setup.
This stops a future contributor from quietly adding a dependency.

Usage: python3 tests/check_no_deps.py   (exit 0 clean, 1 if a dep sneaks in)
"""
import ast
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

# Modules the project deliberately uses. Everything else must be stdlib.
_ALLOWED = {"json", "re", "sys", "os", "ast", "argparse", "io", "pathlib",
            "collections", "itertools", "textwrap", "math", "string"}

# 3.10+ knows its own stdlib; older versions fall back to the allowlist only.
_STDLIB = getattr(sys, "stdlib_module_names", frozenset())


def _imports(path):
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                yield a.name.split(".")[0]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:  # skip relative imports
                yield node.module.split(".")[0]


def main():
    offenders = []
    for sub in ("scripts", "tests"):
        for root, _, files in os.walk(os.path.join(_ROOT, sub)):
            for f in files:
                if not f.endswith(".py"):
                    continue
                path = os.path.join(root, f)
                for mod in _imports(path):
                    # local modules (e.g. flag_slop) live in scripts/, are fine
                    if os.path.exists(os.path.join(_ROOT, "scripts", mod + ".py")):
                        continue
                    if mod in _ALLOWED or mod in _STDLIB:
                        continue
                    offenders.append((os.path.relpath(path, _ROOT), mod))
    if offenders:
        print("NON-STDLIB IMPORTS FOUND (the skill must stay zero-dependency):")
        for path, mod in offenders:
            print(f"  {path}: import {mod}")
        return 1
    print("zero-dependency check OK — stdlib only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
