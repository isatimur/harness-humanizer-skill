# Slop Catalogue

The full taxonomy of AI-slop tells: what each one is, *why* it reads as machine
prose, the detector type that catches it (`scripts/flag_slop.py`), and a canonical
example. This is the single map linking **rules ↔ rubric ↔ corpus**.

Read this to understand *why* something is flagged. The detector surfaces
candidates; the rubric (`rubric.md`) decides bands; this file explains the tells.

## How to read the "detector" column

- A **type name** (`hedge`, `delve`, …) means `flag_slop.py` has a regex for it.
- **model-judgment-only** means there is *deliberately no regex* — the tell needs
  semantics a regex can't see, so only the model (or a human) catches it. These
  are the detector's blind spots, documented on purpose so nobody mistakes a
  quiet detector for clean prose.

---

## Lexically detectable tells (the detector catches these)

| Tell | Why it reads as AI | Detector type | Canonical example |
|---|---|---|---|
| Empty hedging | Avoids committing to the claim it's about to make | `hedge` | "It's worth noting that caching helps." |
| Listicle stem | Announces structure instead of making a point | `listicle` | "There are several key factors to consider." |
| Dead transition | "Moreover/Furthermore" gluing two non-claims | `transition` | "Moreover, the system is robust." |
| Manufactured stakes | Borrowed urgency the content didn't earn | `stakes` | "In today's fast-paced world, speed matters." |
| Performed candor | Fake intimacy to sound human | `candor` | "Let's be honest, nobody reads docs." |
| Rhetorical opener | Engagement-bait with no information | `rhetq` | "Ever wondered why your build is slow?" |
| Not-only-but-also | Inflates one idea into two | `notonly` | "Not only fast, but also cheap." |
| Filler adverb | "genuinely/truly/honestly" as flavor | `intensifier_filler` | "a truly elegant abstraction" |
| Degree intensifier | "very/really + adj" — *often legitimate*, low weight | `intensifier_degree` | "very old browsers" |
| Vague quantifier | "a wide variety of" stands in for a real number | `weaselquant` | "a wide variety of options" |
| Negative-parallel cadence | The "it's not X, it's Y" LLM rhythm | `negparallel` | "It's not just a database, it's a platform." |
| LLM lexicon | "delve / tapestry / realm / testament" | `delve` | "delve into the rich tapestry" |
| Wrap-up scaffolding | "In conclusion / the key takeaway is" | `conclusion` | "In conclusion, it saves time." |
| Corporate uplift | marketing-register buzzwords; *sentence-aware* (see below) | `empower` | "empowers teams to leverage cutting-edge tools" |
| Rule-of-three triplet | Three buzz adjectives in a row | `triadic` | "fast, reliable, and scalable" |
| Call to action | "Buckle up / without further ado / read on" | `calltoaction` | "Buckle up, this changes everything." |
| Em-dash theatrics | Dashes manufacturing unearned emphasis | `emdash` | "It was fast — clean — and correct — somehow." |

### A note on weight

Not every tell is equally damning. `flag_slop.py` weights them (see `_WEIGHTS`):
listicle and stakes are strong signals (20); a lone degree intensifier is weak
(6). This is why "very old browsers" surfaces as a *candidate* but doesn't drag a
paragraph's `slop_band` down — only **clusters** of tells accumulate enough weight
to matter. The detector flags; it does not convict.

### The `empower` rule is sentence-aware

"leverage", "robust", "unlock", "harness", "streamline", "elevate" appear
constantly in honest engineering prose ("we leverage connection pooling", "robust
error handling"). Flagging them there would be noise. So `empower` splits its
vocabulary in two:

- **Marketing-register words** — "empower", "seamless", "frictionless", "synergy",
  "cutting-edge", "state-of-the-art", "best-in-class", "world-class",
  "game-changer", "supercharge", "turnkey", "paradigm shift". These almost never
  occur in honest technical writing, so they **fire on their own**.
- **Rider words** — "leverage", "robust", "unlock", "harness", "elevate",
  "streamline". These **fire only when a marketing word shares the same
  sentence** — i.e. the register is already slop. On their own they stay silent.

So "We leverage Postgres connection pooling to reduce tail latency" is silent,
while "Our seamless platform empowers teams to leverage cutting-edge tooling"
flags the whole cluster. This is still surface-pattern matching, not semantics —
a marketing sentence with zero buzzwords ("our solution helps you do more") slips
through, and that's the detector's documented boundary, not a bug.

---

## Model-judgment-only tells (no regex — the detector is blind here)

These are slop, but no pattern catches them. They are the reason a quiet detector
is **not** proof of clean prose, and the reason the skill loop always re-judges
every paragraph against the rubric rather than trusting the pre-flag.

| Tell | Why no regex | How it's caught |
|---|---|---|
| **Hollowness** — a paragraph that makes no claim at all | "No point" is semantic, not lexical; the words can be perfectly clean | The removal test (`rubric.md`): delete it — is anything lost? |
| **Fabricated stance** — a contrarian hot take in plain words | "Most companies pick tools to look modern" trips no trigger word | The guardrails' over-correction catalogue + fidelity check |
| **Smooth-but-empty specificity** — concrete-sounding nouns that refer to nothing | "modern technologies that ensure reliability" reads specific, says nothing | Does the surrounding context support the specifics? |
| **Plausible-but-wrong claim** | Fidelity, not slop; a regex can't fact-check | Human / source comparison |

**The boundary, stated plainly:** the detector measures *surface tells*, never
*claim presence*. A green `--score` means "no surface slop", not "good writing".
Hollowness is invisible to it — which is exactly why the skill flags hollow spans
by judgment, never by regex, and never fabricates a claim to fill them.

---

## Cross-references

- `rubric.md` — turns these tells into `strong|moderate|weak|fail` bands.
- `guardrails.md` — the over-correction anti-patterns (the louder-slop costumes).
- `examples.md` — before→after pairs for the rewordable tells; flag cases for the
  hollow ones.
- `tests/corpus/*.jsonl` — at least one labeled sample per detectable type.
