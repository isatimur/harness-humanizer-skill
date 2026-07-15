# Contributing corpus samples

Found prose the detector mishandled? **Add the line that proves it.** The corpus
is the skill's regression net — every real-world sample makes the detector harder
to fool and locks the fix in place.

## What the evals test (and what they don't)

| Gate | File | Tests |
|---|---|---|
| Detector | `tests/eval.py` + `tests/corpus/*.jsonl` | regex fires on slop, silent on clean, catches over-correction |
| Rewrite contract | `tests/rewrite_eval.py` + `tests/fixtures/rewrite_cases.jsonl` | hollow vs reword decisions, fidelity-safe afters, banned invented-demo phrases |

Neither gate substitutes for a live model pass. A green detector eval means the
candidate-surfacer behaves. A green rewrite-eval means demos and fixtures have
not drifted into fabrication.

## Pick the right detector corpus file

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
stance in plain words) can't be caught by regex; it belongs in `references/` and
in `rewrite_cases.jsonl`, not this gated corpus.

## Detector record schema

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
  false positive.
- **`band`** *(optional)* — expected rubric band (`strong|moderate|weak|fail`).
- **`source`** — `synthetic` | `real-world` | `examples.md`. **Real-world samples
  are the growth metric.**
- **`note`** — free text, why it's here.

## Rewrite-case schema

```json
{
  "id": "rewrite-hedge-pure",
  "decision": "reword",
  "before": "…",
  "good_after": ["…"],
  "bad_after": ["…"],
  "forbidden_tokens_in_good": ["microsecond"],
  "note": "…"
}
```

`decision` is `reword | hollow | unchanged`. Hollow cases must list empty
`good_after` and at least one fabricated `bad_after`. Reword `good_after`s must
not introduce high-weight tell types or forbidden invent-tokens.

## Workflow

```bash
# add your line to the right tests/corpus/*.jsonl file, then:
python3 tests/eval.py            # all gates must PASS
python3 tests/rewrite_eval.py    # fidelity contracts must PASS
python3 scripts/flag_slop.py --selftest
```

Open a PR. If you added a clean sample that the detector wrongly flags, that's a
detector bug — either tighten the rule in `flag_slop.py` or, if the hit is a
legitimate low-weight candidate, add it to `allow` and say why in `note`.
