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

REPO="isatimur/harness-humanizer-skill"

# --- Description + homepage --------------------------------------------------
gh repo edit "$REPO" \
  --description "Portable Claude Code skill that de-slops AI prose — detect, rewrite to a real point of view, self-score, iterate. Fidelity-first; flags hollow spans instead of faking them." \
  --homepage "https://harness-humanizer-skill.vercel.app/"

# --- Topics (13, re-asserted exactly) ---------------------------------------
# gh replaces the full topic set on each --add-topic invocation list below.
gh repo edit "$REPO" \
  --add-topic ai-writing \
  --add-topic claude-code \
  --add-topic claude-skill \
  --add-topic de-slop \
  --add-topic prose \
  --add-topic writing-tools \
  --add-topic agent-skills \
  --add-topic ai-slop \
  --add-topic anthropic-claude \
  --add-topic cursor \
  --add-topic developer-tools \
  --add-topic humanizer \
  --add-topic llm

# --- Social Preview (manual, one-time) --------------------------------------
# gh has no API for the Social Preview image, so set it by hand once:
#   Settings → General → Social preview → Upload an image…
#   Upload the 1280×640 asset that already lives at: docs/og-image.png
# This is what renders when the repo is shared on X, LinkedIn, Slack, etc.

echo "Done. Verify with: gh repo view $REPO --json description,homepageUrl,repositoryTopics"
