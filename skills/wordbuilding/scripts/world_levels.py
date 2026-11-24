#!/usr/bin/env python3
"""Worldbuilding 7-level scale: 36-question diagnostic bank and profiler.

Two subcommands:
  checklist   Print a blank JSON questionnaire (all levels or a single level).
  evaluate    Score a completed JSON file, build the 7-level profile, and list open questions.

The seven levels are layers of understanding rather than sequential rungs: a world
can be strong at Level 5 while leaving structural questions unanswered at Level 2.
Output is therefore a 7-level profile highlighting open questions below the highest
strong level, rather than a single collapsed score.

Valid answers: yes, partial, no, na (excluded from scoring). Questions with
"direction": "risk" invert scoring so "yes" acts as a warning flag.

Usage:
  python world_levels.py checklist                    # all 36 questions
  python world_levels.py checklist --level 4          # Level 4 only
  python world_levels.py evaluate world.json          # Markdown profile (stdout)
  python world_levels.py evaluate world.json --json result.json --output profile.md
"""

import argparse
import json
import sys
from pathlib import Path

# direction: "positive" earns points for "yes"; "risk" warns on "yes" and inverts points.
LEVELS = [
    {
        "num": 1,
        "name": "Map",
        "summary": "Land must obey rules—either Earth's or your setting's explicitly defined physics.",
        "questions": [
            {
                "id": "rivers",
                "direction": "positive",
                "question": "Do rivers flow downhill by elevation and converge rather than splitting or cutting randomly across mountain ranges?",
                "example": "Westeros: the Riverlands sit between the mountainous Vale and hilly Westerlands, so rivers naturally converge there.",
            },
            {
                "id": "mountains",
                "direction": "positive",
                "question": "Are mountain ranges placed for a geological reason, with rain shadows and climate splits considered?",
                "example": "Mountains act as natural terrain barriers rather than random spikes dotted across a map.",
            },
            {
                "id": "cities",
                "direction": "positive",
                "question": "Are cities located for concrete reasons—water, trade routes, or defensible terrain?",
                "example": "Harbors sit in deep water and major settlements sit on rivers or crossroads rather than being evenly spaced for symmetry.",
            },
            {
                "id": "climate",
                "direction": "positive",
                "question": "Can deserts, frozen regions, ocean currents, and prevailing winds be explained?",
                "example": "The North is cold and sparsely populated because harsh northern climates cannot sustain dense cities.",
            },
            {
                "id": "own_rules",
                "direction": "positive",
                "question": "If the world breaks Earth logic, are the replacement rules defined upfront and applied consistently?",
                "example": "Discworld is flat on the back of a turtle, yet stays faithful to its own internal premise rather than acting arbitrarily.",
            },
        ],
    },
    {
        "num": 2,
        "name": "Rule of Cool",
        "summary": "Dragons, fallen empires, cursed forests: breadth expands the world, but breadth is not depth.",
        "questions": [
            {
                "id": "striking_elements",
                "direction": "positive",
                "question": "Are there striking, evocative elements (dragons, fallen empires nobody fully understands, whispering cursed woods)?",
                "example": "These elements set tone and identity—often what hooks players into your setting in the first place.",
            },
            {
                "id": "defines_identity",
                "direction": "positive",
                "question": "Do those elements establish the setting's tone and emotional identity?",
                "example": "With strong enough characters and narrative momentum, a whole story can thrive right at this level.",
            },
            {
                "id": "depth_illusion",
                "direction": "risk",
                "question": "Are extra gods and ancient wars being added under the assumption that 'bigger' means 'deeper'?",
                "example": "Diagnostic distinction: is the world built on top of cool ideas, or on top of rules?",
            },
            {
                "id": "structural_gaps",
                "direction": "risk",
                "question": "Are foundational structural questions left unanswered (how magic affects daily life, what replaced a fallen empire)?",
                "example": "Asking structural questions does not kill creativity—it reveals what the world actually runs on.",
            },
        ],
    },
    {
        "num": 3,
        "name": "Surface Identity",
        "summary": "The setting stops feeling like generic fantasy and becomes unmistakably itself: names, architecture, clothing, emblems.",
        "questions": [
            {
                "id": "naming",
                "direction": "positive",
                "question": "Do naming conventions follow consistent phonetic rules within each region or culture?",
                "example": "Lord of the Rings: Elvish names follow one phonetic pattern while the Rohirrim carry distinct historical roots—no label needed.",
            },
            {
                "id": "visual_consistency",
                "direction": "positive",
                "question": "Do architecture, attire, armor, symbols, and banners speak the same visual language?",
                "example": "Warhammer 40K's Imperium carries cathedrals, skulls, and oversized armor consistently across weapons, flags, and buildings.",
            },
            {
                "id": "silhouette",
                "direction": "positive",
                "question": "Can you tell where a character or faction belongs from silhouette alone?",
                "example": "From across a battlefield, a helmet or cloak silhouette immediately signals faction.",
            },
            {
                "id": "core_anchor",
                "direction": "positive",
                "question": "Does each region grow from a core inspiration into architecture, clothing, palette, environment, and motivation?",
                "example": "Avatar: Water Tribe draws from Inuit/Arctic life, Earth Kingdom from East Asia, Fire Nation from industrializing imperial Japan.",
            },
            {
                "id": "planet_of_hats",
                "direction": "risk",
                "question": "Is any culture flattened into a single trait ('the warrior race', 'the clever race') where everyone acts identically?",
                "example": "The Planet of Hats trap: aim to make a culture recognizable, not uniform.",
            },
        ],
    },
    {
        "num": 4,
        "name": "Functional Power",
        "summary": "The world stops merely looking distinct and starts behaving logically: power reshapes everything around it.",
        "questions": [
            {
                "id": "power_rules",
                "direction": "positive",
                "question": "Do magic, technology, and divine powers have explicit rules, limits, and costs?",
                "example": "Mistborn: specific metals grant specific abilities with strict limits and counters.",
            },
            {
                "id": "daily_life",
                "direction": "positive",
                "question": "Does power visibly reshape daily labor, security, travel, and urban movement?",
                "example": "Mistborn: an elite caste of magic users concentrates political power and completely alters security and assassination.",
            },
            {
                "id": "political_authority",
                "direction": "positive",
                "question": "Does power determine who holds political legitimacy and authority?",
                "example": "Attack on Titan: political leadership grounds its legitimacy in protecting citizens behind walls.",
            },
            {
                "id": "warfare",
                "direction": "positive",
                "question": "Do creatures or technologies fundamentally shape warfare and defense?",
                "example": "Attack on Titan: massive walls, fortified ring cities, and vertical-mobility gear engineered specifically for Titans.",
            },
            {
                "id": "tech_constraints",
                "direction": "positive",
                "question": "Are technological limits intentional, with downstream consequences thought through?",
                "example": "Dune: thinking machines are banned, so humans are trained to replace them and shields reshape melee combat.",
            },
            {
                "id": "power_destabilization",
                "direction": "risk",
                "question": "If an overwhelming entity or artifact exists, is it left unexplained why it hasn't destabilized everything?",
                "example": "Power with rules and costs stops plot-cheating and makes major events feel like accumulated pressure.",
            },
        ],
    },
    {
        "num": 5,
        "name": "Deep Culture and History",
        "summary": "The world stops looking weathered and becomes genuinely old: beliefs, arguments, taboos, and accumulated history.",
        "questions": [
            {
                "id": "beliefs_debates",
                "direction": "positive",
                "question": "Do we know what people believe, argue over, feel ashamed of, and refuse to abandon even when irrational?",
                "example": "Deep culture means people hold contradictory beliefs and act emotionally—just like real societies.",
            },
            {
                "id": "tradition_origins",
                "direction": "positive",
                "question": "Did traditions start from practical needs before becoming sacred customs or unquestioned taboos?",
                "example": "Practical survival habits ossified into 'we have always done it this way' taboos.",
            },
            {
                "id": "history_ripples",
                "direction": "positive",
                "question": "Does history create ongoing ripples—borders, ruins, trade shifts, religious schisms—rather than isolated dates?",
                "example": "The Silmarillion: past events reshape geography and spawn oaths that trigger wars ages later.",
            },
            {
                "id": "continuity",
                "direction": "positive",
                "question": "Do actions accumulate across eras so present decisions rest on centuries of weight?",
                "example": "By Lord of the Rings, ruins are not scenery—they are shattered kingdoms with living consequences.",
            },
            {
                "id": "internal_contradiction",
                "direction": "positive",
                "question": "Do peasants, nobles, and merchants think differently, and do regions treat the same group differently?",
                "example": "The Witcher: prejudice against non-humans evolves out of war, economic rivalry, and fear, varying by region.",
            },
            {
                "id": "plural_narratives",
                "direction": "positive",
                "question": "Do different peoples and factions remember the same historical events in conflicting ways?",
                "example": "The Elder Scrolls: races recall the same wars differently, religions clash, and factions reinterpret history to justify power.",
            },
            {
                "id": "place_names",
                "direction": "positive",
                "question": "Do place names carry stories of what happened there long ago?",
                "example": "A city's name preserves a forgotten battle, flood, or founder's bargain.",
            },
        ],
    },
    {
        "num": 6,
        "name": "Infrastructure and Institutions",
        "summary": "Banking, trade arteries, military logistics: the gears that keep the world turning without protagonists.",
        "questions": [
            {
                "id": "food_supply",
                "direction": "positive",
                "question": "Do you know how a city of 200,000 inhabitants feeds itself?",
                "example": "If Level 4 is what's under the hood, Level 6 is the gears inside that engine.",
            },
            {
                "id": "communication",
                "direction": "positive",
                "question": "In a continent-spanning empire, how many days does an order take from capital to frontier?",
                "example": "Communication speed dictates how far an empire can coherently govern.",
            },
            {
                "id": "logistics",
                "direction": "positive",
                "question": "How are armies supplied and along which routes does bulk trade flow?",
                "example": "Most worlds hand-wave supply lines; at this level, logistics constrain strategy.",
            },
            {
                "id": "finance",
                "direction": "positive",
                "question": "How are wars financed, and do institutions hold long-term interests independent of the throne?",
                "example": "The Iron Bank of Braavos has no armies or dragons, yet backs rival claimants when crowns default.",
            },
            {
                "id": "closed_systems",
                "direction": "positive",
                "question": "Are institutions closed systems where breaking one component sends shockwaves through the rest?",
                "example": "Fallout Vaults and Snowpiercer's train: engineered closed ecosystems where infrastructure failure threatens survival.",
            },
            {
                "id": "ruler_independent",
                "direction": "positive",
                "question": "Do institutions keep operating regardless of who sits on the throne this season?",
                "example": "The world visibly runs on institutional momentum beyond any single ruler.",
            },
        ],
    },
    {
        "num": 7,
        "name": "Generative World",
        "summary": "The world generates stories by itself—zoom in anywhere and pre-existing tension awaits.",
        "questions": [
            {
                "id": "tension_everywhere",
                "direction": "positive",
                "question": "If you zoom into any province, port, or era, is there pre-existing tension ready to become a story?",
                "example": "Instead of forcing a plot onto empty terrain, you uncover conflicts already baked into the setup.",
            },
            {
                "id": "protagonist_free",
                "direction": "positive",
                "question": "Would the world keep moving without the protagonist rather than hanging on a single narrative thread?",
                "example": "You could follow a king, a merchant, or a thief—the world does not rely on one chosen storyline.",
            },
            {
                "id": "time_jump",
                "direction": "positive",
                "question": "Could you jump 400 years into the past and tell an equally compelling, grounded story?",
                "example": "With coherent geography, lived cultures, rule-bound power, and institutions, eras tell stories automatically.",
            },
        ],
    },
]

