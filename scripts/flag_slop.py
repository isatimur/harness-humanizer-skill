#!/usr/bin/env python3
"""Deterministic slop pre-flagger for the harness-humanizer skill.

Cheap regex pass that narrows attention before the model judges. Emits JSON
candidates — NOT verdicts. The model still scores every paragraph against the
rubric; this just surfaces the obvious offenders fast.

Two surfaces:
  * flag(text)  -> list[{line, type, pattern, span}]   (line-oriented candidates)
  * score(text) -> {v, paragraphs[...], overall{...}}   (per-paragraph slop_band)

`flag()` and the default CLI keep the v0.1.0 hit shape. Severity scoring is
additive via score()/--score. The score measures SURFACE SLOP TELLS ONLY — it is
not a humanness judge. A paragraph with zero slop words can still be hollow (no
claim) and fail the rubric; the detector cannot see that. `slop_band` means
"how many surface tells", never "how good the writing is".

Usage:
    python3 flag_slop.py FILE
    cat text | python3 flag_slop.py
    python3 flag_slop.py --score FILE      # per-paragraph slop_band JSON
    python3 flag_slop.py --selftest

Output: JSON array of {line, type, pattern, span} (default), or the score object
with --score.
"""
import json
import re
import sys

__version__ = "0.2.1"

# (type, human-readable pattern, compiled regex) — case-insensitive.
# Adding a rule? Give it a weight in _WEIGHTS and a corpus sample in tests/.
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
    # --- intensifier, split: filler adverbs (real over-correction tell) vs.
    #     degree words (often legitimate, kept as a low-weight candidate) ---
    ("intensifier_filler", "filler intensifier adverb",
     re.compile(r"\b(truly|genuinely|honestly|literally|simply|basically|"
                r"essentially|undoubtedly|certainly|definitely)\s+\w+", re.I)),
    ("intensifier_degree", "degree intensifier (often legit)",
     # require a lowercase, modifiable follower — kills "very Tuesday"
     # (proper noun) and "very much"/"really the" (function-word) false hits.
     # NB: compiled WITHOUT global re.I so the [A-Z] proper-noun guard stays
     # case-sensitive; the intensifier word + stoplist are case-folded inline.
     re.compile(r"\b(?i:very|really|extremely|incredibly|quite|rather)\s+"
                r"(?i:(?!the\b|a\b|an\b|of\b|to\b|in\b|on\b|much\b|many\b|"
                r"few\b|little\b|more\b))(?![A-Z])[a-z]\w+")),
    # --- new rule types (v0.2.0) ---
    ("weaselquant", "vague quantifier",
     re.compile(r"\b(a (wide|broad) (variety|range|array) of|a number of|"
                r"numerous|countless|myriad|a host of|a plethora of|"
                r"various (different )?)\b", re.I)),
    ("negparallel", "negative-parallel cadence",
     re.compile(r"\b(it'?s not (just|merely|only)\b.*\bit'?s\b"
                r"|this isn'?t (just )?about\b.*\bit'?s about\b)", re.I)),
    ("delve", "LLM-lexicon filler",
     re.compile(r"\b(delv(e|es|ing)|tapestry|a testament to|"
                r"(in )?the realm of|navigat(e|es|ing) the (complex|intricat|nuanc)"
                r"|at the end of the day|when it comes to)\b", re.I)),
    ("conclusion", "wrap-up scaffolding",
     re.compile(r"(?mi)^\s*(in conclusion|to sum up|in summary|to summarize|"
                r"all in all)\b|\bthe key takeaway( here)? is\b", re.I)),
    # NB: 'empower' is NOT a plain regex rule — it is sentence-aware (see
    # _empower_hits) so that standalone "leverage"/"robust" in genuine technical
    # prose stays silent. Only marketing-register buzzwords fire on their own.
    ("triadic", "rule-of-three buzzword triplet",
     re.compile(r"\b(fast|reliable|scalable|secure|robust|powerful|flexible|"
                r"intuitive|seamless|efficient|innovative|modern),?\s+"
                r"(fast|reliable|scalable|secure|robust|powerful|flexible|"
                r"intuitive|seamless|efficient|innovative|modern),?\s+and\s+"
                r"(fast|reliable|scalable|secure|robust|powerful|flexible|"
                r"intuitive|seamless|efficient|innovative|modern)\b", re.I)),
    ("calltoaction", "throat-clearing call to action",
     re.compile(r"\b(let'?s dive (in|right in)|dive right in|buckle up|"
                r"stay tuned|without further ado|let'?s get started|read on)\b", re.I)),
]

