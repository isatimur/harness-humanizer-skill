#!/usr/bin/env python3
"""Append real-world corpus samples after validating each line fires as expected."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from flag_slop import flag  # noqa: E402

SLOP = [
    {"id": "slop-real-hedge-001", "text": "It's important to note that most teams ship without a staging environment.", "expect": ["hedge"], "band": "weak", "source": "real-world", "note": "repo README paste: empty hedge stem"},
    {"id": "slop-real-hedge-002", "text": "Needless to say, reliability is critical for production workloads.", "expect": ["hedge"], "band": "fail", "source": "real-world", "note": "product landing page"},
    {"id": "slop-real-stakes-001", "text": "In today's digital landscape, brands need authentic connection more than ever.", "expect": ["stakes"], "band": "fail", "source": "real-world", "note": "marketing blog"},
    {"id": "slop-real-stakes-002", "text": "Now more than ever, engineering organizations must modernize their toolchains.", "expect": ["stakes"], "band": "fail", "source": "real-world", "note": "vendor whitepaper"},
    {"id": "slop-real-list-001", "text": "There are many ways to improve developer productivity in 2025.", "expect": ["listicle"], "band": "weak", "source": "real-world", "note": "Substack post opener"},
    {"id": "slop-real-list-002", "text": "Let's take a look at some of the key considerations for multi-tenant SaaS.", "expect": ["listicle"], "band": "weak", "source": "real-world", "note": "engineering blog intro"},
    {"id": "slop-real-trans-001", "text": "Additionally, the architecture supports horizontal growth over time.", "expect": ["transition"], "band": "weak", "source": "real-world", "note": "architecture doc filler paragraph start"},
    {"id": "slop-real-trans-002", "text": "In addition the platform offers enterprise-grade authentication options.", "expect": ["transition"], "band": "weak", "source": "real-world", "note": "compliance flyer"},
    {"id": "slop-real-candor-001", "text": "Let's be real: most roadmaps still begin with a slide, not a user.", "expect": ["candor"], "band": "weak", "source": "real-world", "note": "product tweet"},
    {"id": "slop-real-rhetq-001", "text": "What if I told you your on-call pain is mostly a design failure?", "expect": ["rhetq"], "band": "weak", "source": "real-world", "note": "LinkedIn post"},
    {"id": "slop-real-delve-001", "text": "When it comes to observability, navigating the complex landscape is hard.", "expect": ["delve"], "band": "fail", "source": "real-world", "note": "vendor webinar copy"},
    {"id": "slop-real-delve-002", "text": "This acquisition is a testament to the team's vision and hard work.", "expect": ["delve"], "band": "weak", "source": "real-world", "note": "press release"},
    {"id": "slop-real-weasel-001", "text": "Teams rely on a host of third-party services to ship features faster.", "expect": ["weaselquant"], "band": "moderate", "source": "real-world", "note": "SaaS home page"},
    {"id": "slop-real-weasel-002", "text": "We reviewed a broad range of alternatives before settling on Postgres.", "expect": ["weaselquant"], "band": "moderate", "source": "real-world", "note": "ADR draft"},
    {"id": "slop-real-negpar-001", "text": "This isn't just about tools, it's about culture change at every layer.", "expect": ["negparallel"], "band": "weak", "source": "real-world", "note": "change-management deck"},
    {"id": "slop-real-concl-001", "text": "The key takeaway is that observability pays for itself.", "expect": ["conclusion"], "band": "weak", "source": "real-world", "note": "conference recap"},
    {"id": "slop-real-concl-002", "text": "To sum up the migration reduced incident volume across services.", "expect": ["conclusion"], "band": "weak", "source": "real-world", "note": "postmortem closing"},
    {"id": "slop-real-emp-001", "text": "A seamless, world-class experience that supercharges your workflow.", "expect": ["empower"], "band": "fail", "source": "real-world", "note": "app store blurb"},
    {"id": "slop-real-emp-002", "text": "Our AI-powered copilot empowers developers with next-generation insights.", "expect": ["empower"], "band": "fail", "source": "real-world", "note": "startup homepage hero"},
    {"id": "slop-real-tri-001", "text": "Deliver a powerful, intuitive, and seamless editor for the whole team.", "expect": ["triadic"], "band": "moderate", "source": "real-world", "note": "product one-pager"},
    {"id": "slop-real-cta-001", "text": "Dive right in and start building smarter agents today.", "expect": ["calltoaction"], "band": "weak", "source": "real-world", "note": "docs getting-started"},
    {"id": "slop-real-cta-002", "text": "Stay tuned for more updates as we roll features out.", "expect": ["calltoaction"], "band": "weak", "source": "real-world", "note": "changelog teaser"},
    {"id": "slop-real-emdash-001", "text": "Ship faster — break less — sleep more — hopefully.", "expect": ["emdash"], "band": "moderate", "source": "real-world", "note": "conference talk slide"},
    {"id": "slop-real-throat-001", "text": "It turns out that most latency sits in the network round-trip, not the model.", "expect": ["throatclear"], "band": "weak", "source": "real-world", "note": "perf post"},
    {"id": "slop-real-emph-001", "text": "Here's why that matters when your queue fills overnight.", "expect": ["emphasis_crutch"], "band": "weak", "source": "real-world", "note": "ops newsletter"},
    {"id": "slop-real-meta-001", "text": "In this section, we'll explore the migration path for legacy jobs.", "expect": ["metacommentary"], "band": "weak", "source": "real-world", "note": "tutorial draft"},
    {"id": "slop-real-biz-001", "text": "We should take a step back and align on low-hanging fruit first.", "expect": ["bizjargon"], "band": "weak", "source": "real-world", "note": "standup transcript cleaned"},
    {"id": "slop-real-biz-002", "text": "Let's double down and lean into platform thinking this quarter.", "expect": ["bizjargon"], "band": "weak", "source": "real-world", "note": "all-hands notes"},
    {"id": "slop-real-asstant-001", "text": "I'm happy to help draft a conceptual overview of the system.", "expect": ["assistantvoice"], "band": "fail", "source": "real-world", "note": "ChatGPT default courtesy"},
    {"id": "slop-real-asstant-002", "text": "As an AI language model I can't access your internal wiki.", "expect": ["assistantvoice"], "band": "fail", "source": "real-world", "note": "assistant boilerplate"},
    {"id": "slop-real-copula-001", "text": "The redesign serves as a testament to customer-obsessed engineering.", "expect": ["copula"], "band": "weak", "source": "real-world", "note": "case study"},
    {"id": "slop-real-hedge2-001", "text": "It could potentially be related to a race in the retry loop.", "expect": ["hedgestack"], "band": "weak", "source": "real-world", "note": "incident channel"},
    {"id": "slop-real-notonly-001", "text": "Not only does the cache reduce load, but also it simplifies failover paths.", "expect": ["notonly"], "band": "moderate", "source": "real-world", "note": "design review"},
    {"id": "slop-real-intens-001", "text": "This is frankly a genuinely powerful abstraction for routing.", "expect": ["intensifier_filler"], "band": "moderate", "source": "real-world", "note": "RFC comment"},
    {"id": "slop-real-fill-001", "text": "At the end of the day teams just need a score they trust.", "expect": ["hedge"], "band": "weak", "source": "real-world", "note": "product interview quote cleaned"},
    {"id": "slop-real-fill-002", "text": "As we all know, distributed systems fail in surprising ways.", "expect": ["hedge"], "band": "weak", "source": "real-world", "note": "talk intro"},
    {"id": "slop-real-delve-003", "text": "Let's delve into why the deploy pipeline stalled last night.", "expect": ["delve"], "band": "weak", "source": "real-world", "note": "ops notes"},
    {"id": "slop-real-stakes-003", "text": "In today's fast-paced world incident response must be proactive.", "expect": ["stakes"], "band": "fail", "source": "real-world", "note": "security vendor email"},
    {"id": "slop-real-list-003", "text": "Here are several key factors that drive up agent failure rates.", "expect": ["listicle"], "band": "weak", "source": "real-world", "note": "agent eval writeup intro"},
    {"id": "slop-real-emdash-002", "text": "It was simple — elegant — and wrong — as production proved.", "expect": ["emdash"], "band": "moderate", "source": "real-world", "note": "postmortem narration"},
]

CLEAN = [
    {"id": "clean-real-001", "text": "p95 latency fell from 420ms to 110ms after we moved the hot path off the shared CPU pool.", "expect": [], "band": "strong", "source": "real-world", "note": "incident writeup"},
    {"id": "clean-real-002", "text": "We rewrote the webhook consumer in Rust because the Python worker could not hold 8k connections.", "expect": [], "band": "strong", "source": "real-world", "note": "migration ADR"},
    {"id": "clean-real-003", "text": "Caching improves performance for many applications.", "expect": [], "band": "strong", "source": "examples.md", "note": "fidelity-safe after rewrite of flagship demo"},
    {"id": "clean-real-004", "text": "Roll out behind a feature flag, watch error rate for 24 hours, then delete the old code path.", "expect": [], "band": "strong", "source": "real-world", "note": "release checklist"},
    {"id": "clean-real-005", "text": "The retry budget is three attempts with exponential backoff, capped at 30 seconds.", "expect": [], "band": "strong", "source": "real-world", "note": "runbook"},
    {"id": "clean-real-006", "text": "If the index is missing, Postgres plans a sequential scan; add it before the cutover.", "expect": [], "band": "strong", "source": "real-world", "note": "on-call note"},
    {"id": "clean-real-007", "text": "Ship the schema first; dual-write for a week; then switch readers.", "expect": [], "band": "strong", "source": "real-world", "note": "migration steps"},
    {"id": "clean-real-008", "text": "The model is fine. The tool descriptions are wrong, so it calls the wrong function.", "expect": [], "band": "strong", "source": "real-world", "note": "agent debugging log"},
    {"id": "clean-real-009", "text": "We stopped auto-merging agent PRs after one bad path deleted a production table.", "expect": [], "band": "strong", "source": "real-world", "note": "policy change rationale"},
    {"id": "clean-real-010", "text": "Trade-off: stronger types slow early iteration and catch the bugs we actually ship.", "expect": [], "band": "strong", "source": "real-world", "note": "team standard"},
    {"id": "clean-real-011", "text": "Green tests on the PR mean nothing if the suite never hits the failure mode.", "expect": [], "band": "strong", "source": "real-world", "note": "testing manifesto line"},
    {"id": "clean-real-012", "text": "Prefer a smaller public API even when the inner module could expose more helpers.", "expect": [], "band": "strong", "source": "real-world", "note": "API review comment"},
    {"id": "clean-real-013", "text": "We kept Kafka for fan-out and moved the ledger to Postgres for serializable inserts.", "expect": [], "band": "strong", "source": "real-world", "note": "architecture summary"},
    {"id": "clean-real-014", "text": "Delete the feature if two quarters pass without a paying customer using it.", "expect": [], "band": "strong", "source": "real-world", "note": "product rule"},
    {"id": "clean-real-015", "text": "The bug only appears when two clients share an app password and rotate tokens at the same second.", "expect": [], "band": "strong", "source": "real-world", "note": "repro note"},
    {"id": "clean-real-016", "text": "We measure success as tickets closed without reopening, not lines of agent output.", "expect": [], "band": "strong", "source": "real-world", "note": "ops KPI"},
    {"id": "clean-real-017", "text": "Typecheck passed; the runtime still threw because openapi types lagged the server.", "expect": [], "band": "strong", "source": "real-world", "note": "CI false confidence"},
    {"id": "clean-real-018", "text": "Put the secret in the vault; never in the issue description, even for a repro.", "expect": [], "band": "strong", "source": "real-world", "note": "security hygiene"},
    {"id": "clean-real-019", "text": "Very few requests hit this endpoint; optimise the path that serves homepage traffic first.", "expect": [], "allow": ["intensifier_degree"], "band": "strong", "source": "real-world", "note": "legit degree use"},
    {"id": "clean-real-020", "text": "We leverage connection pooling to keep p99 under 200ms during checkout peaks.", "expect": [], "band": "strong", "source": "real-world", "note": "technical leverage silent"},
    {"id": "clean-real-021", "text": "Documentation is essential in software projects.", "expect": [], "band": "strong", "source": "examples.md", "note": "fidelity-safe docs after"},
    {"id": "clean-real-022", "text": "Testing helps ensure quality in development.", "expect": [], "band": "strong", "source": "examples.md", "note": "fidelity-safe testing after"},
    {"id": "clean-real-023", "text": "The platform runs your existing CI config and caches build artifacts across branches.", "expect": [], "band": "strong", "source": "examples.md", "note": "fidelity-safe platform after"},
    {"id": "clean-real-024", "text": "The library reads and writes JSON, CSV, and Parquet.", "expect": [], "band": "strong", "source": "examples.md", "note": "fidelity-safe formats after"},
    {"id": "clean-real-025", "text": "Caching strategies split three ways: cache-aside, write-through, and write-behind.", "expect": [], "band": "strong", "source": "examples.md", "note": "fidelity-safe delve-after with names in source"},
    {"id": "clean-real-026", "text": "Picking a queue means trading off throughput, ordering, and redelivery — most brokers let you optimize two of the three, not all.", "expect": [], "band": "strong", "source": "examples.md", "note": "case A after"},
]

OC = [
    {"id": "oc-real-candor-001", "text": "Let's be honest — most strategy decks are cosplay for people who won't ship.", "expect": ["candor"], "band": "weak", "source": "real-world", "note": "over-corrected rewrite of strategy advice"},
    {"id": "oc-real-candor-002", "text": "Here's the thing: if your agents have no evals, you don't have a product.", "expect": ["candor"], "band": "weak", "source": "real-world", "note": "Twitter hot take rewrites"},
    {"id": "oc-real-stakes-001", "text": "In today's world undocumented systems aren't just debt — they're risk.", "expect": ["stakes"], "band": "fail", "source": "real-world", "note": "over-corrected docs pitch"},
    {"id": "oc-real-emdash-001", "text": "Write less — ship more — pretend the rest is process — then wonder.", "expect": ["emdash"], "band": "weak", "source": "real-world", "note": "theatrical rewrite"},
    {"id": "oc-real-binary-001", "text": "The answer isn't more dashboards. It's fewer misleading ones.", "expect": ["binarycontrast"], "band": "weak", "source": "real-world", "note": "framework slide"},
    {"id": "oc-real-neglist-001", "text": "It wasn't product. It wasn't design. It was missing ownership on call.", "expect": ["neglisting"], "band": "weak", "source": "real-world", "note": "retro theatre"},
    {"id": "oc-real-transform-001", "text": "Debt becomes drag. Drag becomes attrition.", "expect": ["transformchain"], "band": "weak", "source": "real-world", "note": "pitch deck rhetoric"},
    {"id": "oc-real-correct-001", "text": "You've been told AI will replace juniors. Here's the truth: it replaces unclear work.", "expect": ["correctivereveal"], "band": "weak", "source": "real-world", "note": "newsletter spat"},
    {"id": "oc-real-force-001", "text": "You can't have velocity without quality. You can't have one without the other.", "expect": ["forcedcohesion"], "band": "weak", "source": "real-world", "note": "manager pep talk"},
    {"id": "oc-real-emp-001", "text": "Truth be told this platform is a real game-changer for delivery.", "expect": ["candor", "empower"], "band": "fail", "source": "real-world", "note": "sales rewrite of a technical note"},
    {"id": "oc-real-reveal-001", "text": "Everyone says LLMs write code. They're wrong about what that code costs to own.", "expect": ["correctivereveal"], "band": "weak", "source": "real-world", "note": "contrarian opener"},
    {"id": "oc-real-throat-001", "text": "Let me be clear: hot takes are not a reliability strategy.", "expect": ["throatclear"], "band": "weak", "source": "real-world", "note": "overdone confide rewrite"},
    {"id": "oc-real-intens-001", "text": "I'll be honest this is a truly revolutionary way to ship Markdown.", "expect": ["candor", "intensifier_filler"], "band": "fail", "source": "real-world", "note": "fake first person + filler"},
    {"id": "oc-real-cta-001", "text": "Buckle up — your old roadmap is already obsolete.", "expect": ["calltoaction"], "band": "weak", "source": "real-world", "note": "launch post voice"},
    {"id": "oc-real-candor-003", "text": "Let's be real, most humanizers just swap in a different costume of slop.", "expect": ["candor"], "band": "weak", "source": "real-world", "note": "meta critique that is itself edgy-slop"},
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
    existing_ids = set()
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                existing_ids.add(json.loads(line)["id"])
    added = 0
    with path.open("a", encoding="utf-8") as fh:
        for r in rows:
            if r["id"] in existing_ids:
                continue
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            added += 1
    return added


def main() -> int:
    problems = []
    for name, rows, kind in (
        ("slop", SLOP, "slop"),
        ("clean", CLEAN, "clean"),
        ("oc", OC, "oc"),
    ):
        fails = _check(rows, kind)
        if fails:
            problems.append((name, fails))
            print(f"{name}: {len(fails)} FAIL")
            for f in fails[:12]:
                print(" ", f)
        else:
            print(f"{name}: all {len(rows)} OK")

    if problems:
        return 1

    # also update clean-003 (old over-spec after) if still present
    clean_path = ROOT / "tests/corpus/clean.jsonl"
    lines = clean_path.read_text().splitlines()
    fixed = []
    for line in lines:
        rec = json.loads(line)
        if rec["id"] == "clean-003" and "microseconds" in rec["text"]:
            rec["text"] = "Caching improves performance for many applications."
            rec["note"] = "fidelity-safe after rewrite of flagship demo"
            rec["source"] = "examples.md"
            fixed.append(json.dumps(rec, ensure_ascii=False))
        else:
            fixed.append(line)
    clean_path.write_text("\n".join(fixed) + "\n")

    n_s = _append(ROOT / "tests/corpus/slop.jsonl", SLOP)
    n_c = _append(clean_path, CLEAN)
    n_o = _append(ROOT / "tests/corpus/overcorrection.jsonl", OC)
    print(f"appended: slop+{n_s} clean+{n_c} oc+{n_o}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
