#!/usr/bin/env python3
"""Batch 2 real-world corpus seeder — validate then append (idempotent by id)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from flag_slop import flag  # noqa: E402

SLOP = [
    {"id": "slop-rw2-hedge-001", "text": "It's worth noting that most outages trace back to a config change, not a code change.", "expect": ["hedge"], "band": "moderate", "source": "real-world", "note": "SRE blog hedge over a real claim"},
    {"id": "slop-rw2-hedge-002", "text": "That said, the rollout was paused after the first canary regressed.", "expect": ["hedge"], "band": "moderate", "source": "real-world", "note": "status page hedge"},
    {"id": "slop-rw2-hedge-003", "text": "It is important to remember that backups are useless until you test a restore.", "expect": ["hedge"], "band": "moderate", "source": "real-world", "note": "ops wiki"},
    {"id": "slop-rw2-stakes-001", "text": "In today's modern era, every company is a software company whether it likes it or not.", "expect": ["stakes"], "band": "fail", "source": "real-world", "note": "keynote abstract"},
    {"id": "slop-rw2-stakes-002", "text": "The stakes have never been higher for data governance teams.", "expect": ["stakes"], "band": "fail", "source": "real-world", "note": "compliance webinar"},
    {"id": "slop-rw2-list-001", "text": "There are a number of reasons your p99 might spike under load.", "expect": ["listicle"], "band": "weak", "source": "real-world", "note": "perf tutorial opener"},
    {"id": "slop-rw2-list-002", "text": "Let's explore how retrieval-augmented generation actually works under the hood.", "expect": ["listicle"], "band": "weak", "source": "real-world", "note": "RAG explainer"},
    {"id": "slop-rw2-list-003", "text": "Here are some things to consider before adopting a service mesh.", "expect": ["listicle"], "band": "weak", "source": "real-world", "note": "platform post"},
    {"id": "slop-rw2-trans-001", "text": "Moreover, the approach scales cleanly across regions.", "expect": ["transition"], "band": "weak", "source": "real-world", "note": "design doc glue"},
    {"id": "slop-rw2-trans-002", "text": "Furthermore, teams reported higher satisfaction after the change.", "expect": ["transition"], "band": "weak", "source": "real-world", "note": "retro summary"},
    {"id": "slop-rw2-candor-001", "text": "Let's be honest, your test suite is slow because nobody owns it.", "expect": ["candor"], "band": "weak", "source": "real-world", "note": "eng manager blog"},
    {"id": "slop-rw2-candor-002", "text": "Truth be told, the migration took three times longer than we scoped.", "expect": ["candor"], "band": "moderate", "source": "real-world", "note": "postmortem candor"},
    {"id": "slop-rw2-rhetq-001", "text": "Have you ever wondered why your CI bill keeps climbing?", "expect": ["rhetq"], "band": "weak", "source": "real-world", "note": "vendor ad"},
    {"id": "slop-rw2-delve-001", "text": "Let's delve into the internals of the scheduler.", "expect": ["delve"], "band": "weak", "source": "real-world", "note": "deep-dive intro"},
    {"id": "slop-rw2-delve-002", "text": "This release is a testament to two years of platform investment.", "expect": ["delve"], "band": "weak", "source": "real-world", "note": "launch blog"},
    {"id": "slop-rw2-delve-003", "text": "When it comes to security, defense in depth is non-negotiable.", "expect": ["delve"], "band": "moderate", "source": "real-world", "note": "security post cliché opener"},
    {"id": "slop-rw2-weasel-001", "text": "The SDK integrates with a wide range of downstream tools.", "expect": ["weaselquant"], "band": "moderate", "source": "real-world", "note": "SDK docs"},
    {"id": "slop-rw2-weasel-002", "text": "We support countless deployment topologies out of the box.", "expect": ["weaselquant"], "band": "moderate", "source": "real-world", "note": "marketing overreach"},
    {"id": "slop-rw2-weasel-003", "text": "A myriad of factors influence embedding quality.", "expect": ["weaselquant"], "band": "moderate", "source": "real-world", "note": "ML blog"},
    {"id": "slop-rw2-negpar-001", "text": "It's not just faster, it's a fundamentally different workflow.", "expect": ["negparallel"], "band": "weak", "source": "real-world", "note": "product launch cadence"},
    {"id": "slop-rw2-concl-001", "text": "In summary, adopting typed configs removed a whole class of bugs.", "expect": ["conclusion"], "band": "moderate", "source": "real-world", "note": "wrap-up"},
    {"id": "slop-rw2-concl-002", "text": "All in all, the rewrite paid for itself within a quarter.", "expect": ["conclusion"], "band": "moderate", "source": "real-world", "note": "case study close"},
    {"id": "slop-rw2-emp-001", "text": "Our best-in-class platform delivers a frictionless developer experience.", "expect": ["empower"], "band": "fail", "source": "real-world", "note": "homepage hero"},
    {"id": "slop-rw2-emp-002", "text": "A state-of-the-art engine that supercharges your data pipelines.", "expect": ["empower"], "band": "fail", "source": "real-world", "note": "data vendor"},
    {"id": "slop-rw2-emp-003", "text": "Unlock next-generation productivity with our AI copilot.", "expect": ["empower"], "band": "fail", "source": "real-world", "note": "ad copy"},
    {"id": "slop-rw2-tri-001", "text": "Build software that is secure, scalable, and reliable by default.", "expect": ["triadic"], "band": "moderate", "source": "real-world", "note": "framework tagline"},
    {"id": "slop-rw2-cta-001", "text": "Ready to level up? Let's dive in.", "expect": ["calltoaction"], "band": "weak", "source": "real-world", "note": "course intro"},
    {"id": "slop-rw2-cta-002", "text": "Without further ado, here's the new dashboard.", "expect": ["calltoaction"], "band": "weak", "source": "real-world", "note": "release note"},
    {"id": "slop-rw2-emdash-001", "text": "Simple — fast — and reliable — that was the pitch.", "expect": ["emdash"], "band": "moderate", "source": "real-world", "note": "pitch slide"},
    {"id": "slop-rw2-throat-001", "text": "The real problem here is that nobody defined what 'done' means.", "expect": ["throatclear"], "band": "weak", "source": "real-world", "note": "process critique"},
    {"id": "slop-rw2-throat-002", "text": "Let me be clear: retries without idempotency make outages worse.", "expect": ["throatclear"], "band": "weak", "source": "real-world", "note": "reliability post"},
    {"id": "slop-rw2-emph-001", "text": "Make no mistake, unbounded queues will eventually take you down.", "expect": ["emphasis_crutch"], "band": "weak", "source": "real-world", "note": "capacity post"},
    {"id": "slop-rw2-meta-001", "text": "In this post, we'll walk through migrating from REST to gRPC.", "expect": ["metacommentary"], "band": "weak", "source": "real-world", "note": "tutorial meta opener"},
    {"id": "slop-rw2-meta-002", "text": "Spoiler: the bottleneck was DNS the whole time.", "expect": ["metacommentary"], "band": "weak", "source": "real-world", "note": "debugging story"},
    {"id": "slop-rw2-biz-001", "text": "Let's circle back on the roadmap once we move the needle on activation.", "expect": ["bizjargon"], "band": "weak", "source": "real-world", "note": "planning meeting"},
    {"id": "slop-rw2-biz-002", "text": "We should double down on the low-hanging fruit this sprint.", "expect": ["bizjargon"], "band": "weak", "source": "real-world", "note": "sprint planning"},
    {"id": "slop-rw2-asst-001", "text": "Great question! Let me break that down for you step by step.", "expect": ["assistantvoice"], "band": "fail", "source": "real-world", "note": "chatbot reply"},
    {"id": "slop-rw2-asst-002", "text": "I'd be happy to help you architect this system.", "expect": ["assistantvoice"], "band": "fail", "source": "real-world", "note": "assistant courtesy"},
    {"id": "slop-rw2-copula-001", "text": "The library boasts first-class TypeScript support.", "expect": ["copula"], "band": "weak", "source": "real-world", "note": "readme puffery"},
    {"id": "slop-rw2-copula-002", "text": "This partnership stands as a testament to open collaboration.", "expect": ["copula"], "band": "weak", "source": "real-world", "note": "press release"},
    {"id": "slop-rw2-hedgestack-001", "text": "It may possibly be a caching issue, but we're not sure yet.", "expect": ["hedgestack"], "band": "weak", "source": "real-world", "note": "triage note"},
    {"id": "slop-rw2-notonly-001", "text": "Not only is it open source, but also it ships with a hosted option.", "expect": ["notonly"], "band": "moderate", "source": "real-world", "note": "comparison page"},
    {"id": "slop-rw2-intens-001", "text": "This is honestly a genuinely underrated pattern for retries.", "expect": ["intensifier_filler"], "band": "moderate", "source": "real-world", "note": "hn comment"},
    {"id": "slop-rw2-fill-001", "text": "At the end of the day, correctness beats cleverness.", "expect": ["hedge"], "band": "moderate", "source": "real-world", "note": "principle stated with filler"},
    {"id": "slop-rw2-stakes-003", "text": "Now more than ever, latency is a feature, not an afterthought.", "expect": ["stakes"], "band": "fail", "source": "real-world", "note": "perf marketing"},
    {"id": "slop-rw2-list-004", "text": "There are several important factors to weigh when sizing a Kafka cluster.", "expect": ["listicle"], "band": "weak", "source": "real-world", "note": "infra guide"},
    {"id": "slop-rw2-delve-004", "text": "Navigating the complex world of IAM policies is a rite of passage.", "expect": ["delve"], "band": "moderate", "source": "real-world", "note": "cloud post"},
    {"id": "slop-rw2-transform-001", "text": "Data becomes insight. Insight becomes advantage.", "expect": ["transformchain"], "band": "weak", "source": "real-world", "note": "analytics tagline (also OC-adjacent)"},
]

CLEAN = [
    {"id": "clean-rw2-001", "text": "The consumer lagged because we set max.poll.records too high for the handler's per-message cost.", "expect": [], "band": "strong", "source": "real-world", "note": "kafka tuning note"},
    {"id": "clean-rw2-002", "text": "We shard by tenant id so a noisy customer can't starve the rest.", "expect": [], "band": "strong", "source": "real-world", "note": "multitenant design"},
    {"id": "clean-rw2-003", "text": "The flake was a clock skew between the test runner and the token issuer.", "expect": [], "band": "strong", "source": "real-world", "note": "test flake root cause"},
    {"id": "clean-rw2-004", "text": "Rate-limit at the edge; the origin should never see more than it can serve.", "expect": [], "band": "strong", "source": "real-world", "note": "edge rule"},
    {"id": "clean-rw2-005", "text": "We roll forward, not back: a bad deploy gets a fix-forward within the hour or an automated revert.", "expect": [], "band": "strong", "source": "real-world", "note": "deploy policy"},
    {"id": "clean-rw2-006", "text": "The agent kept retrying a 400 because the error schema looked like a 500 to its parser.", "expect": [], "band": "strong", "source": "real-world", "note": "agent bug"},
    {"id": "clean-rw2-007", "text": "Store idempotency keys for 24 hours so a client retry never double-charges.", "expect": [], "band": "strong", "source": "real-world", "note": "payments rule"},
    {"id": "clean-rw2-008", "text": "We cap the context window at 8k tokens and summarize older turns into a running memo.", "expect": [], "band": "strong", "source": "real-world", "note": "context management"},
    {"id": "clean-rw2-009", "text": "The migration is reversible until the drop-column step; everything before it is additive.", "expect": [], "band": "strong", "source": "real-world", "note": "schema migration"},
    {"id": "clean-rw2-010", "text": "A code review that only checks style misses the design bug that costs a rewrite.", "expect": [], "band": "strong", "source": "real-world", "note": "review philosophy"},
    {"id": "clean-rw2-011", "text": "We measure eval pass rate per tool, not per model, because the tools are what break.", "expect": [], "band": "strong", "source": "real-world", "note": "eval design"},
    {"id": "clean-rw2-012", "text": "The queue depth alarm fires at 10k because that's where consumers fall behind for good.", "expect": [], "band": "strong", "source": "real-world", "note": "alerting threshold"},
    {"id": "clean-rw2-013", "text": "Prefer a boring database you can operate over an exciting one you can't.", "expect": [], "band": "strong", "source": "real-world", "note": "ops taste"},
    {"id": "clean-rw2-014", "text": "We gate agent write access behind a human approval step for anything touching billing.", "expect": [], "band": "strong", "source": "real-world", "note": "authority boundary"},
    {"id": "clean-rw2-015", "text": "The retro found no single cause; three small gaps lined up to let the outage through.", "expect": [], "band": "strong", "source": "real-world", "note": "swiss-cheese finding"},
    {"id": "clean-rw2-016", "text": "Feature flags default off in prod and on in staging so the blast radius stays small.", "expect": [], "band": "strong", "source": "real-world", "note": "flag policy"},
    {"id": "clean-rw2-017", "text": "We leverage read replicas for reporting so analytics never blocks checkout writes.", "expect": [], "band": "strong", "source": "real-world", "note": "technical leverage, silent"},
    {"id": "clean-rw2-018", "text": "Robust retries here means bounded attempts, jitter, and a dead-letter queue for the rest.", "expect": [], "band": "strong", "source": "real-world", "note": "standalone robust, silent"},
    {"id": "clean-rw2-019", "text": "Very large payloads bypass the cache and stream straight from object storage.", "expect": [], "allow": ["intensifier_degree"], "band": "strong", "source": "real-world", "note": "legit degree word"},
    {"id": "clean-rw2-020", "text": "The token refresh races when two tabs post within the same second; we added a lock.", "expect": [], "band": "strong", "source": "real-world", "note": "concrete race"},
    {"id": "clean-rw2-021", "text": "Write the runbook before the launch, not after the first 3am page.", "expect": [], "band": "strong", "source": "real-world", "note": "ops advice"},
    {"id": "clean-rw2-022", "text": "The model picks the wrong tool when two tools share a verb in their description.", "expect": [], "band": "strong", "source": "real-world", "note": "tool naming lesson"},
    {"id": "clean-rw2-023", "text": "Keep the schema migration and the code that needs it in separate deploys.", "expect": [], "band": "strong", "source": "real-world", "note": "deploy ordering"},
    {"id": "clean-rw2-024", "text": "Cache invalidation here is a version bump on the key, not a delete-and-hope.", "expect": [], "band": "strong", "source": "real-world", "note": "cache strategy"},
    {"id": "clean-rw2-025", "text": "We keep the prompt in the repo and review changes to it like any other code.", "expect": [], "band": "strong", "source": "real-world", "note": "prompt as code"},
    {"id": "clean-rw2-026", "text": "The p95 target is 200ms; anything slower routes to the degraded read path.", "expect": [], "band": "strong", "source": "real-world", "note": "SLO with fallback"},
]

OC = [
    {"id": "oc-rw2-candor-001", "text": "Let's be honest — your microservices are a distributed monolith with extra billing.", "expect": ["candor"], "band": "weak", "source": "real-world", "note": "hot take rewrite"},
    {"id": "oc-rw2-candor-002", "text": "Here's the thing: most 'AI strategies' are a vendor logo on a slide.", "expect": ["candor"], "band": "weak", "source": "real-world", "note": "edgy opener"},
    {"id": "oc-rw2-stakes-001", "text": "In today's world, shipping without tracing is flying blind at night.", "expect": ["stakes"], "band": "fail", "source": "real-world", "note": "manufactured stakes rewrite"},
    {"id": "oc-rw2-emdash-001", "text": "Fast — cheap — good — pick none, apparently.", "expect": ["emdash"], "band": "weak", "source": "real-world", "note": "theatrics"},
    {"id": "oc-rw2-binary-001", "text": "The problem isn't the model. It's your context window.", "expect": ["binarycontrast"], "band": "weak", "source": "real-world", "note": "reveal cadence"},
    {"id": "oc-rw2-neglist-001", "text": "It wasn't the DB. It wasn't the cache. It was the load balancer all along.", "expect": ["neglisting"], "band": "weak", "source": "real-world", "note": "staccato negative listing"},
    {"id": "oc-rw2-transform-001", "text": "Toil becomes automation. Automation becomes leverage.", "expect": ["transformchain"], "band": "weak", "source": "real-world", "note": "false momentum"},
    {"id": "oc-rw2-correct-001", "text": "You've been told more tests mean fewer bugs. Here's the truth: coverage lies.", "expect": ["correctivereveal"], "band": "weak", "source": "real-world", "note": "contrarian posture"},
    {"id": "oc-rw2-force-001", "text": "You can't have reliability without observability. You can't have one without the other.", "expect": ["forcedcohesion"], "band": "weak", "source": "real-world", "note": "manufactured profundity"},
    {"id": "oc-rw2-throat-001", "text": "Let me be clear: your uptime number is marketing, not reliability.", "expect": ["throatclear"], "band": "weak", "source": "real-world", "note": "confide-then-jab"},
    {"id": "oc-rw2-emp-001", "text": "Truth be told this framework is an absolute game-changer.", "expect": ["candor", "empower"], "band": "fail", "source": "real-world", "note": "candor + buzzword combo"},
    {"id": "oc-rw2-reveal-001", "text": "Everyone says Kubernetes is the answer. They're wrong for teams under ten.", "expect": ["correctivereveal"], "band": "weak", "source": "real-world", "note": "everyone-says posture"},
    {"id": "oc-rw2-intens-001", "text": "I'll be honest this is a genuinely game-changing abstraction.", "expect": ["candor", "empower", "intensifier_filler"], "band": "fail", "source": "real-world", "note": "triple over-correction"},
    {"id": "oc-rw2-cta-001", "text": "Buckle up — this pattern will change how you think about queues.", "expect": ["calltoaction"], "band": "weak", "source": "real-world", "note": "hype cta"},
]


def _check(rows, kind):
    bad = []
    for r in rows:
        types = {h["type"] for h in flag(r["text"])}
        exp = set(r.get("expect", []))
        allow = set(r.get("allow", []))
        if kind in ("slop", "oc"):
            if exp and not exp.issubset(types):
                bad.append((r["id"], sorted(exp), sorted(types), r["text"]))
            elif not exp and not types:
                bad.append((r["id"], ["*"], sorted(types), r["text"]))
        else:
            badhits = types - allow
            if badhits:
                bad.append((r["id"], [], sorted(badhits), r["text"]))
    return bad


def _append(path: Path, rows: list[dict]) -> int:
    existing = set()
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                existing.add(json.loads(line)["id"])
    added = 0
    with path.open("a", encoding="utf-8") as fh:
        for r in rows:
            if r["id"] in existing:
                continue
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            added += 1
    return added


def main() -> int:
    problems = False
    for name, rows, kind in (("slop", SLOP, "slop"), ("clean", CLEAN, "clean"), ("oc", OC, "oc")):
        fails = _check(rows, kind)
        if fails:
            problems = True
            print(f"{name}: {len(fails)} FAIL")
            for f in fails:
                print("  ", f)
        else:
            print(f"{name}: all {len(rows)} OK")
    if problems:
        return 1
    n_s = _append(ROOT / "tests/corpus/slop.jsonl", SLOP)
    n_c = _append(ROOT / "tests/corpus/clean.jsonl", CLEAN)
    n_o = _append(ROOT / "tests/corpus/overcorrection.jsonl", OC)
    print(f"appended: slop+{n_s} clean+{n_c} oc+{n_o}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
