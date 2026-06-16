# Contributing corpus samples

Found prose the detector mishandled? **Add the line that proves it.** The corpus
is the skill's regression net — every real-world sample makes the detector harder
to fool and locks the fix in place.

## What the eval tests (and what it doesn't)

`tests/eval.py` tests **detector behaviour only** — does `scripts/flag_slop.py`
fire on slop and stay quiet on clean prose. It does **not** test rewrite quality,
rewordable-vs-hollow triage, or humanness; those need a model and live in
`references/`. A green eval means the candidate-surfacer behaves, not that the
writing is good.

## Pick the right file

The corpus lives in `tests/corpus/` as JSONL (one sample per line — so your PR is
a one-line diff and a malformed line fails in isolation):

| Symptom | File | Meaning |
|---|---|---|
| Detector stayed **silent** on obvious slop | `slop.jsonl` | should fire |
| Detector **fired** on genuinely clean prose | `clean.jsonl` | should stay quiet |
| **Edgy-slop** slipped through (hot take, performed candor, em-dash theatrics) | `overcorrection.jsonl` | must also fire |

Over-correction is the one that matters most: a humanizer that trades AI-slop for
louder slop has failed. The eval gates `overcorrection.jsonl` at 100% recall — but
only for **lexically detectable** edgy-slop (something with trigger words a regex
can see). Semantic edgy-slop with no trigger words (e.g. a fabricated contrarian
stance in plain words) can't be caught by regex; it belongs in `references/`, not
this gated corpus.

## Record schema

```json
{
  "id": "slop-hedge-007",
  "text": "It's worth noting that this matters.",
  "expect": ["hedge"],
  "band": "fail",
  "source": "real-world",
  "note": "why this sample is here"
}
```

- **`id`** — unique; prefix by file (`slop-`, `clean-`, `oc-`).
- **`text`** — one logical line, no embedded newlines (the detector is line-oriented).
- **`expect`** — rule `type`s that MUST fire. `[]` on a slop sample means "any
  hit"; on a clean sample it means "zero hits".
- **`allow`** *(clean only, optional)* — types tolerated without counting as a
  false positive. Use for low-weight candidates that legitimately appear in clean
  prose, e.g. `"allow": ["intensifier_degree"]` for "very old browsers" or
  `"allow": ["empower"]` for a genuine technical "leverage". These fire as
  candidates (correct) but shouldn't redden the build.
- **`band`** *(optional)* — expected rubric band (`strong|moderate|weak|fail`).
- **`source`** — `synthetic` | `real-world` | `examples.md`. **Real-world samples
  are the growth metric** — mark them so coverage is visible.
- **`note`** — free text, why it's here.

## Workflow

```bash
# add your line to the right tests/corpus/*.jsonl file, then:
python3 tests/eval.py            # all gates must PASS
python3 scripts/flag_slop.py --selftest
```

Open a PR. If you added a clean sample that the detector wrongly flags, that's a
detector bug — either tighten the rule in `flag_slop.py` or, if the hit is a
legitimate low-weight candidate, add it to `allow` and say why in `note`.
