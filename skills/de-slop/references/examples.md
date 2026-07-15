# Examples

Before→after pairs showing each move. Study the *reasoning*, not just the
rewrite — the judgment of rewordable vs. hollow is the whole skill.

**Fidelity rule for every "After" below:** no new claim, number, name, or
mechanism that was not already in the **Before** (or its immediately quoted
surrounding context). Pure subtraction is the default. If a rewrite needs a
specific (Postgres, microseconds, JSON/CSV…), the surrounding text must already
supply that specific — otherwise FLAG as HOLLOW.

---

## Rewordable: empty hedging (pure subtraction)

**Before** (weak — hedging buries a real claim):
> It's worth noting that, in many cases, caching can often lead to significant
> improvements in performance for a wide variety of applications.

**After** (strong — the claim, stated; only padding removed):
> Caching improves performance for many applications.

Why: the source *had* a claim (caching improves performance). "It's worth
noting", "in many cases", "often", "significant", "a wide variety of" add no
meaning. Subtract them. Do **not** invent hit/miss latencies or a mechanism the
source never named.

---

## Rewordable: listicle stem (only when context supplies the factors)

**Before** (weak stem, but a claim arrives in the next sentence of the same
block):
> There are several important factors to consider when choosing a database. A
> document store buys flexible schemas at the cost of joins; a relational store
> trades the reverse.

**After** (strong — stem gone, existing tradeoff kept):
> Choosing a database means choosing what you give up: a document store buys
> flexible schemas at the cost of joins; a relational store trades the reverse.

Why: the tradeoff was already in the source. If the source never names a single
factor, the listicle stem alone is HOLLOW — see below. Do not invent document vs
relational if only the stem exists.

---

## Rewordable: smooth transition → flag when no claim exists

**Before** (weak — "moreover" glues two non-claims):
> The system is designed to be scalable. Moreover, it is built with modern
> technologies that ensure reliability and performance.

**CORRECT response** — flag it, do not invent architecture:
> FLAG (hollow): "Scalable" and "modern technologies" name no mechanism. Deleting
> the paragraph loses nothing. Needs a real claim (how it scales, what the stack
> is), not rewording.

**WRONG response** — fabricating stack details (FAILURE):
> ✗ "The system scales horizontally with stateless workers behind a queue; state
> lives in Postgres…" — invents workers, queues, and Postgres the source never
> mentioned.

---

## Flag, don't fabricate: a hollow paragraph

**Before** (hollow — nothing is being claimed):
> In today's fast-paced digital landscape, leveraging the right tools is more
> important than ever. Organizations must adapt to stay ahead.

**CORRECT response** — flag it:
> FLAG (hollow): This paragraph makes no claim. "The right tools matter" and
> "organizations must adapt" survive no removal test — deleting the paragraph
> loses nothing. It needs a real point (which tools, what adaptation, why now),
> not rewording.

**WRONG response** — fabricating a stance (this is a FAILURE):
> ✗ "Most companies pick tools to look modern, not to solve a problem — and it
> shows in their bloated stacks."
> This invents a contrarian claim the source never made. Slop replaced with
> edgy-slop. Do not do this.

---

## Over-correction: slop → genuine sharpening (PASS) vs slop → edgy-slop (FAIL)

**Before** (has a claim: testing helps quality / development):
> Testing is an important part of the development process that helps ensure
> quality.

**PASS** (subtract + light sharpen; no new domain facts):
> Testing helps ensure quality in development.