SCORE = {"yes": 2, "partial": 1, "no": 0}
NA = "na"
VALID = set(SCORE) | {NA}
THREE_QUESTIONS = ["Why is it here?", "Who benefits from it?", "What happens if this changes?"]
STRONG_THRESHOLD, WEAK_THRESHOLD = 80.0, 50.0


def template(level=None):
    """Return a blank checklist JSON dict; filter to a single level if specified."""
    selected = [s for s in LEVELS if level is None or s["num"] == level]
    return {
        "world": "",
        "answers": {
            str(s["num"]): {q["id"]: "" for q in s["questions"]} for s in selected
        },
    }


def parse_answer(value, loc):
    """Parse one answer into (status, note); raise ValueError if invalid."""
    if isinstance(value, dict):
        status, note = value.get("status", ""), str(value.get("note", "") or "").strip()
    elif isinstance(value, str):
        status, note = value, ""
    else:
        raise ValueError(f"{loc}: answer must be 'yes'/'partial'/'no'/'na' or {{'status': ..., 'note': ...}}")
    status = str(status or "").strip().lower()
    if status == "n/a":
        status = NA
    if status not in VALID:
        raise ValueError(f"{loc}: invalid '{status or 'empty'}'. Valid values: {', '.join(sorted(VALID))}")
    return status, note


