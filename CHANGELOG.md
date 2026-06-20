# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Social preview card** — a 1200×630 `og-image.png` (manuscript/red-pen
  aesthetic) wired into `og:image`/`twitter:image` on both pages, so link unfurls
  on X/LinkedIn/Slack/Discord render properly. Source is `docs/og-image.svg`.
- **`CONTRIBUTING.md`** — the contribution funnel (labeled samples), rule-authoring
  checklist, and the five-command verification suite, surfaced from the README.

### Changed
- Canonical home consolidated on Vercel: GitHub Pages retired, repo homepage and
  README links point at `harness-humanizer-skill.vercel.app` (clean `/ai-slop` URL).

## [0.3.0] — 2026-06-18

The "everyone, every tool" release. Same fidelity-first skill — now portable to
every AI harness, installable as a CLI, scoreable in the browser, and with a
detector that folds in (and out-engineers) the wider de-slop ecosystem.

### Added
- **Portable adapters** — one stdlib-only generator (`scripts/build_adapters.py`)
  renders `SKILL.md` + `references/` into every tool's native format: Cursor
  (`.mdc`), GitHub Copilot (`.instructions.md`), Codex/Amp/Jules (`AGENTS.md`),
  Gemini (`GEMINI.md`), Windsurf, and a self-contained **paste-anywhere
  `PROMPT.md`** for any chatbot. CI gates drift with `--check`.
- **CLI packaging** (`pyproject.toml`) — `uv tool install` / `pipx install`
  exposes a `humanizer-flag` command. Still zero runtime dependencies.
- **Free in-browser Slop Score tool** — `docs/slop.js`, a parity-gated JS port of
  the detector that runs entirely client-side on the website. New
  `tests/check_js_parity.py` keeps it in lockstep with `flag_slop.py`.
- **SEO + glossary** — `docs/ai-slop.html` ("What is AI slop?"), JSON-LD
  (`SoftwareApplication` + `FAQPage`), `sitemap.xml`, `robots.txt`.
- **12 new detector tells**, harvested from
  [stop-slop](https://github.com/hardikpandya/stop-slop) (MIT) and its community
  PRs (#4/#5/#8): `throatclear`, `emphasis_crutch`, `metacommentary`,
  `binarycontrast`, `neglisting`, `bizjargon`, `assistantvoice`, `transformchain`,
  `correctivereveal`, `forcedcohesion`, `copula`, `hedgestack`. Rendered as
  weighted, idiom-anchored rules (not a blunt block-list) so honest technical
  prose stays silent. Contrarian/profundity shapes added to the over-correction
  corpus. Eval still green: recall 1.0, clean-specificity 1.0, over-correction
  recall 1.0, **0 false positives**.
- **`--profile stop-slop`** — opt-in aggressive rules (all adverbs, Wh- openers,
  any em-dash) for fans of stop-slop's stricter style, behind our non-destructive
  report + over-correction guardrails.

### Changed
- **Rubric gains a substance lens** (specificity · restraint · voice) for the
  hollow-vs-rewordable call — the model-judgment axis the regex can't reach.
  Cross-pollinated from stop-slop derivatives (tagore), adapted to guide band
  judgment rather than a numeric gate.
- Website rebuilt: live scorer, an "Install for your tool" matrix (uv-first), and
  full SEO. Now hosted on Vercel.

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
