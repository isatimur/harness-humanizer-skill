#!/usr/bin/env python3
"""Deterministic slop pre-flagger for the harness-humanizer skill.

Cheap regex pass that narrows attention before the model judges. Emits JSON
candidates — NOT verdicts. The model still scores every paragraph against the
rubric; this just surfaces the obvious offenders fast.

Usage:
    python3 flag_slop.py FILE
    cat text | python3 flag_slop.py
    python3 flag_slop.py --selftest

Output: JSON array of {line, type, pattern, span}.
"""
import json
import re
import sys

# (type, human-readable pattern, compiled regex) — case-insensitive.
_RULES = [
    ("hedge", "empty hedging stem",
     re.compile(r"\b(it'?s|it is) (worth noting|important to (note|remember|understand))\b"
                r"|\b(that said|needless to say|as we all know|at the end of the day)\b", re.I)),
    ("listicle", "listicle stem with no point",
     re.compile(r"\b(there are (several|a number of|many) (key |important )?"
                r"(factors|considerations|things|ways|reasons)|"
                r"here are (a few|some|several)|let'?s (explore|dive into|take a look))\b", re.I)),
    ("transition", "dead transition",
     re.compile(r"(?m)^\s*(moreover|furthermore|in addition|additionally)\b[,]?", re.I)),
    ("stakes", "manufactured stakes",
     re.compile(r"\b(in today'?s (fast-paced |digital |modern )?(world|landscape|era)|"
                r"now more than ever|more important than ever|"
                r"the stakes have never been higher)\b", re.I)),
    ("candor", "performed candor",
     re.compile(r"\b(let'?s be honest|let'?s be real|here'?s the thing|"
                r"truth be told|i'?ll be honest)\b", re.I)),
    ("rhetq", "rhetorical-question opener",
     re.compile(r"(?m)^\s*(what if i told you|ever wondered|have you ever)\b", re.I)),
    ("notonly", "not-only-but-also padding",
     re.compile(r"\bnot only\b.*\bbut also\b", re.I)),
    ("intensifier", "filler intensifier",
     re.compile(r"\b(very|really|truly|genuinely|honestly|literally|incredibly|"
                r"extremely)\s+\w+", re.I)),
]


def _emdash_hits(text):
    """Flag sentences with >=2 em dashes (theatrics)."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        for sent in re.split(r"(?<=[.!?])\s+", line):
            if sent.count("—") >= 2:
                out.append({"line": i, "type": "emdash",
                            "pattern": "em-dash density (>=2 in a sentence)",
                            "span": sent.strip()[:120]})
    return out


def flag(text):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for typ, label, rx in _RULES:
            for m in rx.finditer(line):
                hits.append({"line": i, "type": typ, "pattern": label,
                             "span": m.group(0).strip()[:120]})
    hits.extend(_emdash_hits(text))
    hits.sort(key=lambda h: (h["line"], h["type"]))
    return hits


_SELFTEST = (
    "It's worth noting that caching helps.\n"
    "There are several key factors to consider here.\n"
    "Moreover, the system is robust.\n"
    "In today's fast-paced world, speed matters.\n"
    "Let's be honest, nobody reads docs.\n"
    "This is a very important and really useful tool.\n"
    "It was fast — clean — and obviously correct — somehow.\n"
    "A cache miss costs the full computation plus storage bookkeeping.\n"  # clean, no hit
)


def _selftest():
    hits = flag(_SELFTEST)
    types = {h["type"] for h in hits}
    expected = {"hedge", "listicle", "transition", "stakes", "candor",
                "intensifier", "emdash"}
    missing = expected - types
    # the clean last line (line 8) must produce no hits
    clean_line_hits = [h for h in hits if h["line"] == 8]
    ok = not missing and not clean_line_hits
    print(json.dumps({
        "ok": ok,
        "types_found": sorted(types),
        "missing": sorted(missing),
        "false_positives_on_clean_line": clean_line_hits,
        "total_hits": len(hits),
    }, indent=2))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) > 1 and not argv[1].startswith("-"):
        text = open(argv[1], encoding="utf-8").read()
    else:
        text = sys.stdin.read()
    print(json.dumps(flag(text), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