def _level_status(score, has_zero):
    if score is None:
        return "na"
    if score >= STRONG_THRESHOLD and not has_zero:
        return "strong"
    return "weak" if score < WEAK_THRESHOLD else "partial"


def score_world(data):
    """Score a world checklist dict. Raises ValueError on missing/invalid entries."""
    if not isinstance(data, dict):
        raise ValueError("Input must be a JSON object")
    answers = data.get("answers")
    if not isinstance(answers, dict) or not answers:
        raise ValueError("'answers' field is missing or empty. Run `checklist` for a blank template")
    known = {str(s["num"]): s for s in LEVELS}
    missing, invalid, processed = [], [], {}

    for num_key, raw in answers.items():
        key = str(num_key).strip()
        if key not in known:
            invalid.append(f"answers.{num_key}: unknown level. Valid: {', '.join(known)}")
            continue
        if not isinstance(raw, dict):
            missing.append(f"answers.{key}")
            continue
        level = known[key]
        unknown_q = set(raw) - {q["id"] for q in level["questions"]}
        if unknown_q:
            invalid.append(f"answers.{key}: unknown question(s) {', '.join(sorted(unknown_q))}")
        rows = []
        for q in level["questions"]:
            if q["id"] not in raw:
                missing.append(f"answers.{key}.{q['id']}")
                continue
            raw_val = raw[q["id"]]
            is_empty = (
                raw_val is None
                or (isinstance(raw_val, str) and not raw_val.strip())
                or (isinstance(raw_val, dict) and not str(raw_val.get("status") or "").strip())
            )
            if is_empty:
                missing.append(f"answers.{key}.{q['id']}")
                continue
            try:
                status, note = parse_answer(raw_val, f"answers.{key}.{q['id']}")
            except ValueError as e:
                invalid.append(str(e))
                continue
            raw_pts = None if status == NA else SCORE[status]
            pts = None if raw_pts is None else (raw_pts if q["direction"] == "positive" else 2 - raw_pts)
            rows.append({
                "id": q["id"],
                "direction": q["direction"],
                "question": q["question"],
                "example": q["example"],
                "status": status,
                "note": note,
                "score": pts,
            })
        processed[level["num"]] = rows

    if missing or invalid:
        lines = []
        if missing:
            lines.append("Missing answers (or set to 'na'):\n  - " + "\n  - ".join(missing))
        if invalid:
            lines.append("Invalid values:\n  - " + "\n  - ".join(invalid))
        raise ValueError("\n".join(lines))

    result = {"world": str(data.get("world", "") or "").strip() or "(unnamed world)", "levels": []}
    for level in LEVELS:
        if level["num"] not in processed:
            continue
        rows = processed[level["num"]]
        pts = [r["score"] for r in rows if r["score"] is not None]
        pct = 100.0 * sum(pts) / (2 * len(pts)) if pts else None
        result["levels"].append({
            "num": level["num"],
            "name": level["name"],
            "summary": level["summary"],
            "score": round(pct, 1) if pct is not None else None,
            "status": _level_status(pct, any(p == 0 for p in pts)),
            "items": rows,
        })

    strong = [s["num"] for s in result["levels"] if s["status"] == "strong"]
    result["highest_strong"] = max(strong) if strong else None
    result["unassessed"] = [s["num"] for s in LEVELS if s["num"] not in processed]

    open_q, risks = [], []
    for s in result["levels"]:
        for r in s["items"]:
            if r["score"] is not None and r["score"] < 2:
                open_q.append({
                    "level": s["num"],
                    "level_name": s["name"],
                    "id": r["id"],
                    "question": r["question"],
                    "status": r["status"],
                    "below_strong": result["highest_strong"] is not None and s["num"] < result["highest_strong"],
                })
            if r["direction"] == "risk" and r["status"] in ("yes", "partial"):
                risks.append({
                    "level": s["num"],
                    "question": r["question"],
                    "status": r["status"],
                    "example": r["example"],
                })
    result["open_questions"] = open_q
    result["below_strong_questions"] = [a for a in open_q if a["below_strong"]]
    result["risks"] = risks
    result["three_questions"] = THREE_QUESTIONS

    scored = [s for s in result["levels"] if s["score"] is not None]
    if scored:
        weakest = min(scored, key=lambda s: s["score"])
        q = min((r for r in weakest["items"] if r["score"] is not None), key=lambda r: r["score"])
        result["next_step"] = {
            "level": weakest["num"],
            "level_name": weakest["name"],
            "score": weakest["score"],
            "id": q["id"],
            "question": q["question"],
            "example": q["example"],
        }
    else:
        result["next_step"] = None
    return result


