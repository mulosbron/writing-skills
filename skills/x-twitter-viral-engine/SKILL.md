---
name: x-twitter-viral-engine
description: Self-iterating X (Twitter) content generator ("Greatest Hits Rewriter") trained on Top 10% winning hooks and Bottom 90% hooks to avoid. Turns video transcripts or ideas into ranked, viral-ready posts.
---

# X / Twitter Viral Content Engine Skill

## Purpose
Generate high-reach X posts from video transcripts or ideas using a data-driven **Top 10% vs. Bottom 90% feedback loop** that improves every time new performance data is logged.

## Setup & Training Context
Maintain two reference lists (updated daily/weekly from your X Performance Tracker):
- **TOP 10% WINNING HOOKS (Do More Of This)**: Paste hooks that generated the highest impressions/engagement.
- **BOTTOM 90% UNDERPERFORMING HOOKS (Avoid This)**: Paste hooks that flopped or received low reach.
- **Target Audience**: Define who you are speaking to and what outcome they want.

## Workflow
1. **Ingest Source**: Accept a YouTube video transcript, article, or raw idea.
2. **Pattern Matching**:
   - Mirror the rhythm, curiosity gap, specificity, and framing of the **Top 10% Winning Hooks**.
   - Explicitly reject phrasing, openings, and structures found in the **Bottom 90% Hooks**.
3. **Generate & Rank**:
   - Produce **5 distinct X post variations** (mix of punchy single posts, short bulleted breakdowns, and video-companion captions).
   - **Order them from #1 (Highest Viral Potential) to #5**, with a 1-line rationale explaining *why* the hook matches winning data.
4. **Clean Paste Formatting**:
   - Use crisp line breaks and short punchy sentences so the user can copy and paste cleanly (using `Cmd+Shift+V` / `Ctrl+Shift+V`) without messy wall-of-text paragraphs.

## Daily Self-Iterating Feedback Loop SOP
1. Post the selected tweet (optionally paired with a native downloaded video clip).
2. Log `Post #`, `Date`, `Post Link`, `Views`, and `Hook` in `x_viral_hooks_tracker.xlsx`.
3. Run `scripts/hook_feedback_loop.py` to recalculate Top 10% vs. Bottom 90%.
4. Replace the Top 10% / Bottom 90% lists in this skill or Claude Project instructions to retrain on fresh data.
