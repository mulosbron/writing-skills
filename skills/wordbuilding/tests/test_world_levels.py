#!/usr/bin/env python3
"""Unit tests for wordbuilding world_levels.py. Run: python -m unittest tests/test_world_levels.py"""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import world_levels as wl  # noqa: E402

SAMPLE_PATH = ROOT / "assets" / "sample_world.json"
SAMPLE = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
RISK_IDS = {"depth_illusion", "structural_gaps", "planet_of_hats", "power_destabilization"}


def run_cli(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = wl.main(argv)
    return code, out.getvalue(), err.getvalue()


def temp_json(data):
    d = tempfile.TemporaryDirectory()
    path = Path(d.name) / "world.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return d, path


def all_status(status):
    """Fill every question across all 7 levels with the same status."""
    return {
        "world": "Test World",
        "answers": {str(s["num"]): {q["id"]: status for q in s["questions"]} for s in wl.LEVELS},
    }


def strong_world():
    """Full marks across all levels: positive='yes', risk='no'."""
    v = all_status("yes")
    for s in wl.LEVELS:
        for q in s["questions"]:
            if q["direction"] == "risk":
                v["answers"][str(s["num"])][q["id"]] = "no"
    return v


class QuestionBankTests(unittest.TestCase):
    def test_seven_levels_36_questions(self):
        self.assertEqual([s["num"] for s in wl.LEVELS], list(range(1, 8)))
        self.assertEqual([len(s["questions"]) for s in wl.LEVELS], [5, 4, 5, 6, 7, 6, 3])
        ids = [q["id"] for s in wl.LEVELS for q in s["questions"]]
        self.assertEqual(len(ids), len(set(ids)), "question IDs must be unique")
        for s in wl.LEVELS:
            for q in s["questions"]:
                self.assertEqual(q["direction"] == "risk", q["id"] in RISK_IDS)
                self.assertTrue(q["question"].endswith("?"))
                self.assertTrue(q["example"])


class ScoringTests(unittest.TestCase):
    def test_all_strong(self):
        s = wl.score_world(strong_world())
        self.assertTrue(all(x["score"] == 100.0 and x["status"] == "strong" for x in s["levels"]))
        self.assertEqual(s["risks"], [])
        self.assertEqual((s["highest_strong"], s["below_strong_questions"]), (7, []))

    def test_risk_questions_invert_scoring(self):
        v = all_status("yes")
        levels = {x["num"]: x for x in wl.score_world(v)["levels"]}
        self.assertEqual(levels[2]["score"], 50.0)  # (2+2+0+0)/8
        v["answers"]["2"]["depth_illusion"] = "no"
        v["answers"]["2"]["structural_gaps"] = "partial"
        levels = {x["num"]: x for x in wl.score_world(v)["levels"]}
        self.assertEqual(levels[2]["score"], 87.5)  # (2+2+2+1)/8
        self.assertEqual(levels[2]["status"], "strong")
        self.assertEqual(
            [(r["level"], r["status"]) for r in wl.score_world(v)["risks"]],
            [(2, "partial"), (3, "yes"), (4, "yes")],
        )

    def test_zero_point_item_blocks_strong_status(self):
        v = strong_world()
        v["answers"]["7"]["time_jump"] = "no"
        s = wl.score_world(v)
        lvl7 = next(x for x in s["levels"] if x["num"] == 7)
        self.assertEqual((lvl7["score"], lvl7["status"]), (66.7, "partial"))
        self.assertEqual(s["highest_strong"], 6)
        self.assertEqual([a["level"] for a in s["below_strong_questions"]], [])

    def test_thresholds(self):
        self.assertEqual(wl._level_status(80.0, False), "strong")
        self.assertEqual(wl._level_status(79.9, False), "partial")
        self.assertEqual(wl._level_status(50.0, True), "partial")
        self.assertEqual(wl._level_status(49.9, True), "weak")
        self.assertEqual(wl._level_status(None, False), "na")

    def test_na_excluded_from_scoring(self):
        v = strong_world()
        v["answers"]["1"]["climate"] = "na"
        v["answers"]["1"]["mountains"] = "na"
        v["answers"]["1"]["own_rules"] = "partial"
        s = wl.score_world(v)["levels"][0]
        self.assertEqual((s["score"], s["status"]), (83.3, "strong"))
        all_na = all_status("na")
        self.assertEqual(
            (wl.score_world(all_na)["levels"][0]["score"], wl.score_world(all_na)["levels"][0]["status"]),
            (None, "na"),
        )

    def test_all_na_has_no_next_step(self):
        self.assertIsNone(wl.score_world(all_status("na"))["next_step"])

    def test_answer_dict_and_case_normalization(self):
        status, note = wl.parse_answer({"status": "PARTIAL", "note": " note "}, "x")
        self.assertEqual((status, note), ("partial", "note"))
        self.assertEqual(wl.parse_answer("Yes", "x"), ("yes", ""))
        self.assertEqual(wl.parse_answer("N/A", "x"), ("na", ""))

    def test_invalid_answer(self):
        with self.assertRaises(ValueError) as ctx:
            wl.parse_answer("maybe", "answers.1.climate")
        self.assertIn("answers.1.climate", str(ctx.exception))
        self.assertIn("invalid 'maybe'", str(ctx.exception))

    def test_non_sequential_profile_below_strong_questions(self):
        s = wl.score_world(SAMPLE)
        self.assertEqual(
            [(x["num"], x["score"], x["status"]) for x in s["levels"]],
            [(1, 70.0, "partial"), (2, 37.5, "weak"), (3, 90.0, "strong"), (4, 25.0, "weak"), (5, 83.3, "strong")],
        )
        self.assertEqual((s["highest_strong"], s["unassessed"]), (5, [6, 7]))
        self.assertEqual([a["level"] for a in s["below_strong_questions"]], [1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 4])
        self.assertEqual(
            [a["id"] for a in s["below_strong_questions"]][:5],
            ["mountains", "climate", "defines_identity", "depth_illusion", "structural_gaps"],
        )
        self.assertEqual(len(s["open_questions"]), 13)

    def test_risk_flags(self):
        s = wl.score_world(SAMPLE)
        self.assertEqual([(r["level"], r["status"]) for r in s["risks"]], [(2, "yes"), (2, "yes")])

    def test_next_step(self):
        nxt = wl.score_world(SAMPLE)["next_step"]
        self.assertEqual((nxt["level"], nxt["score"], nxt["id"]), (4, 25.0, "daily_life"))
        self.assertIn("Mistborn", nxt["example"])


class ValidationTests(unittest.TestCase):
    def test_missing_and_invalid_listed(self):
        v = all_status("yes")
        del v["answers"]["3"]["silhouette"]
        v["answers"]["3"]["bogus"] = "yes"
        v["answers"]["9"] = {}
        with self.assertRaises(ValueError) as ctx:
            wl.score_world(v)
        msg = str(ctx.exception)
        self.assertIn("answers.3.silhouette", msg)
        self.assertIn("unknown question(s) bogus", msg)
        self.assertIn("unknown level", msg)

    def test_missing_answers_root(self):
        for bad in ({}, {"answers": {}}, {"answers": {"1": "yes"}}, []):
            with self.assertRaises(ValueError):
                wl.score_world(bad)


class CliTests(unittest.TestCase):
    def test_checklist(self):
        code, out, _ = run_cli(["checklist"])
        self.assertEqual(code, 0)
        tpl = json.loads(out)
        self.assertEqual(list(tpl["answers"]), [str(i) for i in range(1, 8)])
        self.assertEqual(sum(len(x) for x in tpl["answers"].values()), 36)
        code, out, _ = run_cli(["checklist", "--level", "4"])
        self.assertEqual((code, list(json.loads(out)["answers"])), (0, ["4"]))

    def test_sample_file_report(self):
        code, out, _ = run_cli(["evaluate", str(SAMPLE_PATH)])
        self.assertEqual(code, 0)
        self.assertIn("# World Profile: Ash Coasts (sample data)", out)
        self.assertIn("| 2 | Rule of Cool | 37.5/100 | weak |", out)
        self.assertIn("| 4 | Functional Power | 25/100 | weak |", out)
        self.assertIn("| 5 | Deep Culture and History | 83.3/100 | strong |", out)
        self.assertIn("Unassessed: 6, 7", out)
        self.assertIn("Highest strong level: **5. Deep Culture and History**.", out)
        self.assertIn("## Open Questions Below Highest Strong Level (5)", out)
        numbered = [line for line in out.splitlines() if line.split(" ", 1)[0] in {f"{i}." for i in range(1, 12)}]
        self.assertEqual(len(numbered), 11)
        self.assertIn("- [Level 2, yes] Are extra gods and ancient wars", out)
        self.assertIn("Weakest level: **4. Functional Power** (25/100). Start with this question:", out)
        self.assertNotIn("38/100", out)
        self.assertIn("- Who benefits from it?", out)

    def test_output_files(self):
        with tempfile.TemporaryDirectory() as d:
            md, js = Path(d) / "profile.md", Path(d) / "result.json"
            code, out, _ = run_cli(["evaluate", str(SAMPLE_PATH), "--output", str(md), "--json", str(js)])
            self.assertEqual((code, out), (0, ""))
            self.assertIn("# World Profile", md.read_text(encoding="utf-8"))
            self.assertEqual(json.loads(js.read_text(encoding="utf-8"))["highest_strong"], 5)

    def test_error_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "d.json"
            path.write_text("{ bad", encoding="utf-8")
            code, out, err = run_cli(["evaluate", str(path)])
            self.assertEqual((code, out), (2, ""))
            self.assertIn("could not read file", err)

            d2, path2 = temp_json({"world": "X", "answers": {"1": wl.template(1)["answers"]["1"]}})
            with d2:
                code, out, err = run_cli(["evaluate", str(path2)])
                self.assertEqual((code, out), (2, ""))
                self.assertIn("Missing answers", err)
                self.assertIn("answers.1.rivers", err)

            self.assertEqual(run_cli(["evaluate", str(Path(d) / "missing.json")])[0], 2)


if __name__ == "__main__":
    unittest.main()
