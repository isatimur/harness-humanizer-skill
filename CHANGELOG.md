# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] — 2026-06-16

### Changed
- **`empower` rule is now sentence-aware.** Marketing-register buzzwords
  ("empower", "seamless", "cutting-edge", "game-changer", "synergy", …) still
  fire on their own, but ambiguous riders common in honest engineering prose
  ("leverage", "robust", "unlock", "harness", "streamline", "elevate") fire
  **only when a marketing word shares the sentence**. So "we leverage connection
  pooling" and "robust error handling" stay silent, while "our seamless platform
  empowers teams to leverage cutting-edge tooling" still flags the whole cluster.
  Removes the last class of false positives on clean technical prose.

## [0.2.0] — 2026-06-15

The "prove it works" release. The skill is now measurable, harder to fool, and
backed by CI — while staying zero-dependency (stdlib only, copy-and-it-just-works).

### Added
- **Eval harness** (`tests/`) — a labeled JSONL corpus
  (`tests/corpus/{slop,clean,overcorrection}.jsonl`) and a deterministic runner
  (`tests/eval.py`) that gate the detector on recall, clean specificity,
  idempotence, and — the project thesis — **over-correction recall**: edgy-slop
  (performed candor, em-dash theatrics) must be caught too, not just timid
  AI-slop. Thresholds in `tests/thresholds.json`, set empirically.
- **Per-paragraph severity scoring** — `score()` / `flag_slop.py --score` emit a
  `slop_band` (`strong|moderate|weak|fail`) aligned to the rubric cutoffs.
  Explicitly labeled "surface tells only": a clean-scoring paragraph can still be
  hollow. Never a humanness judge.
- **New detector rule types**: `weaselquant`, `negparallel`, `delve`,
  `conclusion`, `empower`, `triadic`, `calltoaction` — the classic LLM tells.
- **`references/slop-catalogue.md`** — the full taxonomy mapping each tell to its
  detector type (or "model-judgment-only"), with the detector's boundary documented.
- **CI** (`.github/workflows/ci.yml`) — runs the self-test + eval across Python
  3.9–3.13 with **no pip install** (the portability proof), plus a
  zero-dependency import guard (`tests/check_no_deps.py`).
- **Plugin manifest** (`.claude-plugin/plugin.json`) and this changelog.

### Changed
- **Intensifier rule split** into `intensifier_filler` (flavor adverbs —
  genuinely/truly/honestly, a real over-correction tell, weight 10) and
  `intensifier_degree` (very/really + adjective, often legitimate, weight 6).
  Fixes false positives like "very old browsers" and "very Tuesday" by
  downweighting rather than suppressing — only *clusters* now move the band.
- `examples.md` extended with per-rule before→after pairs and more
  over-correction PASS/FAIL cases; every example is coupled to a corpus line.

### Preserved
- `flag()` and the default `flag_slop.py FILE` output keep the v0.1.0
  `{line, type, pattern, span}` shape — SKILL.md's step-1 contract is unchanged.

## [0.1.0]

- Initial release: the SKILL.md loop, `references/{rubric,guardrails,examples}.md`,
  and the stdlib-only `flag_slop.py` detector with `--selftest`.
