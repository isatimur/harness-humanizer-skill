# Humanness Rubric

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
