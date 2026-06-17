# harness-humanizer: Portability + Adoption Design

**Date:** 2026-06-17
**Status:** Approved (scope: build everything buildable now; launch + BYOK runtime specced for later)
**Goal:** Adoption / reach. Maximize installs, stars, and usage across every AI tool. Stays 100% free / MIT.

## Problem

`harness-humanizer` is a Claude Code skill. Its value (de-slop AI prose, fidelity-first)
is tool-agnostic, but its packaging is Claude-Code-only. To reach "everyone and every AI
tool" it needs (a) to be installable in every major AI harness from one maintained source,
(b) a frictionless install-free surface for non-CLI users, and (c) a discovery engine
(website + SEO + a shareable free tool) so people find it at all.

## Core principle: one source, many renders

`SKILL.md` + `references/*` remain the **single canonical source**. A stdlib-only build
script renders every target. Edit the rubric once → regenerate all. CI fails if any
generated adapter drifts from source. This preserves the project's stdlib-only,
zero-dependency identity.

## Phase 1 — Portability (build now)

### 1.1 Generator
- `scripts/build_adapters.py` — stdlib-only. Reads `SKILL.md` + `references/*`, renders
  each target from a declarative manifest. Flags: `--check` (CI: diff committed vs.
  regenerated, exit 1 on drift), `--write` (regenerate in place).
- Manifest entry = `{id, output_path, format, header}`. `format` ∈
  `{mdc, markdown, agents, prompt}`. Adding a harness = one manifest entry.

### 1.2 Targets (committed under `adapters/`, except where a tool dictates a path)

| Tool | Output path | Format notes |
|---|---|---|
| Claude Code | `SKILL.md` (source) | canonical, not generated |
| Cursor | `adapters/cursor/harness-humanizer.mdc` | MDC frontmatter: `description`, `globs`, `alwaysApply: false` |
| GitHub Copilot | `adapters/copilot/harness-humanizer.instructions.md` | `applyTo` frontmatter + body |
| Codex / Amp / Jules / generic | `adapters/AGENTS.md` | universal markdown, the cross-tool standard |
| Gemini CLI | `adapters/gemini/GEMINI.md` | markdown |
| Windsurf | `adapters/windsurf/harness-humanizer.md` | markdown rule |
| Paste-anywhere | `adapters/PROMPT.md` | fully self-contained: skill body + rubric + guardrails + condensed examples inlined. Works in any chatbot, zero install. |

**Pi / Hermes / OpenCLAW and other niche harnesses:** covered today by the universal
`AGENTS.md` and `PROMPT.md` targets (most newer agents read `AGENTS.md` or accept a pasted
prompt). When an exact rules-file convention is known, add a precise manifest entry. Do not
fabricate config-file specs.

### 1.3 Package the deterministic flagger
- `pyproject.toml` (stdlib-only, no runtime deps) exposing console script `humanizer-flag`
  → `scripts/flag_slop.py`. Enables `pipx install harness-humanizer` / `pip install`.
- Keep the script runnable directly (back-compat).

### 1.4 CI
- Extend `.github/workflows/ci.yml`: run `build_adapters.py --check` and a JS-parity check
  (1.6) so adapters + the in-browser scorer can never silently drift from source.

## Phase 2 — Website + SEO (build now)

### 1.5 "Install for your tool" section on `docs/index.html`
- Tabs/accordion per harness with copy-paste blocks (Cursor, Copilot, Codex/AGENTS.md,
  Gemini, Windsurf, Claude Code) + the paste-anywhere prompt + the one-line pip install.
- Each block links to the matching file in `adapters/`.

### 1.6 Client-side "AI Slop Score" tool (free, no backend, no API key)
- Port the `flag_slop.py` regex rules + scoring to `docs/slop.js`. Paste text → live slop
  score + highlighted flagged spans + per-pattern breakdown. Runs entirely in-browser.
