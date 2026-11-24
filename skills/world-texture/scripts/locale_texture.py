#!/usr/bin/env python3
"""World texture auditor: scores 10 micro-worldbuilding details and builds a Locale Texture Card.

Two subcommands:
  template   Print a blank locale JSON template.
  audit      Validate, score layers, check synergies/lenses, and render a Locale Texture Card.

Valid detail statuses:
  present   Concrete, usable detail is written (2 pts)
  sketch    Rough placeholder or partial idea exists (1 pt)
  absent    Not yet added (0 pts)
  na        Intentionally excluded for this locale (not scored)

Usage:
  python locale_texture.py template
  python locale_texture.py audit locale.json
  python locale_texture.py audit locale.json --output card.md --json result.json --min-score 70
"""

import argparse
import json
import sys
from pathlib import Path

SCORE = {"present": 2, "sketch": 1, "absent": 0}
NA = "na"
VALID_STATUSES = set(SCORE) | {NA}

LAYERS = [
    {
        "id": "voice_custom",
        "name": "Voice & Custom",
        "details": [
            {
                "id": "local_sayings",
                "name": "Local sayings / slogans",
                "prompt": "Everyday greetings, idioms, or oaths hinting at local culture and history.",
            },
            {
                "id": "regional_superstitions",
                "name": "Regional superstitions",
                "prompt": "Local quirks or taboos (e.g., never whistle at night) with real consequences if tested.",
            },
            {
                "id": "seasonal_festivals",
                "name": "Seasonal festivals",
                "prompt": "Recurring celebrations, harvests, or rituals—even a passing mention sets mood.",
            },
        ],
    },
    {
        "id": "physical_memory",
        "name": "Physical Memory",
        "details": [
            {
                "id": "famous_monuments",
                "name": "Famous monuments",
                "prompt": "Ancient landmarks, twin towers, or collapsing colossi showing past ambition and scale.",
            },
            {
                "id": "war_memorials",
                "name": "War memorials",
                "prompt": "Carved names or hillside weapons connecting the locale to unseen past generations.",
            },
            {
                "id": "scarred_landscapes",
                "name": "Scarred landscapes",
                "prompt": "Craters, scorched woods, or glassed earth showing the land remembers history.",
            },
            {
                "id": "unique_animals",
                "name": "Unique everyday wildlife",
                "prompt": "Non-Earth background creatures living ordinary lives in the setting.",
            },
        ],
    },
    {
        "id": "people_legend",
        "name": "Living People & Legend",
        "details": [
            {
                "id": "rival_families",
                "name": "Rival families",
                "prompt": "Two households or factions feuding over land, fishing rights, trade, or turf.",
            },
            {
                "id": "local_heroes",
                "name": "Local heroes",
                "prompt": "Ordinary locals famous nearby (a troll-slaying smith, a royal midwife, a shipwreck survivor).",
            },
            {
                "id": "famous_orders",
                "name": "Famous parties / knightly orders",
                "prompt": "Named companies or orders celebrated—or whispered about—in taverns and ballads.",
            },
        ],
    },
]

DETAIL_ORDER = [d["id"] for layer in LAYERS for d in layer["details"]]
DETAIL_TO_LAYER = {d["id"]: layer["id"] for layer in LAYERS for d in layer["details"]}


def template():
    """Return a blank locale texture JSON dict."""
    return {
        "locale": "",
        "region": "",
        "education_lens": "",
        "lifespan_lens": "",
        "details": {
            d["id"]: {"status": "absent", "detail": "", "hook": ""}
            for layer in LAYERS
            for d in layer["details"]
        },
        "_help": {
            "status": ["present", "sketch", "absent", "na"],
            "education_lens": "How does a scholar vs. an untrained traveler interpret these details?",
            "lifespan_lens": "How do short-lived vs. long-lived species perceive the age of these events?",
        },
    }


def _text(val):
    return str(val or "").strip()


