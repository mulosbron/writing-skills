---
name: thirty-day-constraint-solver
description: Turns any business bottleneck (hiring, sales, churn, lead gen) into a 30-day controllable Input-to-Output execution plan and KPI benchmark tracker (Target vs. Actual vs. Gap).
---

# 30-Day Business Constraint Solver Skill

## Purpose
Eliminate guesswork on any business constraint by defining daily **controllable inputs** (tasks you 100% control) that mathematically drive desired **outputs**, tracked over 30 days.

## Required Inputs
- `constraint_or_goal`: The problem to solve (e.g., "Hire SEO sales reps", "Reduce community churn", "Double inbound leads").
- `start_date`: Anchor date for Day 1 (defaults to today).
- `known_inputs` (optional): Specific daily actions already planned (e.g., "Post 1 Upwork job/day + message hot list").

## Execution Workflow
1. **Identify Controllable Daily Inputs (Leading Indicators)**:
   - Define 4–6 concrete, binary or numeric daily actions (e.g., Upwork posts, Direct Outreach, LinkedIn DMs, Community Posts) where hitting `1` every day makes failure nearly impossible.
2. **Define Measurable Outputs (Lagging Indicators)**:
   - Map the conversion funnel from inputs to final result (e.g., Applications Received -> Screening Calls Booked -> Calls Completed -> Trial Tasks Sent -> Final Interviews -> Offers Made).
3. **Build the 30-Day Plan**:
   - Break down Week 1 (Setup & Launch), Week 2 (Volume & Optimization), Week 3 (Filtering & Iteration), and Week 4 (Closing & Systemizing).
4. **Generate KPI Benchmark Table**:
   - Columns: `Metric | 30-Day Target | Actual | Gap (Actual - Target) | Improvement Lever`.
5. **Spreadsheet Export Ready**:
   - Output clean tabular structure (or run `scripts/generate_30day_tracker.py` to generate a formatted `.xlsx` workbook with date columns, `SUM` totals, and KPI formulas ready for Google Sheets).