**FAIL** (over-corrected — manufactured voice + stance the source didn't have):
> ✗ "Let's be honest: if you're not testing, you're not really an engineer —
> you're just typing and hoping."
> Performed candor ("let's be honest"), a hot take, and an insult the source
> never implied. Louder, still slop.

**Also FAIL** (invented concreteness the source didn't earn):
> ✗ "Tests are the only reason you can change code you wrote six months ago
> without re-reading all of it." — crisp writing, but it adds a claim
> (regression-without-reread) the before never made. Prefer the lean PASS above
> unless the surrounding draft already argues that.

---

## Rewordable: LLM-lexicon filler (delve / tapestry / realm)

**Before** (weak lexicon *and* a named set of options in the same block):
> Let's delve into the rich tapestry of options available in the realm of modern
> caching strategies: cache-aside, write-through, and write-behind.

**After** (strong — lexicon gone, named options kept):
> Caching strategies split three ways: cache-aside, write-through, and
> write-behind.

Why: rewrite this way ONLY if the source names those strategies. If "options"
refers to nothing concrete, it's HOLLOW — flag it. The "delve/tapestry/realm"
vocabulary is never the problem by itself; the absence of a named option is.

---

## Rewordable: corporate uplift (empower / leverage / seamless)

**Before** (weak — buzzwords *and* a stated mechanism in the same block):
> Our platform empowers teams to leverage cutting-edge tooling for a seamless,
> robust workflow. It runs your existing CI config and caches build artifacts
> across branches.

**After** (strong — mechanism kept, marketing peeled off):
> The platform runs your existing CI config and caches build artifacts across
> branches.

Why: the `empower` rule is sentence-aware. Marketing words ("empowers",
"seamless", "cutting-edge") flag; riders ("leverage", "robust") flag when they
share that register. Fix by keeping the mechanism and dropping the uplift. If
there's no mechanism to keep, HOLLOW. Standalone "we leverage connection pooling"
or "robust error handling" in honest technical prose is deliberately *not*
flagged.

---

## Rewordable: vague quantifier (a wide variety of)

**Before** (vague opener, specific formats already named):
> The library supports a wide variety of formats for a number of use cases: JSON,
> CSV, and Parquet, read and write.

**After** (strong — the actual list, quantifier gone):
> The library reads and writes JSON, CSV, and Parquet.

Why: rewrite ONLY if the source names the formats. If it never does, "a wide
variety of" is concealing that there's no real list — HOLLOW. Do not invent
JSON/CSV/Parquet to fill the hole.

---

## The hard judgment call: REWORDABLE vs HOLLOW on near-identical prose

These two look almost the same. The difference is whether a claim exists *in the
surrounding context*, not in the stem alone.

**Case A — REWORDABLE** (the next sentence supplies the point):
> There are several factors to weigh when picking a queue. Throughput, ordering
> guarantees, and redelivery semantics each pull in different directions, and most
> brokers force you to pick two.

→ The listicle stem is slop, but the claim is right there. Subtract the stem:
> Picking a queue means trading off throughput, ordering, and redelivery — most
> brokers let you optimize two of the three, not all.

**Case B — HOLLOW** (identical stem, no point ever arrives):
> There are several factors to weigh when picking a queue. It's important to
> consider your needs carefully and choose the option that's right for you.

→ FLAG (hollow): the stem promises factors; none are named. "Consider your needs"
and "choose what's right" survive no removal test. This needs a real claim (which
factors, what tradeoff), not rewording. **Do not invent the tradeoff from Case A
to rescue Case B** — that's fabrication.

The whole skill lives in telling A from B. When unsure, apply the removal test: if
deleting the paragraph costs the reader nothing, it's hollow.

---

## Over-correction: another PASS vs FAIL pair

**Before:**
> Documentation is an essential part of any software project.

**PASS** (claim stated without padding — no new story about "a year from now"):
> Documentation is essential in software projects.

**FAIL** (over-corrected — manufactured stakes + hot take the source never made):
> ✗ "In today's ship-or-die world, undocumented code isn't just lazy — it's
> sabotage." Manufactured stakes ("in today's…world"), em-dash theatrics, and an
> accusation the source never implied. Louder, still slop.

---

## Idempotence: already-strong prose

**Before** (already strong):
> A cache miss isn't free — it's the full cost plus the bookkeeping of storing the
> result. Caches win only when hits outnumber misses enough to pay that tax back.

**Correct response:** return unchanged. Score = strong. Nothing to do.
