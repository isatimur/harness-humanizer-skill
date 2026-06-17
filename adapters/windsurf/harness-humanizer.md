<!-- GENERATED from SKILL.md + references/ by scripts/build_adapters.py. Do not edit by hand; edit the source and regenerate. -->

> **Install:** place in `.windsurf/rules/` in your project.
>
> Use when prose reads like AI — to remove "AI slop" (empty hedging, listicle stems, smooth transitions that hide the absence of a claim, generic filler) and rewrite it into writing with a real point of view. Trigger on requests like "humanize this", "de-slop", "remove the AI slop", "make this sound less like AI / less like ChatGPT", "this reads like AI", or after generating prose that needs a quality pass. Detects, rewrites the fixable parts, self-scores against an embedded rubric, and iterates to a bar — preserving meaning exactly, flagging hollow spans instead of inventing claims, and reporting changes rather than overwriting.

# Harness Humanizer

Turn AI-slop prose into writing that survives a hostile editor's red pen —
without swapping one kind of slop for another.

## Two hard rules (read first)

1. **Fidelity over flair.** Preserve the original meaning and claims *exactly*.
   Only subtract hedging/filler and sharpen what is already there. Never inject
   stance, edginess, em-dash theatrics, or first-person personality the content
   did not earn. **Swapping AI-slop for edgy-slop is a failure, not a fix.**
2. **Flag hollow spans, don't fabricate.** Some prose is weak because it has no
   point to make — rewording cannot save it. Flag those. Do **not** invent a hot
   take to make them sound sharp.

## The loop

**0. Scope.** Work paragraph by paragraph. Skip code blocks, blockquotes,
headings, and genuine lists.

**1. Pre-flag.** Run the cheap deterministic pass to narrow attention:

```
python3 scripts/flag_slop.py <file>     # or: cat text | python3 scripts/flag_slop.py
```

It returns JSON spans (hedge stems, listicle openers, em-dash density,
"in today's…", filler intensifiers, etc.). These are **candidates, not
verdicts** — you still judge every paragraph.

Optionally, `python3 scripts/flag_slop.py --score <file>` returns a per-paragraph
`slop_band`. Treat it as a **surface-tell meter, not a humanness score**: it
measures how many slop patterns appear, *not* whether a real claim is present. A
paragraph with zero tells can still be hollow and `fail` the rubric — so a high
`slop_band` never excuses you from step 2. See `references/slop-catalogue.md` for
which tells the detector can and cannot see.

**2. Judge.** Score each paragraph against `references/rubric.md` →
`strong | moderate | weak | fail`, with a one-line reason. The bar is the
hostile-editor test: *would this survive a red pen? does removing it lose
anything?*

**3. Triage** each paragraph below **strong**:
- **Rewordable** — there's a real claim buried under hedging/filler → rewrite.
- **Hollow** — weak because there's no actual point → **flag, don't fabricate**.

**4. Rewrite** the rewordable ones, applying `references/guardrails.md`. Subtract
the hedging, sharpen the existing claim, keep the meaning identical.

**5. Self-score** the rewrite against the rubric again.
- Reached **strong** → lock it in.
- Still below → iterate (back to step 4). **Maximum 3 passes total.**
- After 3 passes still not strong → keep the best version and **flag it**
  ("couldn't reach strong — may need a real claim, not better words").

**6. Report — do not overwrite.** Return three things:
- **Humanized text** — rewrites applied; hollow spans left intact.
- **Change log** — per paragraph: `before-band → after-band` and what changed.
- **Flags** — hollow spans + any span that hit the 3-pass cap.

The human or calling agent decides what to accept.

## Properties this loop must preserve

- **Fail-honest:** hollow and capped spans are always surfaced, never quietly
  "polished."
- **Idempotent:** prose that already scores strong is returned unchanged.
- **Non-destructive:** you produce a report + change log, not an in-place edit.

---

## Humanness rubric (inlined)

Score a single paragraph on **humanness** — does this sound like a thinking
author with a point of view, or is it generic AI-flavored prose that could appear
in any blog post?

## Bands (0–100)

- **strong (80–100):** specific, has a point of view, survives a hostile editor's
  red pen. A real claim someone could disagree with. Removing it would lose
  something.
- **moderate (50–79):** readable but generic in spots. A real point is present
  but softened by hedging or filler.
- **weak (20–49):** pattern-matchable AI prose. Removing it loses nothing. The
  sentence is shaped like an argument but isn't making one.
- **fail (0–19):** pure scaffolding language — listicle stems, empty hedging,
  transitions with no content between them.

## Slop indicators (lower the score)

- **Empty hedging:** "it's worth noting", "it's important to remember", "that
  said", "of course", "arguably" used to avoid committing.
