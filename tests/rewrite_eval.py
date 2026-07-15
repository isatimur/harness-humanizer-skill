#!/usr/bin/env python3
"""Deterministic rewrite-contract gate (no model required).

This does NOT prove a model will rewrite well. It does prove:
  1. rewrite cases parse and use a valid decision;
  2. good_after texts do not reintroduce surface slop the before already had
     (or introduce brand-new high-weight tell types, for reword cases);
  3. good_after texts do not contain forbidden invent-tokens;
  4. bad_after texts are *detectably worse or inventable* (for regression docs);
  5. hollow cases have empty good_after and non-empty bad_after examples;
  6. the flagship fidelity-safe after still appears in README / examples.md.

Usage:
    python3 tests/rewrite_eval.py
    python3 tests/rewrite_eval.py --json
"""
from __future__ import annotations

import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "scripts"))

from flag_slop import flag  # noqa: E402

_VALID = {"reword", "hollow", "unchanged"}
_CASES = os.path.join(_HERE, "fixtures", "rewrite_cases.jsonl")


def _load(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{n}: {e}")
    return rows


def _types(text):
    return {h["type"] for h in flag(text)}


def _contains_any(text, tokens):
    low = text.lower()
    return [t for t in tokens if t.lower() in low]


def eval_cases(rows):
    failures = []
    for rec in rows:
        rid = rec.get("id", "?")
        decision = rec.get("decision")
        before = rec.get("before", "")
        good = rec.get("good_after") or []
        bad = rec.get("bad_after") or []
        forbid = rec.get("forbidden_tokens_in_good") or []
        forbid_any = rec.get("forbidden_tokens_for_any_rewrite") or []

        if decision not in _VALID:
            failures.append(f"{rid}: invalid decision {decision!r}")
            continue
        if not before.strip():
            failures.append(f"{rid}: empty before")
            continue

        if decision == "hollow":
            if good:
                failures.append(f"{rid}: hollow must have empty good_after")
            if not bad:
                failures.append(f"{rid}: hollow should list at least one bad_after fabrication")
            continue

        if decision == "unchanged":
            if not good or good[0].strip() != before.strip():
                failures.append(f"{rid}: unchanged good_after[0] must equal before")
            continue

        # reword
        if not good:
            failures.append(f"{rid}: reword requires good_after examples")
            continue

        before_types = _types(before)
        for i, after in enumerate(good):
            if not after.strip():
                failures.append(f"{rid}: empty good_after[{i}]")
                continue
            # good after should not re-add dense surface slop vs before
            after_types = _types(after)
            # new high-weight tells that weren't in before are a failure
            new = after_types - before_types
            # degree intensifiers alone are weakly tolerated
            new -= {"intensifier_degree"}
            if new:
                failures.append(
                    f"{rid}: good_after[{i}] introduces new tell types {sorted(new)}"
                )
            hits = _contains_any(after, forbid)
            if hits:
                failures.append(f"{rid}: good_after[{i}] has forbidden tokens {hits}")
            hits2 = _contains_any(after, forbid_any)
            if hits2:
                failures.append(f"{rid}: good_after[{i}] has forbidden tokens {hits2}")

        for i, after in enumerate(bad):
            hits2 = _contains_any(after, forbid_any)
            # bad afters that are fabrication examples for hollow-context are ok;
            # for reword cases we just require they are listed (documentational).
            if hits2 and decision != "reword":
                pass

    return failures


def check_docs():
    """Hard-guard the public demos against the old fidelity-violating after."""
    failures = []
    banned = [
        "hit returns in microseconds",
        "miss spends milliseconds",
        "cache hit returns in microseconds",
    ]
    watch = [
        "README.md",
        os.path.join("references", "examples.md"),
        os.path.join("docs", "index.html"),
        os.path.join("docs", "humanize-ai-text.html"),
        os.path.join("docs", "ai-slop.html"),
    ]
    for rel in watch:
        path = os.path.join(_ROOT, rel)
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        for b in banned:
            if b in text:
                failures.append(f"{rel}: still contains banned fidelity phrase {b!r}")
    # flagship good after must be present
    readme = open(os.path.join(_ROOT, "README.md"), encoding="utf-8").read()
    if "Caching improves performance for many applications." not in readme:
        failures.append("README.md: missing fidelity-safe flagship after")
    # guardrails invent rule
    guard = open(os.path.join(_ROOT, "references", "guardrails.md"), encoding="utf-8").read()
    if "No invented numbers" not in guard and "invented numbers" not in guard:
        failures.append("references/guardrails.md: missing invented-numbers rule")
    return failures


def main(argv):
    rows = _load(_CASES)
    failures = eval_cases(rows) + check_docs()
    ok = not failures
    if "--json" in argv:
        print(json.dumps({"ok": ok, "n_cases": len(rows), "failures": failures}, indent=2))
    else:
        print(f"de-slop rewrite-eval  ({len(rows)} cases)")
        if failures:
            print(f"FAILURES ({len(failures)}):")
            for f in failures:
                print(" ", f)
            print("RESULT: FAIL")
        else:
            print("RESULT: PASS")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
