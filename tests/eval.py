#!/usr/bin/env python3
"""Detector eval for the de-slop skill.

Deterministic, zero-dependency regression gate for scripts/flag_slop.py. It
tests DETECTOR BEHAVIOUR ONLY — does the regex pass fire on slop and stay quiet
on clean prose — NOT rewrite quality, triage, or humanness. Those need a model
and live in references/, not here. A green eval means "the candidate-surfacer
behaves", never "the writing is good".

Four things it checks:
  1. recall            — labeled slop lines produce the expected rule type(s)
  2. clean specificity — labeled clean lines stay quiet (modulo an `allow` list)
  3. idempotence proxy — the 'after'/strong exemplars (in clean.jsonl) don't refire
  4. over-correction   — edgy-slop (performed candor, em-dash theatrics) MUST also
                         fire; the detector catches louder-slop, not just AI-slop

Usage:
    python3 tests/eval.py                 # human report; exit 0 (pass) / 1 (fail)
    python3 tests/eval.py --json          # machine-readable result
    python3 tests/eval.py --corpus DIR    # alternate corpus dir
    python3 tests/eval.py --no-fail       # always exit 0 (local exploration)
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "scripts"))

from flag_slop import flag  # noqa: E402  (real detector, not a reimplementation)


def _load_jsonl(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{n}: malformed JSONL — {e}")
    return rows


def _hit_types(text):
    return [h["type"] for h in flag(text)]


def _eval_positive(rec):
    """slop / over-correction: TP if every expected type fires."""
    types = set(_hit_types(rec["text"]))
    expect = rec.get("expect", [])
    if expect:
        ok = all(t in types for t in expect)
    else:
        ok = len(types) > 0
    return ok, types


def _eval_clean(rec):
    """clean: TN if no DISALLOWED type fires (an `allow` list is tolerated)."""
    allow = set(rec.get("allow", []))
    hits = flag(rec["text"])
    bad = [h for h in hits if h["type"] not in allow]
    return (len(bad) == 0), bad


def run(corpus_dir):
    slop = _load_jsonl(os.path.join(corpus_dir, "slop.jsonl"))
    clean = _load_jsonl(os.path.join(corpus_dir, "clean.jsonl"))
    oc = _load_jsonl(os.path.join(corpus_dir, "overcorrection.jsonl"))

    positives = [("slop", r) for r in slop] + [("oc", r) for r in oc]
    tp = fn = 0
    oc_tp = oc_fn = 0
    misses = []
    # per-type recall: expected vs. caught
    pt_expected, pt_caught = {}, {}
    for kind, rec in positives:
        ok, types = _eval_positive(rec)
        for t in rec.get("expect", []):
            pt_expected[t] = pt_expected.get(t, 0) + 1
            if t in types:
                pt_caught[t] = pt_caught.get(t, 0) + 1
        if ok:
            tp += 1
            if kind == "oc":
                oc_tp += 1
        else:
            fn += 1
            if kind == "oc":
                oc_fn += 1
            misses.append({"id": rec["id"], "text": rec["text"],
                           "expected": rec.get("expect", []),
                           "got": sorted(types)})

    tn = fp = 0
    false_positives = []
    pt_fp = {}
    for rec in clean:
        ok, bad = _eval_clean(rec)
        if ok:
            tn += 1
        else:
            fp += 1
            for h in bad:
                pt_fp[h["type"]] = pt_fp.get(h["type"], 0) + 1
            false_positives.append({"id": rec["id"], "text": rec["text"],
                                    "hits": [f'{h["type"]}:"{h["span"]}"'
                                             for h in bad]})

    recall = tp / (tp + fn) if (tp + fn) else 1.0
    clean_spec = tn / (tn + fp) if (tn + fp) else 1.0
    oc_recall = oc_tp / (oc_tp + oc_fn) if (oc_tp + oc_fn) else 1.0
    per_type = {
        t: {"expected": pt_expected[t], "caught": pt_caught.get(t, 0),
            "recall": round(pt_caught.get(t, 0) / pt_expected[t], 3)}
        for t in sorted(pt_expected)
    }
    return {
        "counts": {"slop": len(slop), "clean": len(clean), "oc": len(oc),
                   "tp": tp, "fn": fn, "tn": tn, "fp": fp},
        "metrics": {"recall": round(recall, 3),
                    "clean_specificity": round(clean_spec, 3),
                    "oc_recall": round(oc_recall, 3),
                    "false_positives": fp},
        "per_type": per_type,
        "per_type_fp": pt_fp,
        "misses": misses,
        "false_positive_detail": false_positives,
    }


def gate(result, thresholds):
    m = result["metrics"]
    checks = [
        ("recall", m["recall"], ">=", thresholds.get("min_recall", 0.0)),
        ("clean_specificity", m["clean_specificity"], ">=",
         thresholds.get("min_clean_specificity", 0.0)),
        ("oc_recall", m["oc_recall"], ">=",
         thresholds.get("overcorrection_min_recall", 0.0)),
        ("false_positives", m["false_positives"], "<=",
         thresholds.get("max_false_positives", 10 ** 9)),
    ]
    results = []
    for name, val, op, gate_val in checks:
        ok = val >= gate_val if op == ">=" else val <= gate_val
        results.append({"check": name, "value": val, "op": op,
                        "gate": gate_val, "pass": ok})
    for typ, minr in thresholds.get("per_type_min_recall", {}).items():
        pt = result["per_type"].get(typ, {"recall": 1.0})
        ok = pt["recall"] >= minr
        results.append({"check": f"per_type_recall[{typ}]",
                        "value": pt["recall"], "op": ">=", "gate": minr,
                        "pass": ok})
    return results, all(c["pass"] for c in results)


_BANNER = ("de-slop detector eval  "
           "(tests DETECTOR behaviour only — NOT rewrite quality or humanness)")


def _report(result, gate_results, passed):
    c, m = result["counts"], result["metrics"]
    print(_BANNER)
    print(f"corpus: {c['slop']} slop / {c['clean']} clean / {c['oc']} over-correction\n")
    for g in gate_results:
        verdict = "PASS" if g["pass"] else "FAIL"
        print(f"  {g['check']:<24} {g['value']:<7} "
              f"gate {g['op']} {g['gate']:<6} {verdict}")
    print("\nper-type recall:")
    for t, d in result["per_type"].items():
        print(f"  {t:<20} {d['recall']:<5} ({d['caught']}/{d['expected']})")
    if result["per_type_fp"]:
        print("\nper-type false positives on clean:")
        for t, n in sorted(result["per_type_fp"].items()):
            print(f"  {t:<20} {n}")
    if result["misses"]:
        print(f"\nMISSES ({len(result['misses'])}):")
        for mrec in result["misses"]:
            print(f"  {mrec['id']}  expected{mrec['expected']} "
                  f"got{mrec['got']}  \"{mrec['text'][:70]}\"")
    if result["false_positive_detail"]:
        print(f"\nFALSE POSITIVES ({len(result['false_positive_detail'])}):")
        for f in result["false_positive_detail"]:
            print(f"  {f['id']}  {f['hits']}  \"{f['text'][:60]}\"")
    print(f"\nRESULT: {'PASS' if passed else 'FAIL'}")


def main(argv):
    corpus_dir = os.path.join(_HERE, "corpus")
    if "--corpus" in argv:
        corpus_dir = argv[argv.index("--corpus") + 1]
    thresholds_path = os.path.join(_HERE, "thresholds.json")
    thresholds = (json.load(open(thresholds_path))
                  if os.path.exists(thresholds_path) else {})

    result = run(corpus_dir)
    gate_results, passed = gate(result, thresholds)

    if "--json" in argv:
        print(json.dumps({"ok": passed, "thresholds": thresholds,
                          "gates": gate_results, **result}, indent=2))
    else:
        _report(result, gate_results, passed)

    if "--no-fail" in argv:
        return 0
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
