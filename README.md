# harness-humanizer

**Version 0.3.0** · stdlib-only, zero-dependency · [Website + free slop scorer](https://harness-humanizer-skill.vercel.app/) · [What is AI slop?](https://harness-humanizer-skill.vercel.app/ai-slop.html) · [Changelog](CHANGELOG.md) · MIT

A skill that turns AI-slop prose into writing that survives a hostile editor's red
pen — **without** swapping one kind of slop for another. Portable to **every AI
tool**: Claude Code, Cursor, GitHub Copilot, Codex (`AGENTS.md`), Gemini,
Windsurf, or any chatbot via a paste-anywhere prompt — all generated from one
source.

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

## Install for your tool

One source, every harness. Each adapter is generated from the same `SKILL.md` —
pick yours, then invoke with *"humanize this"*, *"de-slop this"*, *"make this
sound less like AI"*, or *"this reads like ChatGPT"*.

| Tool | Install |
|---|---|
| **Claude Code** | `git clone … ~/.claude/skills/harness-humanizer` |
| **Cursor** | copy [`adapters/cursor/harness-humanizer.mdc`](adapters/cursor/harness-humanizer.mdc) → `.cursor/rules/` |
| **GitHub Copilot** | copy [`adapters/copilot/…instructions.md`](adapters/copilot/harness-humanizer.instructions.md) → `.github/instructions/` |
| **Codex / Amp / Jules / Pi / etc.** | copy [`adapters/AGENTS.md`](adapters/AGENTS.md) → repo root |
| **Gemini CLI** | copy [`adapters/gemini/GEMINI.md`](adapters/gemini/GEMINI.md) → repo root or `~/.gemini/` |
| **Windsurf** | copy [`adapters/windsurf/harness-humanizer.md`](adapters/windsurf/harness-humanizer.md) → `.windsurf/rules/` |
| **Any chatbot** | paste [`adapters/PROMPT.md`](adapters/PROMPT.md) into ChatGPT/Claude/Gemini |

```bash
# Claude Code
git clone https://github.com/isatimur/harness-humanizer-skill.git
cp -R harness-humanizer-skill ~/.claude/skills/harness-humanizer

# Cursor (example) — fetch just the adapter
mkdir -p .cursor/rules && curl -o .cursor/rules/harness-humanizer.mdc \
  https://raw.githubusercontent.com/isatimur/harness-humanizer-skill/main/adapters/cursor/harness-humanizer.mdc
```

Editing the rules? Change `SKILL.md` / `references/` and run
`python3 scripts/build_adapters.py` to regenerate every adapter (CI enforces sync).

## CLI: the deterministic flagger

Run the zero-dependency pre-flagger anywhere. **`uv` is the recommended installer:**

```bash
# one-off, no install
uvx --from git+https://github.com/isatimur/harness-humanizer-skill \
  humanizer-flag yourfile.md --score

# install as a tool
uv tool install git+https://github.com/isatimur/harness-humanizer-skill
humanizer-flag yourfile.md                 # JSON of flagged tells
humanizer-flag yourfile.md --score         # per-paragraph slop_band
humanizer-flag yourfile.md --profile stop-slop   # aggressive opt-in rules
```

`pipx install` works identically. Or score text with no install at all in the
**[free in-browser tool](https://harness-humanizer-skill.vercel.app/#tool)**.

## Layout

```
SKILL.md                 # invocation surface: triggers + the loop (canonical source)
references/
  rubric.md              # the 4 bands, slop indicators, two tests, triage, substance lens
  guardrails.md          # fidelity rules + over-correction anti-pattern catalogue
  examples.md            # before→after pairs; flag-don't-fabricate; PASS/FAIL cases
  slop-catalogue.md      # full taxonomy: each tell → its detector type (or none)
scripts/
  flag_slop.py           # stdlib-only regex pre-pass → JSON; --selftest, --score, --profile
  build_adapters.py      # renders SKILL.md + references/ → every tool's format; --check
adapters/                # GENERATED — one per tool (cursor, copilot, AGENTS.md, …) + PROMPT.md
pyproject.toml           # packages flag_slop.py as the `humanizer-flag` CLI (uv/pipx)
docs/                    # the website (Vercel): landing page, glossary, slop.js scorer
tests/                   # dev-only; omittable from a runtime install
  corpus/*.jsonl         # labeled slop / clean / over-correction samples
  eval.py                # deterministic detector gate (recall, specificity, …)
  check_js_parity.py     # docs/slop.js must match flag_slop.py's rule inventory
  thresholds.json        # pass/fail gates
.github/workflows/ci.yml # self-test + eval + adapter-sync + parity, Python 3.9–3.13, no pip
```

The runtime skill is just `SKILL.md`, `references/`, and `scripts/` (or a single
adapter from `adapters/`) — everything else is development or distribution assets.

## Detector & the ecosystem

The detector's taxonomy folds in and extends
[stop-slop](https://github.com/hardikpandya/stop-slop) (MIT) and its community
PRs — rendered as *weighted, idiom-anchored* rules rather than a flat block-list,
so honest technical prose stays silent. The design bet differs: where banned-list
tools *prescribe* a replacement style (be punchy, drop em-dashes, go
second-person), this skill treats those prescriptions as **over-correction** —
louder slop in a different costume — and guards against them. Credit and the full
rationale live in [`references/slop-catalogue.md`](references/slop-catalogue.md).

## Verify

```bash
python3 scripts/flag_slop.py --selftest   # detector smoke test
python3 tests/eval.py                      # full detector eval against the corpus
python3 tests/check_no_deps.py             # confirm it's still stdlib-only
```

The detector also emits a per-paragraph **slop score** with
`python3 scripts/flag_slop.py --score <file>`. That score measures *surface slop
tells only* — it is **not** a humanness judge. A paragraph with no slop words can
still be hollow (no claim) and fail the rubric; only a reader or the model loop
can catch that. A green eval means the candidate-surfacer behaves, never "the
writing is good."

## Origin

The rubric is adapted from the **humanness** judge in
[book-mash](https://github.com/isatimur), the multi-judge quality engine behind
[*From Copilot to Colleague*](https://fromcopilottocolleague.com/). This skill is
the inverse of that judge: where the judge *measures* slop, this *removes* it.

## License

MIT © Timur Isachenko