def parse_detail(raw, detail_id):
    """Validate and normalize one detail entry."""
    loc = f"details.{detail_id}"
    if isinstance(raw, str):
        status, detail, hook = raw, "", ""
    elif isinstance(raw, dict):
        status = raw.get("status", "")
        detail = _text(raw.get("detail"))
        hook = _text(raw.get("hook"))
    else:
        raise ValueError(
            f"{loc}: entry must be 'present'/'sketch'/'absent'/'na' or {{'status': ..., 'detail': ..., 'hook': ...}}"
        )
    status = _text(status).lower()
    if status == "n/a":
        status = NA
    if status not in VALID_STATUSES:
        raise ValueError(
            f"{loc}: invalid status '{status or 'empty'}'. Valid: {', '.join(sorted(VALID_STATUSES))}"
        )
    if status in ("present", "sketch") and not detail:
        raise ValueError(f"{loc}: status is '{status}' but 'detail' text is empty")
    return {"status": status, "detail": detail, "hook": hook}


def audit_locale(data):
    """Validate and score a locale dict. Raises ValueError listing all schema errors."""
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object")
    raw_details = data.get("details")
    if not isinstance(raw_details, dict):
        raise ValueError("'details' field is missing or not an object. Run `template` to generate one")

    unknown = sorted(set(raw_details) - set(DETAIL_ORDER))
    missing, invalid, parsed = [], [], {}
    if unknown:
        invalid.append(f"details: unknown key(s) {', '.join(unknown)}. Valid: {', '.join(DETAIL_ORDER)}")

    for layer in LAYERS:
        for d in layer["details"]:
            did = d["id"]
            if did not in raw_details:
                missing.append(f"details.{did}")
                continue
            try:
                entry = parse_detail(raw_details[did], did)
            except ValueError as e:
                invalid.append(str(e))
                continue
            parsed[did] = {
                "id": did,
                "name": d["name"],
                "prompt": d["prompt"],
                "layer": layer["id"],
                "status": entry["status"],
                "detail": entry["detail"],
                "hook": entry["hook"],
                "score": None if entry["status"] == NA else SCORE[entry["status"]],
            }

    if missing or invalid:
        lines = []
        if missing:
            lines.append("Missing details (or mark as 'absent'/'na'):\n  - " + "\n  - ".join(missing))
        if invalid:
            lines.append("Invalid entries:\n  - " + "\n  - ".join(invalid))
        raise ValueError("\n".join(lines))

    layer_results = []
    for layer in LAYERS:
        items = [parsed[d["id"]] for d in layer["details"]]
        scored = [x["score"] for x in items if x["score"] is not None]
        pct = 100.0 * sum(scored) / (2 * len(scored)) if scored else None
        layer_results.append({
            "id": layer["id"],
            "name": layer["name"],
            "score": round(pct, 1) if pct is not None else None,
            "items": items,
        })

    all_scored = [parsed[did]["score"] for did in DETAIL_ORDER if parsed[did]["score"] is not None]
    total_score = round(100.0 * sum(all_scored) / (2 * len(all_scored)), 1) if all_scored else None

    education_lens = _text(data.get("education_lens"))
    lifespan_lens = _text(data.get("lifespan_lens"))

    warnings = []
    if not education_lens:
        warnings.append({
            "code": "missing_education_lens",
            "message": "education_lens is empty: specify what an educated scholar recognizes vs. an ordinary traveler.",
        })
    if not lifespan_lens:
        warnings.append({
            "code": "missing_lifespan_lens",
            "message": "lifespan_lens is empty: note how short-lived vs. long-lived species perceive recent vs. ancient history.",
        })

    sayings = parsed["local_sayings"]["status"]
    superst = parsed["regional_superstitions"]
    if (sayings in ("present", "sketch")) != (superst["status"] in ("present", "sketch")):
        if sayings != NA and superst["status"] != NA:
            warnings.append({
                "code": "culture_combo_incomplete",
                "message": "Pairing a local saying with a regional superstition creates instant cultural contrast; one of the two is missing.",
            })
    if superst["status"] in ("present", "sketch") and not superst["hook"]:
        warnings.append({
            "code": "untestable_superstition",
            "message": "regional_superstitions has no 'hook': define what happens if a player tests or breaks the taboo.",
        })

    weakest_first_layers = sorted(
        layer_results,
        key=lambda lr: (lr["score"] is None, lr["score"] if lr["score"] is not None else 999),
    )
    priorities = []
    for lr in weakest_first_layers:
        for item in sorted(lr["items"], key=lambda x: x["score"] if x["score"] is not None else 9):
            if item["score"] is not None and item["score"] < 2:
                priorities.append({
                    "layer": lr["name"],
                    "id": item["id"],
                    "name": item["name"],
                    "status": item["status"],
                    "prompt": item["prompt"],
                })

    return {
        "locale": _text(data.get("locale")) or "(unnamed locale)",
        "region": _text(data.get("region")),
        "education_lens": education_lens,
        "lifespan_lens": lifespan_lens,
        "total_score": total_score,
        "layers": layer_results,
        "warnings": warnings,
        "top_priorities": priorities[:3],
        "all_gaps": priorities,
    }


