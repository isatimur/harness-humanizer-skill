# Contributing

Thanks for helping sharpen the skill. The bar is simple: keep it **zero-dependency**,
keep the **false-positive rate near zero**, and grow the labeled corpus with real
prose the skill got wrong.

## The one rule that never bends

`scripts/flag_slop.py` imports **only the Python standard library**. No `pip
install`, ever — that portability is the whole point. CI enforces it
(`tests/check_no_deps.py`), so a stray third-party import fails the build.

## Run the suite before you push

```bash
python3 scripts/flag_slop.py --selftest   # detector smoke test
python3 tests/eval.py                      # recall / clean-specificity / over-correction gates
python3 tests/check_no_deps.py             # stdlib-only guard
python3 tests/check_js_parity.py           # docs/slop.js mirrors the Python rule set
python3 scripts/build_adapters.py --check  # adapters are in sync with SKILL.md
```

All five must pass. The matrix (Python 3.9–3.13) runs the same checks on every PR.

## The highest-value contribution: a labeled sample

Found prose the skill mishandled? Add the one line that proves it. This is the
project's growth metric — see `tests/fixtures/README.md` for the full funnel.

- **It stayed silent on real slop** → add a line to `tests/corpus/slop.jsonl`.
- **It fired on clean writing** (a false positive) → add it to
  `tests/corpus/clean.jsonl` with `expect: []`.
- **Edgy "humanized" slop slipped through** (hot takes, em-dash theatrics,
  fake candor) → add it to `tests/corpus/overcorrection.jsonl`. Catching
  over-correction is the thesis, so this gate sits at 1.0 recall.

Schema: `{id, text, expect:[types], band, source, note}`. Set `source:
"real-world"` when it came from actual AI output — those are the samples that
matter most.

## Adding or changing a detector rule

1. Edit `scripts/flag_slop.py` (the rule + its weight in `_WEIGHTS`).
2. Anchor it to an idiom, not a bare word. A rule that fires on "leverage" in
   honest engineering prose is a regression, not a feature — see the
   sentence-aware `empower` split in `references/slop-catalogue.md` for the pattern.
3. Add at least one slop sample **and** one clean sample that exercises a
   legitimate use of the same words.
4. Mirror the rule in `docs/slop.js` (parity gate) and document it in
   `references/slop-catalogue.md`.
5. Run `python3 scripts/build_adapters.py` to regenerate every tool adapter.

## Editing the skill text

`SKILL.md` and `references/` are the canonical source. Everything in `adapters/`
is generated — never hand-edit it; change the source and regenerate. As a courtesy
to the tool's purpose, run your own prose through it:
`python3 scripts/flag_slop.py --score yourfile.md`.

## What lives where

- `SKILL.md`, `references/`, `scripts/` — the runtime skill.
- `adapters/` — generated, one per tool. Do not edit by hand.
- `docs/` — the website (deployed on Vercel).
- `tests/` — corpus + gates; omittable from a lean runtime install.

By contributing you agree your work is licensed under the repository's MIT license.
