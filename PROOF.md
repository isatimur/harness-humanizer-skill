# Proof: it passes its own detector

The fastest way to distrust a "humanizer" is to read its own marketing and find slop.
So here is de-slop's own prose, scored by de-slop's own detector.

Reproduce it yourself — zero dependencies, any Python 3.9+:

```bash
git clone https://github.com/isatimur/de-slop && cd de-slop
python3 scripts/flag_slop.py --score README.md
python3 scripts/flag_slop.py --score SKILL.md
```

## Result (run on this repo)

| Document | Band | Score | Detector hits |
|---|---|---|---|
| `SKILL.md` | **strong** | 100 / 100 | 0 |
| `references/guardrails.md` | **strong** | 100 / 100 | 0 |
| `references/rubric.md` | **strong** | 97 / 100 | 1 |
| `README.md` | **strong** | 97 / 100 | 3 |

Every core document lands in the top band.

## The honest footnotes (we surface these, we don't hide them)

The detector measures *surface slop tells*, so the handful of hits are worth naming
rather than scrubbing — that is the whole ethic of the project:

- The README's lone non-`strong` paragraph is the one that **quotes** slop mannerisms
  ("let's be honest…", "it's worth noting that…") as the *negative examples* it warns
  against. The detector flags the words; in context they are the exhibit, not the crime.
- Two README hits are the degree word "rather than" — a phrase the detector marks as
  "often legit." It is legit here.

A `strong` score is not a claim that the writing is *good* — only that it carries no
surface slop. The detector says so itself on every run: *"slop_band measures surface
slop tells only, not humanness; a clean-scoring paragraph can still be hollow."* The
point stands anyway: a de-slopper whose own docs survive its own pass has earned the
benefit of the doubt that most "humanizers" have not.
