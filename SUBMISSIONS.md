# Submission kit — get to #1 in AI-slop

The goal: become the **most-adopted AI de-slopper / writing skill** in the agent-skills
ecosystem. "#1 skill" is won on **discovery surfaces** (curated lists, skill registries,
AI directories) plus **social proof** (stars, reviews, citations) — not on one launch day.

Work this top-down. Tier 1 is where skill-seekers actually look; do it first. Everything
below is free unless marked **`$`**. Lead every listing with the one-line differentiator:

> **The AI de-slopper that won't fake a voice — and passes its own detector.**

**Positioning by surface** (don't paste identical copy everywhere — engines down-weight
duplicates): awesome-lists → *technical substance*; AI directories → *AI-first, free*;
communities → *before→after demo first, pitch second*.

**Canonical links:** repo `https://github.com/isatimur/de-slop` · site
`https://de-slop-ai.vercel.app/` · scorer `…/#tool`

---

## Readiness (honest gaps before Tier-1 push)

| Asset | State |
|---|---|
| Public, no wall | ✅ |
| License + repo + site live | ✅ |
| GEO pages (single H1, FAQ schema, llms.txt) | ✅ (just shipped) |
| Pricing page | ✅ n/a — free/MIT (state it explicitly in listings) |
| Screenshots / 60–90s demo video | ⬜ **build before Product Hunt** (scorer screen-capture is enough) |
| Star base (~15–25 from network) | ⬜ seed before launch posts |
| PyPI listing | ⬜ blocked on pending-publisher (separate task) |

---

## Tier 1 — Agent-skill discovery surfaces (DO FIRST, highest value)

These are where people browse for skills. Mostly dofollow GitHub backlinks + direct in-market discovery.

