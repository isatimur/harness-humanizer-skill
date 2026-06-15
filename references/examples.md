# Examples

Before→after pairs showing each move. Study the *reasoning*, not just the
rewrite — the judgment of rewordable vs. hollow is the whole skill.

## Rewordable: empty hedging

**Before** (weak — hedging buries a real claim):
> It's worth noting that, in many cases, caching can often lead to significant
> improvements in performance for a wide variety of applications.

**After** (strong — the claim, stated):
> Caching cuts repeated work, so a cache hit returns in microseconds what a cache
> miss spends milliseconds computing.

Why: the source *had* a claim (caching improves performance); it was smothered by
"it's worth noting", "in many cases", "often", "a wide variety." Subtract the
hedging, name the mechanism. Meaning preserved.

## Rewordable: listicle stem

**Before** (weak — stem with no point of view):
> There are several important factors to consider when choosing a database. Let's
> explore some of the key considerations.

**After** (strong — commits to the actual point):
> Choosing a database is mostly choosing what you're willing to give up: a
> document store buys flexible schemas at the cost of joins; a relational store
> trades the reverse.

Why: only rewrite this way if the surrounding text actually makes that tradeoff
point. If the source never names a single factor, this is HOLLOW — see below.

## Rewordable: smooth transition hiding no claim

**Before** (weak — "moreover" glues two non-claims):
> The system is designed to be scalable. Moreover, it is built with modern
> technologies that ensure reliability and performance.

**After** (strong — concrete, falsifiable):
> The system scales horizontally: stateless workers behind a queue, so adding
> capacity is adding workers. State lives in Postgres, the one component that
> can't be cloned away.

Why: rewrite this way ONLY if the source's surrounding context supports those
specifics. If "modern technologies" refers to nothing concrete, flag it.

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

## Over-correction: slop → genuine sharpening (PASS) vs slop → edgy-slop (FAIL)

**Before:**
> Testing is an important part of the development process that helps ensure
> quality.

**PASS** (sharpened, fidelity intact):
> Tests are the only reason you can change code you wrote six months ago without
> re-reading all of it.

**FAIL** (over-corrected — manufactured voice + stance the source didn't have):
> ✗ "Let's be honest: if you're not testing, you're not really an engineer —
> you're just typing and hoping."
> Performed candor ("let's be honest"), a hot take, and an insult the source
> never implied. Louder, still slop.

## Rewordable: LLM-lexicon filler (delve / tapestry / realm)

**Before** (weak — buzzword vocabulary, real point underneath):
> Let's delve into the rich tapestry of options available in the realm of modern
> caching strategies.

**After** (strong — names the actual options):
> Caching strategies split three ways: cache-aside, write-through, and
> write-behind — each trades freshness against write latency differently.

Why: rewrite this way ONLY if the source actually goes on to discuss those
strategies. If "options" refers to nothing concrete, it's HOLLOW — flag it. The
"delve/tapestry/realm" vocabulary is never the problem by itself; the absence of
a named option is.

## Rewordable: corporate uplift (empower / leverage / seamless)

**Before** (weak — buzzwords standing in for a mechanism):
> Our platform empowers teams to leverage cutting-edge tooling for a seamless,
> robust workflow.

**After** (strong — what it actually does):
> The platform runs your existing CI config unchanged and adds one thing: it
> caches build artifacts across branches, so a green main makes feature branches
> build in seconds.

Why: "empower/leverage/seamless/robust" are low-weight candidates — they flag, but
they're only slop when they *replace* a mechanism. The fix is naming the
mechanism, not deleting the words. If there's no mechanism to name, HOLLOW.

## Rewordable: vague quantifier (a wide variety of)

**Before** (weak — "a wide variety" hides the absence of a count):
> The library supports a wide variety of formats for a number of use cases.

**After** (strong — the actual list):
> The library reads JSON, CSV, and Parquet, and writes all three back — enough for
> ETL work, not enough to be a general serialization layer.

Why: rewrite ONLY if the source names the formats somewhere. If it never does,
"a wide variety of" is concealing that there's no real list — HOLLOW.

## The hard judgment call: REWORDABLE vs HOLLOW on near-identical prose

These two look almost the same. The difference is whether a claim exists *in the
surrounding context*, not in the sentence itself.

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

## Over-correction: another PASS vs FAIL pair

**Before:**
> Documentation is an essential part of any software project.

**PASS** (sharpened, fidelity intact):
> Docs are the interface to your code for everyone who didn't write it — including
> you, a year from now.

**FAIL** (over-corrected — manufactured stakes + hot take the source never made):
> ✗ "In today's ship-or-die world, undocumented code isn't just lazy — it's
> sabotage." Manufactured stakes ("in today's…world"), em-dash theatrics, and an
> accusation the source never implied. Louder, still slop.

## Idempotence: already-strong prose

**Before** (already strong):
> A cache miss isn't free — it's the full cost plus the bookkeeping of storing the
> result. Caches win only when hits outnumber misses enough to pay that tax back.

**Correct response:** return unchanged. Score = strong. Nothing to do.