# Severity weights — the tuning surface. Higher = stronger slop tell.
# Bands align to references/rubric.md cutoffs once turned into a 0..100 score.
_WEIGHTS = {
    "listicle": 20, "stakes": 20, "candor": 18, "rhetq": 18,
    "calltoaction": 16, "delve": 16, "hedge": 15, "conclusion": 14,
    "emdash": 12, "weaselquant": 12, "negparallel": 12,
    "transition": 10, "notonly": 10, "intensifier_filler": 10,
    "empower": 8, "triadic": 8, "intensifier_degree": 6,
}


# 'empower' buzzwords, split by how often they appear in HONEST technical prose.
# Marketing terms almost never do — they fire on their own. Riders (leverage,
# robust, unlock, …) are common in real engineering writing, so they fire ONLY
# when a marketing term shares the sentence (i.e. the register is already slop).
_EMPOWER_MARKETING = re.compile(
    r"\b(empower(s|ing)?|seamless(ly)?|frictionless|turnkey|synerg(y|ies)|"
    r"cutting-edge|bleeding-edge|state-of-the-art|best-in-class|world-class|"
    r"game-?chang(er|ing)|supercharg(e|es|ing)|next-generation|paradigm shift)\b",
    re.I)
_EMPOWER_RIDER = re.compile(
    r"\b(leverag(e|es|ing|ed)|robust|unlock(s|ing|ed)?|harness(es|ing)?|"
    r"elevate(s|d)?|streamlin(e|es|ed|ing))\b", re.I)


def _empower_hits(text):
    """Corporate-uplift buzzwords, sentence-aware.

    Marketing-register words always flag. Ambiguous 'rider' words (leverage,
    robust, …) flag only when a marketing word shares the sentence — so
    "we leverage Postgres connection pooling" stays silent while "empowers teams
    to leverage cutting-edge tooling" does not.
    """
    out = []
    label = "corporate-uplift buzzword"
    for i, line in enumerate(text.splitlines(), 1):
        for sent in re.split(r"(?<=[.!?])\s+", line):
            marketing = list(_EMPOWER_MARKETING.finditer(sent))
            for m in marketing:
                out.append({"line": i, "type": "empower", "pattern": label,
                            "span": m.group(0).strip()[:120]})
            if marketing:  # register is already marketing → riders count too
                for m in _EMPOWER_RIDER.finditer(sent):
                    out.append({"line": i, "type": "empower", "pattern": label,
                                "span": m.group(0).strip()[:120]})
    return out


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
    """Line-oriented slop candidates. Output shape is stable since v0.1.0."""
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for typ, label, rx in _RULES:
            for m in rx.finditer(line):
                hits.append({"line": i, "type": typ, "pattern": label,
                             "span": m.group(0).strip()[:120]})
    hits.extend(_empower_hits(text))
    hits.extend(_emdash_hits(text))
    hits.sort(key=lambda h: (h["line"], h["type"]))
    return hits


# --- severity scoring (additive; never replaces flag()) ---------------------

_BLANK = re.compile(r"^\s*$")
_SKIP_FIRST = re.compile(r"^\s*(#|>|[-*+]\s|\d+[.)]\s)")  # heading/quote/list


def _paragraphs(text):
    """Yield (start_line, [lines]) for in-scope paragraphs.

    Splits on blank lines. Skips fenced code blocks, and any paragraph whose
    first line opens a heading, blockquote, or list — same scope rules SKILL.md
    declares. Mirrors the model's step-0 so detector and skill agree on scope.
    """
    lines = text.splitlines()
    in_fence = False
    para, start = [], None
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if _BLANK.match(line):
            if para and para != ["__skip__"]:
                yield start, para
            para, start = [], None
            continue
        if not para:
            start = i
            if _SKIP_FIRST.match(line):
                # consume the rest of this non-scope block without emitting
                para = ["__skip__"]
                continue
        if para == ["__skip__"]:
            continue
        para.append(line)
    if para and para != ["__skip__"]:
        yield start, para


def _band(score):
    if score >= 80:
        return "strong"
    if score >= 50:
        return "moderate"
    if score >= 20:
        return "weak"
    return "fail"


