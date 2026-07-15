#!/usr/bin/env bash
set -euo pipefail

# Re-assert this repo's GitHub metadata (description, topics, homepage) from
# source control, so the listing never silently drifts from what the README
# promises. Idempotent: re-running it just re-sets the same values.
#
# Requires the GitHub CLI, authenticated: https://cli.github.com/
#   gh auth status
#
# Run from anywhere:
#   bash scripts/setup-github.sh

REPO="isatimur/de-slop"

# --- Description + homepage --------------------------------------------------
# Homepage is intentionally the old harness-humanizer-skill.vercel.app domain
# (see CHANGELOG 0.4.0 "Unchanged"); update it in the same change as any future domain move.
gh repo edit "$REPO" \
  --description "Portable Claude Code skill that de-slops AI prose — detect, rewrite to a real point of view, self-score, iterate. Fidelity-first; flags hollow spans instead of faking them." \
  --homepage "https://harness-humanizer-skill.vercel.app/"

# --- Topics (13, replaced exactly) -------------------------------------------
# `gh repo edit --add-topic` is additive only — it can never remove a stale
# topic. PUT the full names[] list instead, which genuinely replaces the set.
gh api -X PUT "repos/$REPO/topics" \
  -f "names[]=ai-writing" \
  -f "names[]=claude-code" \
  -f "names[]=claude-skill" \
  -f "names[]=de-slop" \
  -f "names[]=prose" \
  -f "names[]=writing-tools" \
  -f "names[]=agent-skills" \
  -f "names[]=ai-slop" \
  -f "names[]=anthropic-claude" \
  -f "names[]=cursor" \
  -f "names[]=developer-tools" \
  -f "names[]=humanizer" \
  -f "names[]=llm"

# --- Social Preview (manual, one-time) --------------------------------------
# gh has no API for the Social Preview image, so set it by hand once:
#   Settings → General → Social preview → Upload an image…
#   Upload the 1200×630 asset that already lives at: docs/og-image.png
# This is what renders when the repo is shared on X, LinkedIn, Slack, etc.

echo "Done. Verify with: gh repo view $REPO --json description,homepageUrl,repositoryTopics"
