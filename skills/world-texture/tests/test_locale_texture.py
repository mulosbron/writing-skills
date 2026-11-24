#!/usr/bin/env python3
"""Unit tests for world-texture locale_texture.py. Run: python -m unittest tests/test_locale_texture.py"""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import locale_texture as lt  # noqa: E402

SAMPLE_PATH = ROOT / "assets" / "sample_locale.json"
SAMPLE = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))


def run_cli(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = lt.main(argv)
    return code, out.getvalue(), err.getvalue()


def make_locale(status="present", detail="Concrete flavor", hook="Actionable hook"):
    tpl = lt.template()
    tpl["locale"] = "Test Town"
    tpl["education_lens"] = "Scholars know the runes."
    tpl["lifespan_lens"] = "Elves remember the siege."
    for did in tpl["details"]:
        tpl["details"][did] = {
            "status": status,
            "detail": detail if status in ("present", "sketch") else "",
            "hook": hook if status in ("present", "sketch") else "",
        }
    return tpl


class TemplateAndBankTests(unittest.TestCase):
    def test_ten_details_across_three_layers(self):
        self.assertEqual(len(lt.LAYERS), 3)
        self.assertEqual([len(layer["details"]) for layer in lt.LAYERS], [3, 4, 3])
        self.assertEqual(len(lt.DETAIL_ORDER), 10)
        self.assertEqual(len(set(lt.DETAIL_ORDER)), 10)

    def test_template_cli_outputs_valid_json(self):
        code, out, _ = run_cli(["template"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(list(data["details"]), lt.DETAIL_ORDER)
        self.assertIn("_help", data)


class ScoringAndWarningsTests(unittest.TestCase):
    def test_all_present_scores_100_with_no_warnings(self):
        res = lt.audit_locale(make_locale("present"))
        self.assertEqual(res["total_score"], 100.0)
        self.assertTrue(all(lr["score"] == 100.0 for lr in res["layers"]))
        self.assertEqual(res["warnings"], [])
        self.assertEqual(res["top_priorities"], [])

    def test_sample_locale_scores_and_flags_untestable_superstition(self):
        res = lt.audit_locale(SAMPLE)
        layers = {lr["id"]: lr["score"] for lr in res["layers"]}
        # voice_custom: present(2) + present(2) + sketch(1) = 5/6 -> 83.3
        self.assertEqual(layers["voice_custom"], 83.3)
        # physical_memory: 2 + 0 + 2 + 0 = 4/8 -> 50.0
        self.assertEqual(layers["physical_memory"], 50.0)
        # people_legend: 2 + 1 + na = 3/4 -> 75.0
        self.assertEqual(layers["people_legend"], 75.0)
        # total: 12 / 18 -> 66.7
        self.assertEqual(res["total_score"], 66.7)
        codes = [w["code"] for w in res["warnings"]]
        self.assertEqual(codes, ["untestable_superstition"])
        # Weakest layer (physical_memory) appears first in top_priorities
        self.assertEqual(res["top_priorities"][0]["layer"], "Physical Memory")

    def test_na_excluded_from_layer_and_total(self):
        loc = make_locale("present")
        for did in ("famous_monuments", "war_memorials", "scarred_landscapes", "unique_animals"):
            loc["details"][did] = {"status": "na", "detail": "", "hook": ""}
        res = lt.audit_locale(loc)
        layers = {lr["id"]: lr["score"] for lr in res["layers"]}
        self.assertIsNone(layers["physical_memory"])
        self.assertEqual(res["total_score"], 100.0)

    def test_missing_lenses_and_incomplete_culture_combo_warn(self):
        loc = make_locale("present")
        loc["education_lens"] = ""
        loc["lifespan_lens"] = ""
        loc["details"]["regional_superstitions"] = {"status": "absent", "detail": "", "hook": ""}
        codes = {w["code"] for w in lt.audit_locale(loc)["warnings"]}
        self.assertEqual(codes, {"missing_education_lens", "missing_lifespan_lens", "culture_combo_incomplete"})

    def test_shorthand_string_absent_and_na(self):
        loc = make_locale("present")
        loc["details"]["war_memorials"] = "absent"
        loc["details"]["famous_orders"] = "N/A"
        res = lt.audit_locale(loc)
        self.assertEqual(res["layers"][1]["score"], 75.0)
        self.assertEqual(res["layers"][2]["score"], 100.0)


class ValidationAndCliTests(unittest.TestCase):
    def test_missing_and_invalid_entries_listed(self):
        loc = make_locale("present")
        del loc["details"]["war_memorials"]
        loc["details"]["unique_animals"] = {"status": "present", "detail": "", "hook": ""}
        loc["details"]["local_heroes"] = {"status": "maybe", "detail": "x", "hook": ""}
        loc["details"]["extra"] = "absent"
        with self.assertRaises(ValueError) as ctx:
            lt.audit_locale(loc)
        msg = str(ctx.exception)
        self.assertIn("details.war_memorials", msg)
        self.assertIn("'detail' text is empty", msg)
        self.assertIn("invalid status 'maybe'", msg)
        self.assertIn("unknown key(s) extra", msg)

    def test_cli_outputs_and_min_score_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            md, js = Path(d) / "card.md", Path(d) / "out.json"
            code, out, _ = run_cli(["audit", str(SAMPLE_PATH), "--output", str(md), "--json", str(js)])
            self.assertEqual((code, out), (0, ""))
            text = md.read_text(encoding="utf-8")
            self.assertIn("# Locale Texture Card: Cinderport (sample data)", text)
            self.assertIn("## Top 3 High-Impact Additions", text)
            self.assertEqual(json.loads(js.read_text(encoding="utf-8"))["total_score"], 66.7)

            code, _, err = run_cli(["audit", str(SAMPLE_PATH), "--min-score", "75"])
            self.assertEqual(code, 1)
            self.assertIn("below minimum (75.0)", err)

            self.assertEqual(run_cli(["audit", str(Path(d) / "missing.json")])[0], 2)


if __name__ == "__main__":
    unittest.main()