| Target | Mechanism | Value | Notes |
|---|---|---|---|
| **hesreallyhim/awesome-claude-code** | ⚠️ Recommend via its automated flow — **read its `CONTRIBUTING.md`**, do **not** open a direct PR (only the maintainer's bot opens PRs) | ★★★★★ | The canonical Claude Code list. Skill category exists. |
| **VoltAgent/awesome-agent-skills** | PR add (1000+ skills; cross-tool: Claude/Codex/Gemini/Cursor) | ★★★★★ | Biggest cross-agent list — perfect fit (we're cross-tool). |
| **ComposioHQ/awesome-claude-skills** | PR add | ★★★★☆ | Active, skill-specific. |
| **travisvn/awesome-claude-skills** | PR add | ★★★★☆ | Claude-Code-focused skills. |
| **tech-leads-club/agent-skills** | PR add (validated/"secure" registry — may require review) | ★★★★☆ | Quality-gated → strong trust signal if accepted. |
| **awesomeclaude.ai** & **awesome-skills.com** | Web submit form | ★★★☆☆ | Web directories that mirror the lists; extra discovery. |
| `gh skill` ecosystem (GitHub Agent Skills) | Ensure repo is `gh skill`-installable + tagged | ★★★★☆ | GitHub CLI can install skills directly (Apr-2026 changelog). Make sure SKILL.md metadata is discoverable. |
| **vercel-labs/skills** (decentralized installer CLI, 70+ agents) | No submission — already installable: `npx skills add isatimur/de-slop` (root `SKILL.md` conforms). **Advertise the command**; consider a PR to any examples/showcase list in the repo. | ★★★★★ | Distribution surface, not a list. One command installs us into Claude Code/Cursor/Cline/OpenCode/etc. Put the command everywhere. |
| **skills.sh** (registry/leaderboard for the `npx skills` ecosystem) | Indexes GitHub skills installed via `npx skills add`. Confirm we appear at `skills.sh/isatimur/de-slop`; check the docs (`/docs`, CLI/API) for any explicit publish step. **Ranking = total installs + 8-week activity** → every install/launch post compounds here. | ★★★★★ | Public leaderboard with visible install counts. The competitor `story-deslop` lives here at 6.4K installs / 3.3K★ — this is the scoreboard to climb. Drive installs via the one-command line everywhere. |

**Ready-to-paste entry (markdown list item for awesome-lists):**
```markdown
- [de-slop](https://github.com/isatimur/de-slop) — Removes "AI slop" (hedging, listicle stems, filler) without faking a voice. Subtractive method, self-scores against a rubric, flags hollow spans instead of fabricating claims. Zero-dependency, MIT, works in Claude Code / Cursor / Copilot / Codex / Gemini / Windsurf.
```
**Category to request:** `Writing` / `Content` / `Editing` skill.

---

## Tier 2 — AI tool directories (free, dofollow, AI-citation fuel)

High-DR directories that ChatGPT/Perplexity pull from for "best AI writing/humanizer tool" answers. All free; all dofollow on free tier.

| Directory | Submit | Value | Notes |
|---|---|---|---|
| **There's An AI For That (TAAFT)** | Free submit form | ★★★★★ | ~2M monthly visits, largest AI directory; 24–48h. |
| **Futurepedia** | Free submit (human review 3–7d) | ★★★★☆ | Curated → higher quality signal; dofollow. |
| **Toolify.ai** | Free submit (**2–4 wk queue**; Express `$`) | ★★★★☆ | Large; use the free queue. |
| **AlternativeTo** | Free add (community) | ★★★★★ | "X alternative" intent traffic; list us under Grammarly/AI-writing alternatives — honestly. |
| **SaaSHub** | Free submit | ★★★★☆ | Dofollow; good DR. |
| **Peerlist** | Free project post | ★★★☆☆ | Dev-leaning audience; dofollow. |
| **TheSaaSDir** | Free via badge exchange | ★★★☆☆ | Dofollow; cited by AI engines. |

**Tagline (<10 words):** `Remove AI slop without faking a voice — any AI tool`
**60-char:** `De-slop AI writing without faking a voice. Free, MIT.`
**~150-word long description:**
```
de-slop turns machine-flavored prose into writing that survives a
hostile editor's red pen — without swapping AI-slop for a louder slop. Most
"humanizers" bolt on forced hot takes, em-dash drama, and fake first-person;
this one treats that as the failure mode. It detects the real tells (empty
hedging, listicle stems, transitions that hide the absence of a claim, generic
filler), rewrites the fixable parts toward a genuine point of view under strict
fidelity, self-scores against an embedded rubric, and — the part that matters —
flags hollow paragraphs instead of inventing a claim to fill them. It reports
changes rather than overwriting, so you stay in control. Free, MIT, and
zero-dependency (stdlib-only Python 3.9–3.13), with an in-browser scorer that
runs locally. Portable to Claude Code, Cursor, GitHub Copilot, Codex, Gemini,
Windsurf, or any chatbot via a paste-anywhere prompt — all from one source.
```
**Tags:** `AI writing`, `editing`, `content`, `humanizer`, `developer tools`, `open source`, `productivity`

---

## Tier 3 — Launch events (one-shot spikes — see LAUNCH.md for timing)

| Event | When | Value | Notes |
|---|---|---|---|
| **Show HN** (Hacker News) | Tue–Thu 8–10am ET | ★★★★★ | Technical angle ready: zero-dep detector + over-correction corpus. Copy in `LAUNCH.md`. |
| **Product Hunt** | Own day, 12:01am PT | ★★★★☆ | Needs the demo video + a few hunters. Ask for *feedback*, never upvotes. |
| **Fazier** | Launch week | ★★★☆☆ | PH-style, lighter; dofollow. |
| **DevHunt** | Launch week | ★★★☆☆ | Dev-tool-specific. |
| **BetaList** | If positioned as new | ★★☆☆☆ | Optional; slower. |

---

## Tier 4 — Communities (ongoing, 90/10 rule: help 9×, promote 1×)

Genuine mentions here are GEO fuel — Claude/Perplexity index Reddit + HN heavily.

| Community | Angle | Value |
|---|---|---|
| **r/ClaudeAI** | "skill that de-slops without faking a voice" + before→after | ★★★★★ |
| **r/ChatGPT**, **r/writing**, **r/cursor** | tailored per sub; lead with the demo | ★★★★☆ |
| **dev.to / Hashnode** | technical post: "How I built a de-slopper that passes its own detector" (canonical → blog), dofollow | ★★★★☆ |
| **Indie Hackers** | build-in-public thread on launch day | ★★★☆☆ |
| **Lobsters** (if invited) | technical only | ★★★☆☆ |

> Reddit copy is in `LAUNCH.md`. One sub at a time, tailored — identical cross-posts read as spam.

---

## Tier 5 — Entity/GEO presence (feeds AI training corpora)

| Surface | Action | Value |
|---|---|---|
| **GitHub Topics** | Tag repo: `claude-skill`, `ai-writing`, `agent-skills`, `humanizer`, `llm`, `mcp` (where apt) | ★★★★☆ |
| **Wikidata / project entries** | Create a basic entry once notable | ★★★☆☆ |
| **llmrefs / GeoTracker** | Monitor "best AI humanizer" citations monthly | tracking |

---

## Tracker — tick as you go

**Tier 1 — skill surfaces**
- [ ] awesome-claude-code (via CONTRIBUTING flow — not direct PR)
- [ ] VoltAgent/awesome-agent-skills (PR)
- [ ] ComposioHQ/awesome-claude-skills (PR)
- [ ] travisvn/awesome-claude-skills (PR)
- [ ] tech-leads-club/agent-skills (PR)
- [ ] awesomeclaude.ai (form)
- [ ] awesome-skills.com (form)
- [ ] Repo `gh skill`-installable + topics tagged

**Tier 2 — AI directories**
- [ ] TAAFT  - [ ] Futurepedia  - [ ] Toolify (free queue)  - [ ] AlternativeTo  - [ ] SaaSHub  - [ ] Peerlist  - [ ] TheSaaSDir

**Tier 3 — launch**
- [ ] Show HN  - [ ] Product Hunt (after demo video)  - [ ] Fazier  - [ ] DevHunt

**Tier 4 — communities**
- [ ] r/ClaudeAI  - [ ] r/cursor  - [ ] r/writing  - [ ] dev.to post  - [ ] Indie Hackers

**Per submission:** after it goes live, confirm the backlink is dofollow:
`curl -sIL <listing-url> | grep -i rel=` (no `rel=nofollow` near your link = dofollow).

---

## Notes on honesty (non-negotiable for this project)

- Don't claim PyPI install until it's live (it isn't yet — see README).
- On AlternativeTo / comparison surfaces, describe competitors fairly — engines cross-check and de-rank lies.
- `⚠️` rows have a specific contribution mechanism — follow each repo's `CONTRIBUTING.md`; a wrong-format PR burns the first impression with that maintainer.
- URLs to specific submission forms change; the **targets** are verified real (Jun 2026), but confirm each form URL at submit time.
