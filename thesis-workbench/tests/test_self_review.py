from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_self_review import REVIEW_AREAS, audit_review
from build_prompt import TASKS, assemble


class SelfReviewTests(unittest.TestCase):
    def setUp(self):
        self.report = {
            "scope": "GIẢ LẬP: kiểm tra một tiêu chí",
            "artifact": "artifact-demo", "review_basis": "Yêu cầu GIẢ LẬP",
            "reviewer_mode": "same_assistant_separate_pass",
            "criteria": [{"id": "R1", "criterion": "Tiêu chí GIẢ LẬP", "judgment": "met",
                          "evidence": "Vị trí minh họa GIẢ LẬP", "reason": "Lý do minh họa"}],
            "findings": [], "remaining_limits": [], "overall_verdict": "ready_for_scope",
            "grade": None, "grading_basis": None,
        }

    def codes(self):
        return {item["code"] for item in audit_review(self.report)["issues"]}

    def academic_report(self):
        self.report["review_type"] = "academic"
        original = self.report["criteria"][0]
        self.report["criteria"] = [dict(original, id=f"R{i}", review_area=area)
                                   for i, area in enumerate(sorted(REVIEW_AREAS), 1)]
        return self.report

    def test_academic_review_records_all_five_areas_with_explicit_semantic_limit(self):
        result = audit_review(self.academic_report())
        self.assertEqual(result["mechanical_status"], "clear")
        self.assertEqual(result["semantic_checks"], "not_performed")

    def test_academic_review_cannot_hide_a_missing_area_behind_ready(self):
        self.academic_report()["criteria"].pop()
        self.assertTrue({"missing_review_areas", "premature_ready_verdict"}.issubset(self.codes()))

    def test_academic_review_rejects_unknown_or_malformed_area(self):
        for area in ("layout-only", None, ["content"]):
            self.academic_report()["criteria"][0]["review_area"] = area
            with self.subTest(area=area):
                self.assertIn("invalid_review_area", self.codes())

    def test_unchecked_formatting_remains_disclosed_without_claiming_readiness(self):
        self.academic_report()
        item = next(c for c in self.report["criteria"] if c["review_area"] == "language_presentation")
        item.update(judgment="not_checked", evidence="", reason="Chỉ có văn bản giả lập, không có tệp.",
                    next_action="Cần xem tệp hoặc bản render để kiểm tra bố cục.")
        self.report.update(overall_verdict="not_fully_checked", remaining_limits=["Chưa xem tệp/bản render."])
        self.assertEqual(audit_review(self.report)["mechanical_status"], "clear")
        self.report["overall_verdict"] = "ready_for_scope"
        self.assertIn("premature_ready_verdict", self.codes())

    def test_cli_flags_academic_report_with_missing_area(self):
        self.academic_report()["criteria"].pop()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(json.dumps(self.report), encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/audit_self_review.py"),
                                     "--report", str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("missing_review_areas", {x["code"] for x in json.loads(result.stdout)["issues"]})

    def test_consistent_review_is_clear_without_inventing_grade(self):
        result = audit_review(self.report)
        self.assertEqual(result["mechanical_status"], "clear")
        self.assertEqual(result["semantic_checks"], "not_performed")
        self.assertIsNone(self.report["grade"])

    def test_ready_despite_unmet_criterion_is_rejected(self):
        self.report["criteria"][0].update(judgment="not_met", next_action="Cần sửa phần GIẢ LẬP")
        self.assertIn("premature_ready_verdict", self.codes())

    def test_grade_without_provided_scale_is_rejected(self):
        self.report["grade"] = {"value": "D", "criterion_ids": ["R1"]}
        self.assertIn("unsupported_grade", self.codes())

    def test_met_without_evidence_is_rejected(self):
        self.report["criteria"][0]["evidence"] = ""
        self.assertIn("missing_review_evidence", self.codes())

    def test_resolved_finding_requires_recheck_evidence(self):
        self.report["findings"] = [{"id": "F1", "severity": "minor", "location": "Vị trí GIẢ LẬP",
                                    "issue": "Lỗi GIẢ LẬP", "action": "Đã sửa GIẢ LẬP", "status": "resolved"}]
        self.assertIn("unverified_fix", self.codes())

    def test_open_finding_prevents_ready(self):
        self.report["findings"] = [{"id": "F1", "severity": "major", "location": "Vị trí GIẢ LẬP",
                                    "issue": "Lỗi GIẢ LẬP", "action": "Cần sửa", "status": "open"}]
        self.assertIn("premature_ready_verdict", self.codes())

    def test_unchecked_item_cannot_be_hidden(self):
        self.report["criteria"][0].update(judgment="not_checked", next_action="Cần đọc bằng chứng")
        self.report["overall_verdict"] = "not_fully_checked"
        self.assertIn("undisclosed_unchecked_item", self.codes())

    def test_duplicate_criterion_and_unknown_grade_basis_are_rejected(self):
        self.report["criteria"].append(copy.deepcopy(self.report["criteria"][0]))
        self.report["grading_basis"] = {"provided": True, "source": "Rubric GIẢ LẬP", "scale": "P/M/D"}
        self.report["grade"] = {"value": "D", "criterion_ids": ["UNKNOWN"]}
        self.assertTrue({"invalid_criterion_id", "grade_without_criteria"}.issubset(self.codes()))

    def test_candid_review_policy_is_wired_into_every_task(self):
        for task in TASKS:
            with self.subTest(task=task):
                content = assemble(task)
                self.assertIn("# Phản biện có căn cứ, trò chuyện có cá tính và tự rà công tâm", content)


if __name__ == "__main__":
    unittest.main()
