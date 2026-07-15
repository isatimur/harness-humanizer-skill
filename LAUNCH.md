# Launch runbook

Sequenced plan + ready-to-post copy for each channel. The angle that separates this
from every other "humanizer": **it won't trade AI-slop for louder slop, and it passes
its own detector.** Post when ready; nothing here auto-publishes.

Links: site https://de-slop-ai.vercel.app/ · repo
https://github.com/isatimur/de-slop · scorer
https://de-slop-ai.vercel.app/#tool

---

## The sequence (order matters)

A launch is an *amplifier*. Amplifying an empty repo wastes the spike — a visitor
who lands on 3 stars and no listings bounces. So the discovery + proof layer goes
**first**, the loud channels **second**.

**Phase 1 — Seed (do before any launch post)**
- Work [`SUBMISSIONS.md`](SUBMISSIONS.md) top-down: awesome-lists & skill registries
  first (permanent discovery + backlinks), directories second.
- Get the first ~15–25 stars from your own network so the repo doesn't read as cold.
- Confirm the site is live: scorer works, all four pages 200, `og-image.png` unfurls.
- Build the **proof artifact** (below). It's the single best comment in every thread.

**Phase 2 — Launch days (don't stack them on one day)**
| Day | Channel | Best window | Notes |
|---|---|---|---|
| Day 1 (Tue–Thu) | **Show HN** | 8–10am ET | Title below. Be at your desk for 3h to answer. |
| Day 1 (staggered) | **Reddit** | after HN settles | One sub at a time, tailored — never cross-post identical text. |
| Day 1–2 | **X / LinkedIn** | mid-morning | The thread below; the card unfurls, don't attach an image. |
| Day 3 (own day) | **Product Hunt** | 12:01am PT | Needs its own day + a few hunters lined up. |

**Phase 3 — Compound (the week after)**
- Reply to every comment; turn each "it got X wrong" into a `*.jsonl` corpus sample
  and say so in-thread (the contribution funnel is itself a hook).
- Repurpose the best before→after pairs into standalone social posts.

## The proof artifact (build once, paste everywhere)

The most persuasive thing you can show is the tool judging *itself*:

```bash
uvx --from git+https://github.com/isatimur/de-slop \
  de-slop README.md --score
```

Screenshot the run showing the README/SKILL/rubric scoring `strong` under the
project's own detector. Skeptics trust "it passes its own bar" far more than any
claim. Lead comments with it. The result is pre-captured in [`PROOF.md`](PROOF.md)
(SKILL.md + guardrails.md score 100/100; README + rubric score 97 — all `strong`).

## Pre-flight checklist

- [ ] Phase-1 directory/awesome-list submissions started (see `SUBMISSIONS.md`)
- [ ] Repo has a non-trivial star count
- [ ] Site live: scorer, `/ai-slop`, `/humanize-ai-text`, `/ai-slop-vs-over-correction` all 200
- [ ] `og-image.png` unfurls on X/LinkedIn/Slack (test with a private post)
- [ ] Proof-artifact screenshot ready
- [ ] 3 hours blocked to respond on launch day

---

## Hacker News (Show HN)

**Title:** Show HN: An AI de-slopper that won't fake a voice (and passes its own detector)

**Body:**
Most "humanizers" swap AI-slop for louder slop — forced hot takes, em-dash
theatrics, fake "let's be honest." I treated that as a failure mode, not a fix.

de-slop detects machine-writing tells (empty hedging, listicle stems,
manufactured stakes), rewrites the fixable parts toward a real point of view under
strict fidelity, and — the part I care about — **flags hollow paragraphs instead
of inventing a claim to fill them.** A paragraph with no point can't be reworded
into having one.

The detector is zero-dependency Python (stdlib only, runs on 3.9–3.13 with no pip
install) and is gated on its own labeled corpus, including an over-correction
corpus so the "louder slop" shapes get caught too. It's portable to Claude Code,
Cursor, Copilot, Codex, Gemini, Windsurf, or any chatbot — all generated from one
source. There's a free in-browser scorer.

Happy to talk about the rewordable-vs-hollow judgment call, which is the whole game.

---

## Product Hunt

**Tagline:** Remove AI slop without faking a voice — in any AI tool

**Description:**
de-slop turns machine-flavored prose into writing that survives a hostile
editor's red pen. It detects the tells, rewrites toward a real point of view, self-
scores against a rubric, and flags hollow spans instead of fabricating claims. Free,
MIT, zero-dependency, and portable to every AI tool. Includes a free in-browser slop
scorer.

**First comment:** Built this because every humanizer I tried just produced a
different, louder kind of slop. The rule here is fidelity-first: subtract hedging,
sharpen the real claim, and when there's no claim, say so — don't fake one.

---

## Reddit (r/ClaudeAI, r/cursor, r/writing, r/ChatGPT)

**Title:** I built a de-slopper that flags hollow writing instead of faking a voice

Lead with the demo, not the pitch. Show a before→after from the site, then:

> It's free/MIT, works in [tool for that sub], and the detector is open-source and
> runs with zero dependencies. There's a browser scorer if you just want to paste
> text: [scorer link]. Feedback on cases it gets wrong is the most useful thing —
> there's a one-line way to add them to the test corpus.

(Tailor the tool name per sub. Don't cross-post identical text; each sub reads as spam.)

---

## X / LinkedIn thread

1/ Every "humanize AI text" tool I tried just made a louder kind of slop: forced hot
takes, em-dash drama, fake "let's be honest." So I built one with two hard rules.

2/ Rule 1 — fidelity over flair. Preserve the claim exactly; only subtract hedging
and sharpen what's already there.

3/ Rule 2 — flag hollow spans, don't fabricate. Prose with no point can't be
reworded into having one. So it gets flagged, not faked.

4/ The detector is zero-dependency, open-source, and gated on its own corpus —
including an "over-correction" set so the louder-slop shapes get caught too. It even
passes its own detector on its own docs.

5/ Portable to Claude Code, Cursor, Copilot, Codex, Gemini, Windsurf, or any chatbot.
Free in-browser scorer + MIT. [link] (the card unfurls here ↓)

---

## Notes

- Lead every post with the **before→after** or the **two rules**, never the feature list.
- The social card (`og-image.png`) unfurls on X/LinkedIn/Slack — no need to attach an image.
- Best proof point in comments: *the tool's own README/SKILL/rubric score `strong`
  under its own detector.* Skeptics respect that more than claims.
