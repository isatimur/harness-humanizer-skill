# de-slop — Launch & Distribution Plan

**Status:** Ready to execute (not yet run). Goal: adoption — installs, stars,
usage across every AI tool, and owning "AI slop" in search. 100% free / MIT.

Sequencing matters: ship the free tool and adapters first (done in v0.3.0), then
seed backlinks, then launch loud — each step gives the next something to point at.

## 1. Pre-launch checklist (assets that must exist)
- [x] Free in-browser Slop Score tool (frictionless, no API key)
- [x] Paste-anywhere `PROMPT.md` + per-tool adapters
- [x] "What is AI slop?" glossary page (SEO landing)
- [x] `uv tool install` / `pipx` CLI
- [ ] Publish CLI to PyPI so `uvx de-slop` / `uv tool install de-slop` work by name (currently git-only)
- [ ] OG image (1200×630) for social cards — the manuscript/red-pen motif
- [ ] 30-second screen capture of the scorer flipping fail → strong

## 2. Comparison page (capture competitor search traffic)
Build `docs/vs-stop-slop.html` with the `competitor-alternatives` skill. Honest,
respectful, decision-oriented:
- What stop-slop is great at (simple, popular, prescriptive banned-list).
- The different bet: fidelity-first, flag-don't-fabricate, runnable detector,
  every-tool portability, over-correction guardrails.
- "Use stop-slop if… / use de-slop if…" — real guidance, not a takedown.
- Note the `--profile stop-slop` interop on-ramp.
Target queries: "stop-slop alternative", "AI humanizer that preserves meaning".

## 3. Directory + backlink sweep (run via `directory-submissions`)
- AI-tool directories: There's An AI For That, Futurepedia, AI directories that
  list skills/prompts.
- Claude/Cursor ecosystem: `awesome-claude-code`, `awesome-cursor`,
  `awesome-copilot`, `awesome-ai-coding-tools` — PR the adapter + one-liner.
- AGENTS.md registries / skill marketplaces as they emerge.
- Dev backlinks: dev.to / Hashnode cross-post of the glossary.

## 4. Launch moment (after backlinks are seeded)
- **Show HN**: "Show HN: De-slop AI prose in any AI tool — without trading it for
  louder slop." Lead with the free scorer + the over-correction thesis (the
  differentiator), not the feature list.
- **r/ClaudeAI, r/cursor, r/LocalLLaMA**: angle "one skill, every AI tool";
  link the free tool first, repo second.
- **X/LinkedIn**: the fail→strong screen capture + the "louder slop is still slop"
  line. Tag the stop-slop author respectfully (we built on their corpus).
- **Product Hunt** (optional): only with the OG image + video ready.

## 5. SEO follow-through (compounding)
- Keep the glossary updated as the taxonomy grows; add FAQ entries from real
  questions.
- Consider programmatic pages per tell ("the listicle-stem tell", etc.) via
  `programmatic-seo` if the glossary gains traction.
- Internal-link the tool ↔ glossary ↔ install everywhere.

## Success signals
- Week 1: scorer shares + repo stars; HN/Reddit front-page or steady referral.
- Month 1: page ranks for "AI slop" / "humanize AI text"; ≥3 directory/awesome
  listings; first external adapters or contributions.

## Integrity guardrails for all outreach
- Never disparage stop-slop or tagore; we extend their work and credit it.
- The free tool is honestly framed: "surface tells, not a humanness judge."
- No fabricated metrics or fake reviews. Claims must be verifiable from the repo.
