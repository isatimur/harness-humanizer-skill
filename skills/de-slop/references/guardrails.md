# Guardrails

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
