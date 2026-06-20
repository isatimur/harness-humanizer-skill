# Launch copy

Ready-to-post copy for each channel. The angle that separates this from every
other "humanizer": **it won't trade AI-slop for louder slop, and it passes its own
detector.** Post when ready; nothing here auto-publishes.

Links: site https://harness-humanizer-skill.vercel.app/ · repo
https://github.com/isatimur/harness-humanizer-skill · scorer
https://harness-humanizer-skill.vercel.app/#tool

---

## Hacker News (Show HN)

**Title:** Show HN: An AI de-slopper that won't fake a voice (and passes its own detector)

**Body:**
Most "humanizers" swap AI-slop for louder slop — forced hot takes, em-dash
theatrics, fake "let's be honest." I treated that as a failure mode, not a fix.

harness-humanizer detects machine-writing tells (empty hedging, listicle stems,
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
harness-humanizer turns machine-flavored prose into writing that survives a hostile
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