def _fmt_score(score):
    return "—" if score is None else (f"{score:.0f}/100" if score == int(score) else f"{score:.1f}/100")


def format_report(s):
    out = [f"# World Profile: {s['world']}", ""]
    assessed = [x["num"] for x in s["levels"]]
    line = f"Assessed levels: {', '.join(map(str, assessed)) or 'none'}"
    if s["unassessed"]:
        line += f". Unassessed: {', '.join(map(str, s['unassessed']))}"
    out += [line, "", "| Level | Name | Score | Status |", "|---|---|---|---|"]
    for x in s["levels"]:
        out.append(f"| {x['num']} | {x['name']} | {_fmt_score(x['score'])} | {x['status']} |")
    out += ["", "## Reading the Profile", ""]
    if s["highest_strong"] is None:
        out.append("No level is 'strong' yet. That is not a flaw—these are layers of understanding, and many great stories thrive at Level 2.")
    else:
        top = next(x for x in s["levels"] if x["num"] == s["highest_strong"])
        out.append(f"Highest strong level: **{top['num']}. {top['name']}**.")
        out.append("Levels are not sequential rungs; lower levels need not be 100% strong. However, open questions below your strongest layer represent structural gaps underneath it.")
    if s["below_strong_questions"]:
        out += ["", f"## Open Questions Below Highest Strong Level ({s['highest_strong']})", ""]
        for i, a in enumerate(s["below_strong_questions"], 1):
            out.append(f"{i}. [Level {a['level']}, {a['status']}] {a['question']}")
    out += ["", "## Risk Flags", ""]
    if s["risks"]:
        out.append("In these items, 'yes' indicates a warning flag.")
        for r in s["risks"]:
            out.append(f"- [Level {r['level']}, {r['status']}] {r['question']}")
    else:
        out.append("- None.")
    if s["next_step"]:
        a = s["next_step"]
        out += [
            "",
            "## Next Step",
            "",
            f"Weakest level: **{a['level']}. {a['level_name']}** ({_fmt_score(a['score'])}). Start with this question:",
            "",
            f"> {a['question']}",
            "",
            f"Example of what good looks like: {a['example']}",
        ]
    out += ["", "## Three Questions to Ask Any World Element", ""]
    out += [f"- {g}" for g in s["three_questions"]]
    out.append("")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="7-level worldbuilding profiler.")
    sub = ap.add_subparsers(dest="command", required=True)
    c = sub.add_parser("checklist", help="Print blank checklist JSON")
    c.add_argument("--level", type=int, choices=[s["num"] for s in LEVELS], help="Only output this level")
    ev = sub.add_parser("evaluate", help="Score a completed checklist JSON")
    ev.add_argument("file", help="Completed checklist JSON file")
    ev.add_argument("--json", metavar="OUT", help="Also write profile result to JSON file")
    ev.add_argument("--output", metavar="FILE", help="Write Markdown profile to FILE instead of stdout")
    args = ap.parse_args(argv)

    if args.command == "checklist":
        json.dump(template(args.level), sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    try:
        data = json.loads(Path(args.file).read_text(encoding="utf-8"))
        result = score_world(data)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: could not read file: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"ERROR: invalid file.\n{e}", file=sys.stderr)
        return 2

    text = format_report(result)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    if args.json:
        Path(args.json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
