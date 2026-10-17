from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_self_review import audit_review
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