def _fmt_score(val):
    return "—" if val is None else f"{val:.0f}/100"


def format_report(res):
    lines = [f"# Locale Texture Card: {res['locale']}"]
    if res["region"]:
        lines.append(f"Region: {res['region']}")
    lines += [
        "",
        f"**Texture Coverage: {_fmt_score(res['total_score'])}**",
        "",
        "| Layer | Score |",
        "|---|---|",
    ]
    for lr in sorted(res["layers"], key=lambda x: x["score"] if x["score"] is not None else 999):
        lines.append(f"| {lr['name']} | {_fmt_score(lr['score'])} |")

    lines += ["", "## Calibration Lenses", ""]
    lines.append(f"- **Education lens:** {res['education_lens'] or '(not specified)'}")
    lines.append(f"- **Lifespan lens:** {res['lifespan_lens'] or '(not specified)'}")

    lines += ["", "## Ready-to-Use Details", ""]
    for lr in res["layers"]:
        lines += [f"### {lr['name']}", "", "| Detail | Status | Content | Hook |", "|---|---|---|---|"]
        for item in lr["items"]:
            content = item["detail"] or "—"
            hook = item["hook"] or "—"
            lines.append(f"| {item['name']} | {item['status']} | {content} | {hook} |")
        lines.append("")

    lines += ["## Synergy & Lens Warnings", ""]
    if res["warnings"]:
        lines += [f"- **{w['code']}**: {w['message']}" for w in res["warnings"]]
    else:
        lines.append("- None.")

    lines += ["", "## Top 3 High-Impact Additions", ""]
    if res["top_priorities"]:
        for i, p in enumerate(res["top_priorities"], 1):
            lines.append(f"{i}. **{p['layer']} — {p['name']}** (`{p['status']}`): {p['prompt']}")
    else:
        lines.append("All scored details are present. Keep details conversational and revealed through play, not lore dumps.")
    lines.append("")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="10-detail micro-worldbuilding texture auditor.")
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("template", help="Print blank locale texture JSON")
    au = sub.add_parser("audit", help="Audit a locale JSON and output a Locale Texture Card")
    au.add_argument("file", help="Locale JSON file")
    au.add_argument("--output", metavar="FILE", help="Write Markdown report to FILE instead of stdout")
    au.add_argument("--json", dest="json_path", metavar="OUT", help="Write structured audit JSON to OUT")
    au.add_argument("--min-score", type=float, default=None, help="Exit 1 if total score is below threshold")
    args = ap.parse_args(argv)

    if args.command == "template":
        json.dump(template(), sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    try:
        raw = json.loads(Path(args.file).read_text(encoding="utf-8"))
        raw.pop("_help", None)
        result = audit_locale(raw)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: could not read file: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"ERROR: invalid locale file.\n{e}", file=sys.stderr)
        return 2

    text = format_report(result)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.min_score is not None and (result["total_score"] is None or result["total_score"] < args.min_score):
        print(f"Total texture score is below minimum ({args.min_score}).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
