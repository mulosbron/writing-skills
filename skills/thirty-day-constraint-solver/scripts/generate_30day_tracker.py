#!/usr/bin/env python3
"""
Custom 30-Day Input-to-Output Business Constraint Tracker (.xlsx) Generator.
Usage:
  python3 generate_30day_tracker.py --goal "Hire SEO Sales Reps" \
    --inputs "Upwork Post,LinkedIn DM,Community Post" \
    --outputs "Applications,Calls Booked,Offers Made" -o custom_30day.xlsx
"""

import argparse
from datetime import date, timedelta
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def build_workbook(goal: str, start: date, inputs: list, outputs: list, out_path: Path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "30-Day Tracker"

    fill_meta = PatternFill("solid", fgColor="1E293B")
    fill_in = PatternFill("solid", fgColor="1D4ED8")
    fill_out = PatternFill("solid", fgColor="047857")
    fill_tot = PatternFill("solid", fgColor="E2E8F0")
    white_bold = Font(name="Calibri", size=10.5, bold=True, color="FFFFFF")
    body = Font(name="Calibri", size=10)
    bold = Font(name="Calibri", size=10.5, bold=True)
    thin = Side(style="thin", color="CBD5E1")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    headers = [("Day", fill_meta), ("Date", fill_meta)] + [(x, fill_in) for x in inputs] + [("Input Total", fill_in)] + [(y, fill_out) for y in outputs]
    for i, (h, fl) in enumerate(headers, start=1):
        c = ws.cell(row=1, column=i, value=h)
        c.fill = fl; c.font = white_bold; c.border = border
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 28

    in_start_col = 3
    in_end_col = 2 + len(inputs)
    score_col = in_end_col + 1
    total_cols = len(headers)

    for d in range(30):
        r = d + 2
        ws.cell(row=r, column=1, value=f"Day {d+1}").font = body
        ws.cell(row=r, column=2, value=(start + timedelta(days=d)).isoformat()).font = body
        for c_i in range(3, total_cols + 1):
            cell = ws.cell(row=r, column=c_i)
            if c_i == score_col:
                cell.value = f"=SUM({get_column_letter(in_start_col)}{r}:{get_column_letter(in_end_col)}{r})"
                cell.font = bold
            else:
                cell.value = 0
                cell.font = body
            cell.number_format = "#,##0"
        for c_i in range(1, total_cols + 1):
            ws.cell(row=r, column=c_i).border = border

    tot_r = 32
    ws.cell(row=tot_r, column=1, value="TOTAL").font = bold
    ws.cell(row=tot_r, column=2, value=goal).font = bold
    for c_i in range(3, total_cols + 1):
        col_l = get_column_letter(c_i)
        c = ws.cell(row=tot_r, column=c_i, value=f"=SUM({col_l}2:{col_l}31)")
        c.font = bold; c.number_format = "#,##0"
    for c_i in range(1, total_cols + 1):
        ws.cell(row=tot_r, column=c_i).fill = fill_tot
        ws.cell(row=tot_r, column=c_i).border = border

    for i in range(1, total_cols + 1):
        ws.column_dimensions[get_column_letter(i)].width = 16 if i > 2 else 13
    ws.freeze_panes = "C2"

    # KPI Gap Tab
    ks = wb.create_sheet("KPI Benchmarks")
    k_hdrs = ["Metric", "Category", "30-Day Target", "Actual", "Gap", "Progress %"]
    for i, h in enumerate(k_hdrs, start=1):
        c = ks.cell(row=1, column=i, value=h)
        c.fill = fill_meta; c.font = white_bold; c.border = border
    row_i = 2
    for idx, name in enumerate(inputs):
        col_l = get_column_letter(in_start_col + idx)
        ks.cell(row=row_i, column=1, value=name).font = body
        ks.cell(row=row_i, column=2, value="Input").font = body
        ks.cell(row=row_i, column=3, value=30).number_format = "#,##0"
        ks.cell(row=row_i, column=4, value=f"='30-Day Tracker'!{col_l}32").number_format = "#,##0"
        ks.cell(row=row_i, column=5, value=f"=D{row_i}-C{row_i}").number_format = "+#,##0;-#,##0;0"
        ks.cell(row=row_i, column=6, value=f"=IFERROR(D{row_i}/C{row_i},0)").number_format = "0.0%"
        for c_i in range(1, 7): ks.cell(row=row_i, column=c_i).border = border
        row_i += 1
    for idx, name in enumerate(outputs):
        col_l = get_column_letter(score_col + 1 + idx)
        ks.cell(row=row_i, column=1, value=name).font = body
        ks.cell(row=row_i, column=2, value="Output").font = body
        ks.cell(row=row_i, column=3, value=10).number_format = "#,##0"
        ks.cell(row=row_i, column=4, value=f"='30-Day Tracker'!{col_l}32").number_format = "#,##0"
        ks.cell(row=row_i, column=5, value=f"=D{row_i}-C{row_i}").number_format = "+#,##0;-#,##0;0"
        ks.cell(row=row_i, column=6, value=f"=IFERROR(D{row_i}/C{row_i},0)").number_format = "0.0%"
        for c_i in range(1, 7): ks.cell(row=row_i, column=c_i).border = border
        row_i += 1
    for i, w in enumerate([26, 12, 15, 14, 14, 14], start=1):
        ks.column_dimensions[get_column_letter(i)].width = w

    wb.save(out_path)


def main():
    p = argparse.ArgumentParser(description="Generate a custom 30-day Input/Output Excel tracker.")
    p.add_argument("--goal", required=True, help="Business constraint or 30-day goal")
    p.add_argument("--start-date", default=date.today().isoformat(), help="YYYY-MM-DD start date")
    p.add_argument("--inputs", required=True, help="Comma-separated controllable daily inputs")
    p.add_argument("--outputs", required=True, help="Comma-separated lagging outputs")
    p.add_argument("-o", "--output", type=Path, default=Path("custom_30day_tracker.xlsx"), help="Output .xlsx path")
    args = p.parse_args()

    inputs = [x.strip() for x in args.inputs.split(",") if x.strip()]
    outputs = [x.strip() for x in args.outputs.split(",") if x.strip()]
    build_workbook(args.goal, date.fromisoformat(args.start_date), inputs, outputs, args.output)
    print(f"Generated 30-day tracker for '{args.goal}' -> {args.output}")


if __name__ == "__main__":
    main()
