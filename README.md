# harness-humanizer

A portable [Claude Code](https://claude.com/claude-code) skill that turns AI-slop
prose into writing that survives a hostile editor's red pen — **without** swapping
one kind of slop for another.

It detects the tells of machine-flavored writing (empty hedging, listicle stems,
smooth transitions that hide the absence of a claim, generic filler), rewrites the
fixable parts toward a real point of view, self-scores against an embedded rubric,
and iterates to a bar. It **reports rather than overwrites**, and it **flags hollow
spans instead of inventing claims** to fill them.

## What makes it different

Most "humanizer" tools trade AI-slop for a louder slop — forced hot takes,
em-dash theatrics, fake first-person, "let's be honest…" mannerisms. This skill
treats that as a failure, not a fix. Two hard rules:

1. **Fidelity over flair** — preserve the original meaning and claims exactly;
   only subtract hedging and sharpen what's already there.
2. **Flag hollow spans, don't fabricate** — prose that's weak because it has no
   point to make can't be reworded into having one. Those get flagged, not faked.

## The loop

1. **Pre-flag** — a deterministic regex pass (`scripts/flag_slop.py`) cheaply
   surfaces obvious slop as *candidates*.
2. **Judge** — score each paragraph against the embedded humanness rubric
   (`strong | moderate | weak | fail`).
3. **Triage** — below-strong paragraphs are *rewordable* (real claim, buried) or
   *hollow* (no claim) — the central judgment call.
4. **Rewrite** the rewordable ones under strict fidelity guardrails.
5. **Self-score & iterate** — bar = strong, cap = 3 passes; keep the best and flag
   anything that can't reach the bar.
6. **Report** — humanized text + a per-paragraph change log + flags. The human
   decides what to accept.

Properties: **fail-honest** (hollow/capped spans always surfaced), **idempotent**
(already-strong prose returned unchanged), **non-destructive** (report, not
in-place edit).

## Install

Copy the skill into your Claude Code skills directory:

```bash
git clone https://github.com/isatimur/harness-humanizer-skill.git
cp -R harness-humanizer-skill ~/.claude/skills/harness-humanizer
# (omit .git/README/LICENSE if you prefer: just SKILL.md, references/, scripts/)
```

Then invoke it on any prose with prompts like *"humanize this"*, *"de-slop this"*,
*"make this sound less like AI"*, or *"this reads like ChatGPT"*.

## Layout

```
SKILL.md                 # invocation surface: triggers + the loop
references/
  rubric.md              # the 4 bands, slop indicators, the two tests, triage rule
  guardrails.md          # fidelity rules + over-correction anti-pattern catalogue
  examples.md            # before→after pairs; flag-don't-fabricate; PASS/FAIL cases
scripts/
  flag_slop.py           # stdlib-only regex pre-pass → JSON candidates; --selftest
```

Verify the script with `python3 scripts/flag_slop.py --selftest`.

## Origin

The rubric is adapted from the **humanness** judge in
[book-mash](https://github.com/isatimur), the multi-judge quality engine behind
[*From Copilot to Colleague*](https://fromcopilottocolleague.com/). This skill is
the inverse of that judge: where the judge *measures* slop, this *removes* it.

## License

MIT © Timur Isachenko