- **Listicle stems with no point of view:** "There are several key factors…",
  "Here are a few things to consider…" followed by the obvious.
- **Smooth transitions that hide the absence of a claim:** "Moreover", "In
  addition", "Furthermore" gluing together sentences that don't actually advance
  an argument.
- **Generic filler:** intensifiers ("really", "very", "truly", "incredibly"),
  manufactured stakes ("in today's fast-paced world"), throat-clearing openers.

For the full taxonomy of tells — each one, why it reads as AI, and which detector
type catches it (or why none can) — see `slop-catalogue.md`. Note that the
detector surfaces *candidates* by surface pattern; this rubric assigns the band.
A clean-looking paragraph can still be **weak** or **fail** if it makes no claim
(hollowness is invisible to any regex — only the removal test below catches it).

## The two tests

1. **Hostile-editor test:** would a sharp editor leave this sentence on the page,
   or red-pen it as padding?
2. **Removal test:** if you deleted this sentence, would the reader lose
   anything? If nothing is lost, the sentence is slop regardless of how polished
   it sounds.

## The substance lens (specificity · restraint · voice)

Surface tells are only half the judgment. A paragraph can be mechanically clean —
zero hedging, no buzzwords — and still be slop because it has nothing to say. When
the detector is quiet, judge substance on three axes before passing it:

- **Specificity** — does it commit to a concrete claim (a name, number, mechanism,
  consequence), or only gesture at one? "Significant improvement" fails;
  "latency dropped from 340ms to 90ms" passes.
- **Restraint** — is the emphasis earned, or manufactured? Forced contrast, dramatic
  fragmentation, and hot takes are *negative* substance — louder, not stronger.
- **Voice** — is there a thinking author reacting to the facts, or a neutral
  narrator restating them? Voice is not personality theatrics; it is having a point.

Mechanics-clean ≠ good. This lens is what separates *moderate* from *strong*, and
it is the human/model side of the loop the regex cannot reach. (The three-axis
"substance" framing is shared with `stop-slop` derivatives like `tagore`; here it
guides band judgment rather than a numeric gate.)

## Triage rule (for anything below strong)

- **REWORDABLE** — the paragraph *has a real claim* that's buried under hedging or
  filler. The fix is subtraction + sharpening. → rewrite it.
- **HOLLOW** — the paragraph is weak because it *has no actual point to make*.
  Nothing is lost if removed. Rewording cannot fix an absent claim. → flag it;
  do not invent a claim to fill the hole.

The single most important judgment call this skill makes is rewordable vs.
hollow. When unsure, apply the removal test: if deleting the paragraph entirely
would cost the reader nothing, it is hollow.

---

## Guardrails (inlined)

Apply these to every rewrite. The goal is to remove slop, not to perform
"humanness." A rewrite that violates these is a failure even if it scores well.

## Fidelity (the prime rule)

- Preserve the original **meaning and claims exactly**. The rewrite says the same
  thing the author meant — only clearer and without padding.
- You may **subtract** (hedging, filler, dead transitions) and **sharpen** (make
  an existing claim concrete, surface the point that was buried).
- You may **not add** a claim, opinion, statistic, example, or stance that was not
  already in the source. If the point isn't there, that's a HOLLOW span — flag it,
  don't fill it.

## Over-correction anti-patterns (never inject these)

The classic failure of "humanizer" tools is trading AI-slop for a louder slop.
Do not introduce any of:

- **Forced contrarianism / hot takes** — "Everyone says X, but they're wrong."
  (unless the source actually argued this)
- **Em-dash theatrics** — dramatic dashes manufacturing emphasis the content
  doesn't earn.
- **Fake first person** — "I've seen this a hundred times", "In my experience"
  inserted into prose that had no author-presence.
- **"Let's be honest / let's be real / here's the thing"** — performed candor.
- **Manufactured stakes** — "In a world where…", "Now more than ever", "The
  stakes have never been higher."
- **Rhetorical-question openers** — "What if I told you…?", "Ever wondered why…?"
- **Intensifier padding** — "genuinely", "truly", "honestly", "literally" as
  flavor.

These are slop in a different costume. The bar is a *thinking* author, not a
*loud* one.

## Idempotence

- If a paragraph already scores **strong**, return it unchanged. The skill must do
  nothing to good prose.
- Running the skill twice on the same text must produce the same result the second
  time as the first (the first run's output is already at the bar).

## When in doubt

Prefer the smaller edit. The best de-slop is usually deletion of the hedge plus
nothing else. If you can't improve a sentence without inventing content, you've
found a hollow span — flag it and move on.

---

*Optional tooling — a zero-dependency deterministic pre-flagger (`flag_slop.py`), the full slop catalogue, and the test corpus live in the repo: https://github.com/isatimur/harness-humanizer-skill*
