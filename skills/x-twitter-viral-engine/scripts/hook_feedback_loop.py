#!/usr/bin/env python3
"""
X / Twitter Self-Iterating Feedback Loop Generator.
Reads a CSV of posts (columns: views, hook) and splits them into Top 10% winning hooks
and Bottom 90% underperforming hooks, outputting updated Claude Project instructions.
"""

import argparse
import csv
import math
from pathlib import Path


def load_rows(csv_path: Path):
    rows = []
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for r in reader:
            hook = (r.get("hook") or r.get("Hook Used") or "").strip()
            views_raw = (r.get("views") or r.get("Views") or "0").replace(",", "").strip()
            if not hook:
                continue
            try:
                views = int(float(views_raw))
            except ValueError:
                views = 0
            rows.append({"views": views, "hook": hook, "topic": (r.get("topic") or "").strip()})
    return rows


def generate_instructions(rows, top_pct: float = 0.10):
    if not rows:
        return "# No rows found in tracker CSV.\n"
    sorted_rows = sorted(rows, key=lambda x: x["views"], reverse=True)
    top_n = max(1, math.ceil(len(sorted_rows) * top_pct))
    top_hooks = sorted_rows[:top_n]
    bottom_hooks = sorted_rows[top_n:]

    lines = [
        "# Updated X / Twitter Viral Engine Instructions (Auto-Generated)",
        "",
        f"Total posts analyzed: **{len(sorted_rows)}** | Top {int(top_pct*100)}% cutoff: **{top_hooks[-1]['views']:,} views**",
        "",
        "## TOP 10% WINNING HOOKS — DO MORE OF THIS",
        "Mirror the curiosity gap, rhythm, and specificity of these top performers:",
        "",
    ]
    for r in top_hooks:
        lines.append(f"- **[{r['views']:,} views]** {r['hook']}")

    lines += [
        "",
        "## BOTTOM 90% UNDERPERFORMING HOOKS — AVOID THIS",
        "Do NOT reuse the phrasing, weak openings, or generic structures below:",
        "",
    ]
    for r in bottom_hooks:
        lines.append(f"- [{r['views']:,} views] {r['hook']}")

    lines += [
        "",
        "## Generation Rule",
        "Whenever I paste a video transcript or topic, write 5 X post options ranked from #1 (highest viral potential) to #5 based strictly on the Top 10% patterns above.",
        "",
    ]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Generate Top 10% / Bottom 90% X hook instructions for Claude.")
    p.add_argument("csv_file", type=Path, help="Path to x_viral_hooks_tracker.csv")
    p.add_argument("-o", "--output", type=Path, default=Path("updated_x_instructions.md"), help="Output Markdown path")
    p.add_argument("--top-pct", type=float, default=0.10, help="Top percentile fraction (default: 0.10)")
    args = p.parse_args()

    rows = load_rows(args.csv_file)
    md = generate_instructions(rows, args.top_pct)
    args.output.write_text(md, encoding="utf-8")
    print(f"Analyzed {len(rows)} hooks -> wrote {args.output}")


if __name__ == "__main__":
    main()
