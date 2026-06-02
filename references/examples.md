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

## Idempotence: already-strong prose

**Before** (already strong):
> A cache miss isn't free — it's the full cost plus the bookkeeping of storing the
> result. Caches win only when hits outnumber misses enough to pay that tax back.

**Correct response:** return unchanged. Score = strong. Nothing to do.