def _score_paragraph(start_line, lines):
    text = "\n".join(lines)
    hits = flag(text)
    # remap hit line numbers to absolute file lines
    for h in hits:
        h["line"] = start_line + h["line"] - 1
    words = max(len(re.findall(r"\b\w+\b", text)), 1)
    raw = sum(_WEIGHTS.get(h["type"], 8) for h in hits)
    density_bonus = min(20, (len(hits) / words) * 100 * 4)
    penalty = min(100, raw + density_bonus)
    slop_score = max(0, round(100 - penalty))
    by_type = {}
    for h in hits:
        by_type[h["type"]] = by_type.get(h["type"], 0) + 1
    return {
        "index": None, "line_start": start_line, "words": words,
        "slop_score": slop_score, "slop_band": _band(slop_score),
        "hits": hits, "by_type": by_type,
    }, words


def score(text):
    """Per-paragraph slop_band. SURFACE TELLS ONLY — not a humanness judge."""
    paras, weights = [], []
    for idx, (start, lines) in enumerate(_paragraphs(text)):
        p, w = _score_paragraph(start, lines)
        p["index"] = idx
        paras.append(p)
        weights.append(w)
    total_words = sum(weights) or 1
    overall_score = round(
        sum(p["slop_score"] * w for p, w in zip(paras, weights)) / total_words
    ) if paras else 100
    return {
        "v": 2,
        "note": "slop_band measures surface slop tells only, not humanness; "
                "a clean-scoring paragraph can still be hollow (no claim).",
        "paragraphs": paras,
        "overall": {
            "slop_score": overall_score, "slop_band": _band(overall_score),
            "paragraph_count": len(paras),
            "total_hits": sum(len(p["hits"]) for p in paras),
        },
    }


# --- selftest ----------------------------------------------------------------

_SELFTEST = (
    "It's worth noting that caching helps.\n"          # 1  hedge
    "There are several key factors to consider here.\n"  # 2  listicle
    "Moreover, the system is robust.\n"                # 3  transition; empower SILENT (standalone robust)
    "In today's fast-paced world, speed matters.\n"    # 4  stakes
    "Let's be honest, nobody reads docs.\n"            # 5  candor
    "This is a truly important and really useful tool.\n"  # 6  filler + degree
    "It was fast — clean — and obviously correct — somehow.\n"  # 7  emdash
    "We must delve into the rich tapestry of various options.\n"  # 8  delve+weaselquant
    "Buckle up, in conclusion the key takeaway is clear.\n"  # 9  calltoaction+conclusion
    "Our seamless platform empowers teams to leverage cutting-edge tools.\n"  # 10 empower (marketing cluster)
    "A cache miss costs the full computation plus storage bookkeeping.\n"  # 11 clean
    "We support very old browsers for compatibility.\n"  # 12 degree only (legit, low wt)
    "The pipeline is robust and we leverage caching for speed.\n"  # 13 clean (empower riders, no marketing → SILENT)
)
# absolute line numbers in _SELFTEST that must produce NO hit
_CLEAN_LINES = {11, 13}


def _selftest():
    hits = flag(_SELFTEST)
    types = {h["type"] for h in hits}
    expected = {"hedge", "listicle", "transition", "stakes", "candor",
                "intensifier_filler", "intensifier_degree", "emdash",
                "delve", "weaselquant", "calltoaction", "conclusion",
                "empower"}
    missing = expected - types
    clean_line_hits = [h for h in hits if h["line"] in _CLEAN_LINES]
    # the degree-only line (12) must NOT contain a stronger tell than degree
    degree_line = [h for h in hits if h["line"] == 12]
    degree_ok = all(h["type"] == "intensifier_degree" for h in degree_line) \
        and len(degree_line) >= 1
    # standalone 'robust' (line 3) must NOT raise an empower hit
    empower_silent_ok = not [h for h in hits
                             if h["line"] in {3, 13} and h["type"] == "empower"]
    # scoring sanity: slop-heavy text scores low; clean line scores strong
    sc = score(_SELFTEST)
    ok = (not missing and not clean_line_hits and degree_ok
          and empower_silent_ok and sc["overall"]["slop_band"] in {"weak", "fail"})
    print(json.dumps({
        "ok": ok,
        "version": __version__,
        "types_found": sorted(types),
        "missing": sorted(missing),
        "false_positives_on_clean_line": clean_line_hits,
        "degree_line_ok": degree_ok,
        "empower_silent_on_standalone_riders": empower_silent_ok,
        "overall_slop_band": sc["overall"]["slop_band"],
        "total_hits": len(hits),
    }, indent=2))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    want_score = "--score" in argv
    args = [a for a in argv[1:] if not a.startswith("-")]
    if args:
        text = open(args[0], encoding="utf-8").read()
    else:
        text = sys.stdin.read()
    out = score(text) if want_score else flag(text)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
