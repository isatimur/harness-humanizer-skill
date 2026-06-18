#!/usr/bin/env python3
"""Render the canonical skill into every AI tool's native format.

SINGLE SOURCE OF TRUTH: `SKILL.md` + `references/{rubric,guardrails,examples}.md`.
This script reads them and renders one self-contained adapter per target tool, so
the skill can be dropped into Cursor, GitHub Copilot, Codex/Amp (AGENTS.md),
Gemini, Windsurf, or pasted into any chatbot — all from the same source. Edit the
source once, run this, and every adapter regenerates identically.

Zero dependencies (stdlib only), like the rest of the project.

Usage:
    python3 scripts/build_adapters.py            # (re)generate adapters/
    python3 scripts/build_adapters.py --check    # CI: fail if adapters drifted
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
REPO = "https://github.com/isatimur/harness-humanizer-skill"

GENERATED_NOTE = (
    "<!-- GENERATED from SKILL.md + references/ by scripts/build_adapters.py. "
    "Do not edit by hand; edit the source and regenerate. -->"
)


def _read(*parts):
    with open(os.path.join(_ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def _split_frontmatter(md):
    """Return (frontmatter_text, body) for a `---`-fenced markdown file."""
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S)
    if not m:
        return "", md
    return m.group(1), m.group(2).lstrip("\n")


def _description(frontmatter):
    """Collapse the folded YAML `description:` scalar into one line."""
    lines = frontmatter.splitlines()
    out, capturing = [], False
    for ln in lines:
        if ln.startswith("description:"):
            capturing = True
            rest = ln.split(":", 1)[1].strip()
            if rest and rest not in (">-", ">", "|", "|-"):
                out.append(rest)
            continue
        if capturing:
            if re.match(r"^\S", ln):  # next top-level key → stop
                break
            out.append(ln.strip())
    return re.sub(r"\s+", " ", " ".join(out)).strip()


def _strip_h1(md):
    """Drop a leading `# Title` line so inlined sections nest cleanly."""
    return re.sub(r"^#\s+.*\n+", "", md, count=1).rstrip()


def build_core(include_examples=False):
    """Assemble the self-contained skill body shared by every adapter."""
    fm, body = _split_frontmatter(_read("SKILL.md"))
    # Drop the source-only "## References" section (those files won't travel with
    # a single copied adapter); we inline the essentials instead.
    skill_body = re.split(r"\n##\s+References\b", body)[0].rstrip()

    rubric = _strip_h1(_read("references", "rubric.md"))
    guardrails = _strip_h1(_read("references", "guardrails.md"))

    parts = [
        skill_body,
        "\n\n---\n\n## Humanness rubric (inlined)\n\n" + rubric,
        "\n\n---\n\n## Guardrails (inlined)\n\n" + guardrails,
    ]
    if include_examples:
        examples = _strip_h1(_read("references", "examples.md"))
        parts.append("\n\n---\n\n## Examples (inlined)\n\n" + examples)
    parts.append(
        "\n\n---\n\n*Optional tooling — a zero-dependency deterministic "
        "pre-flagger (`flag_slop.py`), the full slop catalogue, and the test "
        f"corpus live in the repo: {REPO}*\n"
    )
    return "".join(parts), _description(fm)


# --- per-format renderers ---------------------------------------------------

def _r_mdc(core, desc, note):
    # Cursor rules (.mdc): YAML frontmatter, opt-in (alwaysApply: false).
    return (f"---\ndescription: {desc}\nglobs:\nalwaysApply: false\n---\n"
            f"{GENERATED_NOTE}\n\n> **Install:** {note}\n\n{core}")


def _r_copilot(core, desc, note):
    # GitHub Copilot custom instructions (.instructions.md).
    return (f"---\napplyTo: \"**\"\ndescription: {desc}\n---\n"
            f"{GENERATED_NOTE}\n\n> **Install:** {note}\n\n{core}")


def _r_agents(core, desc, note):
    # AGENTS.md — the cross-tool standard (Codex, Amp, Jules, and more).
    return (f"{GENERATED_NOTE}\n\n> **Install:** {note}\n>\n> {desc}\n\n{core}")


def _r_markdown(core, desc, note):
    # Plain markdown rule (Gemini, Windsurf, generic).
    return (f"{GENERATED_NOTE}\n\n> **Install:** {note}\n>\n> {desc}\n\n{core}")


def _r_prompt(core, desc, note):
    header = (
        "# Harness Humanizer — paste-anywhere prompt\n\n"
        f"{GENERATED_NOTE}\n\n"
        "Copy everything below the line into any AI chat (ChatGPT, Claude, "
        "Gemini, etc.), then paste the text you want de-slopped underneath it. "
        "No install required.\n\n"
        "---\n\n"
        "You are an editor running the **Harness Humanizer** loop. Apply the "
        "rules, loop, rubric, and guardrails below to the prose I give you. "
        "Report your changes and flags — do not silently rewrite.\n\n"
    )
    return header + core


RENDERERS = {
    "mdc": _r_mdc, "copilot": _r_copilot, "agents": _r_agents,
    "markdown": _r_markdown, "prompt": _r_prompt,
}

# Declarative target manifest. Add a harness = add one entry.
TARGETS = [
    {"id": "cursor", "fmt": "mdc",
     "path": "adapters/cursor/harness-humanizer.mdc",
     "note": "place in `.cursor/rules/` in your project."},
    {"id": "copilot", "fmt": "copilot",
     "path": "adapters/copilot/harness-humanizer.instructions.md",
     "note": "place in `.github/instructions/` in your repo."},
    {"id": "agents", "fmt": "agents",
     "path": "adapters/AGENTS.md",
     "note": "drop `AGENTS.md` at your repo root — Codex, Amp, Jules and many "
             "agents read it (also covers Pi, Hermes, OpenCLAW and other "
             "AGENTS.md-aware tools)."},
    {"id": "gemini", "fmt": "markdown",
     "path": "adapters/gemini/GEMINI.md",
     "note": "place `GEMINI.md` at your repo root or in `~/.gemini/`."},
    {"id": "windsurf", "fmt": "markdown",
     "path": "adapters/windsurf/harness-humanizer.md",
     "note": "place in `.windsurf/rules/` in your project."},
    {"id": "prompt", "fmt": "prompt",
     "path": "adapters/PROMPT.md",
     "note": "copy-paste into any chatbot."},
]


def render_all():
    """Return {path: content} for every target."""
    core, desc = build_core(include_examples=False)
    core_full, _ = build_core(include_examples=True)
    out = {}
    for t in TARGETS:
        body = core_full if t["fmt"] == "prompt" else core
        content = RENDERERS[t["fmt"]](body, desc, t["note"])
        if not content.endswith("\n"):
            content += "\n"
        out[t["path"]] = content
    return out


def write_all(rendered):
    for path, content in rendered.items():
        full = os.path.join(_ROOT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"  wrote {path}")


def check_all(rendered):
    drift = []
    for path, content in rendered.items():
        full = os.path.join(_ROOT, path)
        if not os.path.exists(full):
            drift.append((path, "missing"))
            continue
        with open(full, encoding="utf-8") as fh:
            if fh.read() != content:
                drift.append((path, "out of date"))
    return drift


def main(argv):
    rendered = render_all()
    if "--check" in argv:
        drift = check_all(rendered)
        if drift:
            print("Adapters are out of sync with source:")
            for path, why in drift:
                print(f"  {path}: {why}")
            print("\nRun: python3 scripts/build_adapters.py")
            return 1
        print(f"adapters in sync ({len(rendered)} targets) — OK")
        return 0
    print(f"Generating {len(rendered)} adapters from SKILL.md + references/ ...")
    write_all(rendered)
    print("done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
