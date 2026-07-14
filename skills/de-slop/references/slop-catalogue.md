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
| Throat-clearing opener | Announces a reveal instead of making it | `throatclear` | "The uncomfortable truth is most teams skip tests." |
| Emphasis crutch | Tells you it matters instead of showing it | `emphasis_crutch` | "Make no mistake, this will break." |
| Meta-commentary | Narrates the writing instead of writing | `metacommentary` | "Let me walk you through why it failed." |
| Binary-contrast cadence | The "the answer isn't X, it's Y" reveal rhythm | `binarycontrast` | "The answer isn't more servers. It's caching." |
| Negative listing | Staccato "it wasn't X, it wasn't Y, it was Z" | `neglisting` | "It wasn't the code. It wasn't the config. It was DNS." |
| Business-jargon idiom | Office filler standing in for a verb | `bizjargon` | "Let's circle back and move the needle." |
| Assistant voice | Chatbot sycophancy / email pleasantry | `assistantvoice` | "Great question! I'd be happy to help." |
| Transformation chain | "X becomes Y. Y becomes Z." false momentum | `transformchain` | "Friction becomes flow. Flow becomes speed." |
| Corrective reveal | "You've been told X; here's the truth" posturing | `correctivereveal` | "You've been told tests slow you down. Here's the truth: they don't." |
| Forced cohesion | Manufactured profundity binding two ideas | `forcedcohesion` | "You can't have one without the other." |
| Copula inflation | "boasts / serves as a testament" dodging "is/has" | `copula` | "The framework boasts a clean API." |
| Stacked hedges | Two qualifiers where zero or one belong | `hedgestack` | "It might possibly be a memory leak." |

### Harvested from stop-slop (and why ours differs)

The twelve tells above (from "Throat-clearing opener" down) were catalogued by
[stop-slop](https://github.com/hardikpandya/stop-slop) (MIT, Hardik Pandya) — an
excellent, widely-used banned-list skill — and its community pull requests:
assistant-voice and hedge-stacks from
[PR #4](https://github.com/hardikpandya/stop-slop/pull/4), email pleasantries /
transformation chains / corrective reveals / forced cohesion from
[PR #5](https://github.com/hardikpandya/stop-slop/pull/5), and copula inflation +
the register-aware framing from
[PR #8](https://github.com/hardikpandya/stop-slop/pull/8). We fold the taxonomy
into a *runnable, weighted, low-false-positive detector* rather than a flat
block-list: each pattern is idiom-anchored so honest technical prose stays silent
(a blanket "ban every adverb" match would not).

PR #8's "register-aware" thesis — different writing contexts tolerate different
patterns — is the same instinct behind this detector's sentence-aware rules (the
`empower` rider split, the low-weight `intensifier_degree`). A lone hedge in
academic prose or an em-dash in narrative is not automatically slop; only clusters
convict. The deeper difference is philosophy — stop-slop
*prescribes* a replacement style (be punchy, drop em-dashes, go second-person);
several of those prescriptions are exactly the over-correction `guardrails.md`
flags as *louder slop*. That is why `binarycontrast` and `neglisting` live in the
**over-correction** corpus: they are shapes a naive humanizer produces, and the
detector must catch them too.

### The `stop-slop` profile (opt-in interop)

`flag_slop.py --profile stop-slop` switches on stop-slop's stricter, aggressive
rules — `adverb_ly` (every -ly adverb), `wh_opener` (Wh- question openers),
`emdash_any` (any em-dash) — which the default profile keeps **off** because
fidelity-first writing tolerates a lone adverb or dash. Fans of stop-slop's style
get its severity *plus* our non-destructive report and over-correction guardrails.
These extra rules are deliberately excluded from the gated eval; the default
profile is what carries the low-false-positive contract.

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
