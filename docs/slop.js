/* de-slop — in-browser AI-slop scorer.
 *
 * A faithful JS port of scripts/flag_slop.py: same rule TYPES and same WEIGHTS
 * (tests/check_js_parity.py gates the inventory so this never drifts from the
 * Python detector). Minor regex-engine differences are tolerated on edge cases —
 * this is the shareable demo, not the gated detector. Like the Python version it
 * measures SURFACE TELLS ONLY, never claim presence: a clean score is not a
 * promise of good writing, and hollowness is invisible to it.
 *
 * Zero dependencies. Runs entirely client-side — your text never leaves the page.
 */
(function (root) {
  "use strict";

  // Severity weights — MUST stay byte-identical to flag_slop.py `_WEIGHTS`.
  // PARITY:WEIGHTS-START
  var WEIGHTS = {
    listicle: 20, stakes: 20, candor: 18, rhetq: 18,
    assistantvoice: 18, calltoaction: 16, delve: 16, metacommentary: 16,
    correctivereveal: 16, hedge: 15, throatclear: 15, conclusion: 14,
    emphasis_crutch: 14, transformchain: 14, emdash: 12, weaselquant: 12,
    negparallel: 12, binarycontrast: 12, neglisting: 12, forcedcohesion: 12,
    hedgestack: 12, copula: 10, transition: 10, notonly: 10,
    intensifier_filler: 10, empower: 8, triadic: 8, bizjargon: 8,
    intensifier_degree: 6
  };
  // PARITY:WEIGHTS-END

  var TRIAD = "(fast|reliable|scalable|secure|robust|powerful|flexible|" +
    "intuitive|seamless|efficient|innovative|modern)";

  // [type, human label, regex]. Mirrors flag_slop.py `_RULES`.
  var RULES = [
    ["hedge", "empty hedging stem",
      /\b(it'?s|it is) (worth noting|important to (note|remember|understand))\b|\b(that said|needless to say|as we all know|at the end of the day)\b/gi],
    ["listicle", "listicle stem with no point",
      /\b(there are (several|a number of|many) (key |important )?(factors|considerations|things|ways|reasons)|here are (a few|some|several)|let'?s (explore|dive into|take a look))\b/gi],
    ["transition", "dead transition",
      /^\s*(moreover|furthermore|in addition|additionally)\b,?/gim],
    ["stakes", "manufactured stakes",
      /\b(in today'?s (fast-paced |digital |modern )?(world|landscape|era)|now more than ever|more important than ever|the stakes have never been higher)\b/gi],
    ["candor", "performed candor",
      /\b(let'?s be honest|let'?s be real|here'?s the thing|truth be told|i'?ll be honest)\b/gi],
    ["rhetq", "rhetorical-question opener",
      /^\s*(what if i told you|ever wondered|have you ever)\b/gim],
    ["notonly", "not-only-but-also padding",
      /\bnot only\b.*\bbut also\b/gi],
    ["intensifier_filler", "filler intensifier adverb",
      /\b(truly|genuinely|honestly|literally|simply|basically|essentially|undoubtedly|certainly|definitely)\s+\w+/gi],
    ["intensifier_degree", "degree intensifier (often legit)",
      /\b(?:[Vv]ery|[Rr]eally|[Ee]xtremely|[Ii]ncredibly|[Qq]uite|[Rr]ather)\s+(?!the\b|a\b|an\b|of\b|to\b|in\b|on\b|much\b|many\b|few\b|little\b|more\b)[a-z]\w+/g],
    ["weaselquant", "vague quantifier",
      /\b(a (wide|broad) (variety|range|array) of|a number of|numerous|countless|myriad|a host of|a plethora of|various (different )?)\b/gi],
    ["negparallel", "negative-parallel cadence",
      /\b(it'?s not (just|merely|only)\b.*\bit'?s\b|this isn'?t (just )?about\b.*\bit'?s about\b)/gi],
    ["delve", "LLM-lexicon filler",
      /\b(delv(e|es|ing)|tapestry|a testament to|(in )?the realm of|navigat(e|es|ing) the (complex|intricat|nuanc)|at the end of the day|when it comes to)\b/gi],
    ["conclusion", "wrap-up scaffolding",
      /^\s*(in conclusion|to sum up|in summary|to summarize|all in all)\b|\bthe key takeaway( here)? is\b/gim],
    ["triadic", "rule-of-three buzzword triplet",
      new RegExp("\\b" + TRIAD + ",?\\s+" + TRIAD + ",?\\s+and\\s+" + TRIAD + "\\b", "gi")],
    ["calltoaction", "throat-clearing call to action",
      /\b(let'?s dive (in|right in)|dive right in|buckle up|stay tuned|without further ado|let'?s get started|read on)\b/gi],
    ["throatclear", "throat-clearing opener",
      /\b(the uncomfortable truth is|it turns out(,| that)|let me be clear|the real (problem|question|issue|reason) (is|here)|can we talk about|i'?m going to be honest|i'?ll be honest with you)\b/gi],
    ["emphasis_crutch", "emphasis crutch",
      /\b(let that sink in|make no mistake|this matters because|here'?s why (that|this) matters)\b/gi],
    ["metacommentary", "meta-commentary scaffolding",
      /\b(plot twist|spoiler( alert)?|let me walk you through|in this (section|post|article|chapter)[, ]+(we|i)'?ll|as we'?ll see|i want to explore|you already know this,? but)\b/gi],
    ["binarycontrast", "binary-contrast cadence",
      /\b(the (answer|question|problem|issue) (isn'?t|is not)\b.*?\bit'?s\b|isn'?t the problem[.,]\s+\w+\s+is\b|it'?s not (that )?\w+[.,]\s+it'?s that\b)/gi],
    ["neglisting", "negative listing",
      /\bit wasn'?t\b.*?\bit wasn'?t\b.*?\bit was\b/gi],
    ["bizjargon", "business-jargon idiom",
      /\b(circle back|double down|move the needle|low-hanging fruit|boil the ocean|take a step back|on the same page|moving forward|lean into|deep dive)\b/gi],
    ["assistantvoice", "assistant voice / sycophancy",
      /\b(great question|good question|i'?d be happy to|i'?m happy to|happy to help|glad you asked|i'?d love to help|as an ai( language model)?|i hope (this (email|message) )?finds you well|i hope (you'?re|all is)( doing)? well)\b/gi],
    ["transformchain", "transformation chain",
      /\b(\w+) becomes? (\w+)[.,]\s+\2 becomes?\b/gi],
    ["correctivereveal", "corrective reveal / contrarian posturing",
      /\b(you'?ve been told|here'?s the (actual )?truth|(everyone|they all) says?\b.{0,40}\bthey'?re wrong)\b/gi],
    ["forcedcohesion", "forced cohesion",
      /\byou can'?t have one without the other\b/gi],
    ["copula", "copula avoidance / significance inflation",
      /\b(boasts|(serves|stands) as a (testament|reminder|symbol|cornerstone))\b/gi],
    ["hedgestack", "stacked hedges",
      /\b(might|may|could)\s+(possibly|potentially|perhaps)\b|\b(possibly|perhaps)\s+(might|could|may)\b/gi]
  ];

  var EMPOWER_MARKETING = /\b(empower(s|ing)?|seamless(ly)?|frictionless|turnkey|synerg(y|ies)|cutting-edge|bleeding-edge|state-of-the-art|best-in-class|world-class|game-?chang(er|ing)|supercharg(e|es|ing)|next-generation|paradigm shift)\b/gi;
  var EMPOWER_RIDER = /\b(leverag(e|es|ing|ed)|robust|unlock(s|ing|ed)?|harness(es|ing)?|elevate(s|d)?|streamlin(e|es|ed|ing))\b/gi;

  function splitLines(text) { return text.split(/\r?\n/); }
  function splitSentences(line) { return line.split(/(?<=[.!?])\s+/); }

  function matchAll(line, re) {
    var out = [], m;
    re.lastIndex = 0;
    while ((m = re.exec(line)) !== null) {
      out.push(m[0].trim().slice(0, 120));
      if (m.index === re.lastIndex) re.lastIndex++; // guard zero-width
    }
    return out;
  }

  // Sentence-aware corporate-uplift, mirrors flag_slop._empower_hits.
  function empowerHits(line) {
    var hits = [];
    splitSentences(line).forEach(function (sent) {
      var marketing = matchAll(sent, EMPOWER_MARKETING);
      marketing.forEach(function (s) { hits.push({ type: "empower", pattern: "corporate-uplift buzzword", span: s }); });
      if (marketing.length) {
        matchAll(sent, EMPOWER_RIDER).forEach(function (s) {
          hits.push({ type: "empower", pattern: "corporate-uplift buzzword", span: s });
        });
      }
    });
    return hits;
  }

  function emdashHits(line) {
    var hits = [];
    splitSentences(line).forEach(function (sent) {
      if ((sent.match(/—/g) || []).length >= 2) {
        hits.push({ type: "emdash", pattern: "em-dash density (>=2 in a sentence)", span: sent.trim().slice(0, 120) });
      }
    });
    return hits;
  }

  function flag(text) {
    var hits = [];
    splitLines(text).forEach(function (line, i) {
      RULES.forEach(function (rule) {
        matchAll(line, rule[2]).forEach(function (span) {
          hits.push({ line: i + 1, type: rule[0], pattern: rule[1], span: span });
        });
      });
      empowerHits(line).forEach(function (h) { h.line = i + 1; hits.push(h); });
      emdashHits(line).forEach(function (h) { h.line = i + 1; hits.push(h); });
    });
    return hits;
  }

  function band(s) {
    if (s >= 80) return "strong";
    if (s >= 50) return "moderate";
    if (s >= 20) return "weak";
    return "fail";
  }

  // Mirror flag_slop._paragraphs scope rules (skip code fences/headings/quotes/lists).
  function paragraphs(text) {
    var lines = splitLines(text), out = [], para = [], start = null, inFence = false, skip = false;
    var SKIP_FIRST = /^\s*(#|>|[-*+]\s|\d+[.)]\s)/;
    function flush() { if (para.length && !skip) out.push({ start: start, lines: para.slice() }); para = []; start = null; skip = false; }
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      if (line.trim().indexOf("```") === 0) { inFence = !inFence; continue; }
      if (inFence) continue;
      if (/^\s*$/.test(line)) { flush(); continue; }
      if (!para.length) { start = i + 1; if (SKIP_FIRST.test(line)) { skip = true; } }
      if (skip) continue;
      para.push(line);
    }
    flush();
    return out;
  }

  function scoreParagraph(p) {
    var text = p.lines.join("\n");
    var hits = flag(text);
    hits.forEach(function (h) { h.line = p.start + h.line - 1; });
    var words = Math.max((text.match(/\b\w+\b/g) || []).length, 1);
    var raw = hits.reduce(function (a, h) { return a + (WEIGHTS[h.type] || 8); }, 0);
    var densityBonus = Math.min(20, (hits.length / words) * 100 * 4);
    var penalty = Math.min(100, raw + densityBonus);
    var slop = Math.max(0, Math.round(100 - penalty));
    return { lineStart: p.start, words: words, slopScore: slop, slopBand: band(slop), hits: hits };
  }

  function score(text) {
    var paras = paragraphs(text).map(scoreParagraph);
    var totalWords = paras.reduce(function (a, p) { return a + p.words; }, 0) || 1;
    var overall = paras.length
      ? Math.round(paras.reduce(function (a, p) { return a + p.slopScore * p.words; }, 0) / totalWords)
      : 100;
    var totalHits = paras.reduce(function (a, p) { return a + p.hits.length; }, 0);
    return { paragraphs: paras, overall: { slopScore: overall, slopBand: band(overall), paragraphCount: paras.length, totalHits: totalHits } };
  }

  root.HHSlop = { flag: flag, score: score, band: band, RULES: RULES, WEIGHTS: WEIGHTS };
})(typeof window !== "undefined" ? window : this);
