#!/usr/bin/env python3
"""
Video Transcript -> Multi-Channel Claude Prompt Bundle Generator.
Takes a transcript file + target keyword + CTA URL and generates ready-to-paste prompts for:
1) SEO Blog Post, 2) 5x Multi-Platform Rewrites, 3) X Viral Tweets, 4) Livestream Mega-Guide.
"""

import argparse
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Convert a video transcript into a multi-channel Claude prompt pack.")
    p.add_argument("transcript_file", type=Path, help="Path to transcript .txt or .md file")
    p.add_argument("--keyword", required=True, help="Primary SEO keyword")
    p.add_argument("--cta", default="https://example.com", help="Target CTA destination URL")
    p.add_argument("--topic", default="", help="Optional topic name (defaults to keyword)")
    p.add_argument("-o", "--output", type=Path, default=Path("prompt_bundle.md"), help="Output Markdown bundle")
    args = p.parse_args()

    transcript = args.transcript_file.read_text(encoding="utf-8").strip()
    topic = args.topic or args.keyword
    snippet = transcript[:12000] + ("\n\n[...transcript truncated for preview; attach full file in Claude...]" if len(transcript) > 12000 else "")

    bundle = f"""# Multi-Channel Claude Prompt Bundle: {topic}

---

## Prompt 1: SEO Blog Post (Front-Loaded Keyword + 1 Sentence Per Line)

```text
Keyword = {args.keyword}
CTA URL = {args.cta}

Using the transcript below:
1. Create 5 short, attention-grabbing SEO headline options containing "{args.keyword}".
2. Write a comprehensive, easy-to-read SEO blog post optimized around "{args.keyword}".
3. Front-load "{args.keyword}" inside the VERY FIRST sentence.
4. Keep language simple and conversational, with clear H2/H3 headers.
5. Put EVERY sentence on its own new line.
6. Include 2-3 natural CTAs funneling readers to {args.cta}.

TRANSCRIPT:
{snippet}
```

---

## Prompt 2: 5x Multi-Platform Rewrites (LinkedIn, WordPress, X, Reddit, Newsletter)

```text
Rewrite the core insights from this "{topic}" transcript into 5 completely unique platform-native pieces:
1. LinkedIn Article (clean formatting, scannable headers, CTA to {args.cta})
2. X (Twitter) Thread (strong hook + 6 punchy takeaways)
3. Reddit Value Post (zero hard selling, pure step-by-step tactical breakdown)
4. Short Email Newsletter (curiosity subject line + 3 bullets + link)
5. YouTube Community / Skool Post (short punchy summary + discussion question)
```

---

## Prompt 3: Live Stream 6,000-Word Mega-Guide & Lead Magnet

```text
Topic = {topic}
Offer CTA = {args.cta}

Research the latest updates on "{topic}" and build a complete live stream presenter guide & lead magnet in this exact order:
1. Opening Hook (first 30 seconds) + Live Demo Links
2. Custom Named Framework + Subheadline
3. Belief-Breaking Section (3-5 old beliefs vs new truths)
4. Russell Brunson Hook-Story-Offer flow
5. 30-Day Implementation Plan
6. Social Promo Posts (X, LinkedIn, YouTube Community)
7. 100 Practical Copy-Paste Prompts for {topic}
```
"""
    args.output.write_text(bundle, encoding="utf-8")
    print(f"Created multi-channel prompt bundle -> {args.output}")


if __name__ == "__main__":
    main()