- **Parity:** rules live in one JSON-ish table mirrored from Python. A test
  (`tests/check_js_parity.py`) asserts the JS rule set matches `flag_slop.py` so they don't
  diverge. This is the shareable, frictionless demo artifact.
- Framed honestly per the skill's own ethos: "surface-tell meter, not a humanness score."

### 1.7 SEO foundation
- Real canonical URL, refined `<title>`/meta/OG/Twitter cards.
- JSON-LD: `SoftwareApplication` + `FAQPage`.
- `docs/sitemap.xml`, `docs/robots.txt`.
- Glossary page `docs/ai-slop.html` — "What is AI slop? The full taxonomy," built from
  `references/slop-catalogue.md`. Targets "AI slop", "humanize AI text", "make ChatGPT
  sound human." Internal-links to the tool and install section.
- Run `seo-audit` / `schema-markup` / `ai-seo` skills for execution + validation.

## Phase 3 — Deferred (specced, not built this pass)

### Launch assets (`docs/superpowers/specs/launch-plan.md`)
- Show HN + r/ClaudeAI + r/cursor posts (angle: "one skill, every AI tool").
- Directory submission list (AI-tool directories, skill registries).
- awesome-list PR targets (awesome-claude-code, awesome-cursor, awesome-copilot).

### BYOK rewrite tool (phase 2 runtime)
- Bring-your-own-key web tool that runs the full rewrite loop client-side against the
  user's own API key; matching CLI subcommand. No server, no stored keys.

## Competitive: stop-slop (11.1k⭐, MIT, Hardik Pandya) — "multiply the effect"

stop-slop is the category leader: large banned-word/structure lists + a 5-dimension score
(directness, rhythm, trust, authenticity, density; <35/50 → revise) + hard rules (no
em-dashes, no adverbs, active voice, second-person, remove quotable constructions). It is
prescriptive and Claude-oriented.

Our differentiation is substantive, not manufactured: stop-slop's prescriptions are the
exact over-correction `guardrails.md` already guards against (mechanical "be punchy / drop
em-dashes / go second-person" produces edgy-LinkedIn slop). We preserve meaning, flag
hollow spans instead of faking them, ship a runnable detector + self-scoring loop, and run
in every tool.

Moves (build now unless noted):
1. **Harvest the corpus.** Fold stop-slop's MIT phrase/structure lists into `flag_slop.py`
   rules + `slop-catalogue.md`, with attribution. Their static markdown becomes a runnable,
   scoreable, portable detector. New corpus samples added to `tests/`.
2. **Interop profile.** `flag_slop.py --profile stop-slop` (and a PROMPT variant) applies
   their aggressive list *with* our fidelity guardrails as the safety net.
3. **Comparison page (deferred to launch assets).** `docs/vs-stop-slop.html` — honest,
   captures their search traffic, says when to use each. Built via `competitor-alternatives`.
4. **Distribution.** Match their copy-paste simplicity; exceed their reach via adapters +
   paste prompt + free web tool.

Integrity: attribute stop-slop, never disparage. The difference is a real design bet
(rule-based subtraction vs. fidelity-first judgment), framed as such.

## Out of scope
- Paid acquisition, hosted/paid API, accounts, analytics backends.
- Refactoring unrelated to the above.

## Success signals
- Portability: adapters generate + `--check` is green in CI; a user can install in any
  listed tool by copy-paste.
- Adoption: slop-score tool is shareable and works offline; site ranks for "AI slop";
  GitHub stars / directory listings climb post-launch.

## File manifest (new/changed)
- New: `scripts/build_adapters.py`, `adapters/**`, `pyproject.toml`,
  `tests/check_js_parity.py`, `docs/slop.js`, `docs/ai-slop.html`, `docs/sitemap.xml`,
  `docs/robots.txt`, `docs/superpowers/specs/launch-plan.md`.
- Changed: `docs/index.html` (install section, tool, SEO/schema), `.github/workflows/ci.yml`,
  `README.md` (tool matrix + website tool link), `CHANGELOG.md`, `vercel.json` (commit it).
