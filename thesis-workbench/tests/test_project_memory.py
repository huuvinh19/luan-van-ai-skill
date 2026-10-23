from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_prompt import assemble
from project_gate import evaluate_gate


class ProjectMemoryTests(unittest.TestCase):
    def setUp(self):
        demo = ROOT / "examples/demo-project"
        self.profile = json.loads((demo / "project.json").read_text())
        self.state = json.loads((demo / "project_state.json").read_text())

    def test_prompt_must_be_selected_before_asking_for_assignment_bundle(self):
        self.state["active_prompt"] = None
        result = evaluate_gate(self.profile, self.state, "draft")
        self.assertEqual(result["status"], "select_prompt")
        self.assertEqual(result["questions"], [])
        self.assertFalse(result["can_execute"])

    def test_prompt_needs_actual_content_and_valid_task(self):
        for change in ({"content": "  "}, {"reason": ""}, {"task": "bad-task"}):
            state = copy.deepcopy(self.state)
            state["active_prompt"].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError):
                evaluate_gate(self.profile, state, "draft")

    def test_goal_is_asked_without_reasking_supplied_assignment_and_rubric(self):
        self.profile["target_outcome"] = None
        result = evaluate_gate(self.profile, self.state, "draft")
        self.assertEqual([q["id"] for q in result["questions"]], ["target_outcome"])
        self.assertFalse(result["can_execute"])

    def test_missing_plan_selects_outline_instead_of_drafting(self):
        self.state["project_memory"] = None
        result = evaluate_gate(self.profile, self.state, "draft")
        self.assertEqual(result["status"], "plan")
        self.assertFalse(result["can_execute"])
        content = assemble("draft", self.profile, state=self.state)
        self.assertIn("# Lập câu hỏi và dàn ý", content)
        self.assertNotIn("# Viết phần luận văn được giao", content)

    def test_outline_must_cover_every_required_item(self):
        self.state["project_memory"]["requirements"].append({
            "id": "R2", "text": "GIẢ LẬP: giải thích giới hạn", "kind": "required",
            "origin": "Đề giả lập", "check": "Có câu giải thích giới hạn dữ liệu"})
        result = evaluate_gate(self.profile, self.state, "draft")
        self.assertEqual(result["status"], "plan")
        self.assertTrue(any("R2" in gap for gap in result["memory_gaps"]))

    def test_suggestion_does_not_require_a_forced_section(self):
        self.state["project_memory"]["requirements"].append({
            "id": "R2", "text": "GIẢ LẬP: có thể minh họa", "kind": "suggestion",
            "origin": "Gợi ý giả lập", "check": "Tùy phạm vi"})
        result = evaluate_gate(self.profile, self.state, "draft")
        self.assertEqual(result["memory_gaps"], [])
        self.assertEqual(result["status"], "confirm")

    def test_unknown_requirement_or_duplicate_id_is_invalid(self):
        state = copy.deepcopy(self.state)
        state["project_memory"]["outline"][0]["requirement_ids"] = ["R999"]
        with self.assertRaises(ValueError):
            evaluate_gate(self.profile, state, "draft")
        self.state["project_memory"]["requirements"] *= 2
        with self.assertRaises(ValueError):
            evaluate_gate(self.profile, self.state, "draft")

    def test_changed_goal_requires_updated_requirements_and_outline(self):
        self.profile["target_outcome"] = "GIẢ LẬP: đổi mục tiêu sang so sánh hai nhóm"
        result = evaluate_gate(self.profile, self.state, "draft")
        self.assertEqual(result["status"], "plan")

    def test_changed_outline_invalidates_its_previous_confirmation(self):
        self.state["project_memory"]["outline"][0]["title"] += " có nội dung mới"
        self.assertEqual(evaluate_gate(self.profile, self.state, "draft")["status"], "confirm")

    def test_error_log_is_preserved_without_restarting_confirmed_work(self):
        self.state["known_errors"].append("GIẢ LẬP: kiểm tra lại mẫu số trước khi tính tỷ lệ.")
        self.assertEqual(evaluate_gate(self.profile, self.state, "review")["status"], "ready")
        content = assemble("review", self.profile, state=self.state)
        self.assertIn(self.state["known_errors"][-1], content)
        self.assertIn(self.state["active_prompt"]["content"].splitlines()[0], content)


if __name__ == "__main__":
    unittest.main()
