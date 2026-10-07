import copy
import json
import unittest
from pathlib import Path

from reasoning_audit import audit, route_effort

BASE = Path(__file__).resolve().parents[1] / "examples"
CASES = json.loads((BASE / "reasoning-cases.json").read_text())
CACHE = json.loads((BASE / "models-cache-sample.json").read_text())


class ReasoningAuditTests(unittest.TestCase):
    def test_two_reported_mismatches_are_detected(self):
        report = audit(CASES, CACHE)
        self.assertEqual(report["status"], "mismatch")
        self.assertEqual([row["observed_route"] for row in report["cases"]], ["low", "max"])
        self.assertTrue(report["cases"][1]["candidate_catalog_differs"])

    def test_matched_route_passes(self):
        cases = copy.deepcopy(CASES)
        cases["cases"][0]["candidate_route"]["effort"] = "none"
        cases["cases"][0]["candidate_route"]["tries"][0]["effort"] = "none"
        cases["cases"][1]["candidate_route"]["effort"] = "xhigh"
        cases["cases"][1]["candidate_route"]["tries"][0]["effort"] = "xhigh"
        self.assertEqual(audit(cases, CACHE)["status"], "matched")

    def test_missing_catalog_or_disagreeing_log_is_inconclusive(self):
        cases = copy.deepcopy(CASES)
        cases["cases"][1]["candidate_slug"] = "unknown"
        self.assertEqual(audit({"cases": [cases["cases"][1]]}, CACHE)["status"], "inconclusive")
        self.assertIsNone(route_effort({"effort": "xhigh", "tries": [{"status": 200, "effort": "max"}]}))

    def test_official_route_must_match_official_catalog(self):
        cases = copy.deepcopy(CASES)
        cases["cases"][1]["baseline_route"]["effort"] = "max"
        cases["cases"][1]["baseline_route"]["tries"][0]["effort"] = "max"
        self.assertEqual(audit({"cases": [cases["cases"][1]]}, CACHE)["status"], "inconclusive")

    def test_failed_try_does_not_claim_upstream_parity(self):
        cases = copy.deepcopy(CASES)
        cases["cases"][0]["candidate_route"]["tries"][0]["status"] = 500
        self.assertEqual(audit({"cases": [cases["cases"][0]]}, CACHE)["status"], "inconclusive")


if __name__ == "__main__":
    unittest.main()
