from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_prompt import TASKS, assemble
from project_gate import TASK_NAMES, brief_fingerprint, evaluate_gate, profile_fingerprint


class ProjectGateTests(unittest.TestCase):
    def setUp(self):
        self.profile = json.loads((ROOT / "examples/demo-project/project.json").read_text(encoding="utf-8"))
        self.state = json.loads((ROOT / "examples/demo-project/project_state.json").read_text(encoding="utf-8"))

    def resign_test_state(self):
        # All confirmations in these fixtures are explicitly synthetic test data.
        self.state["user_confirmation"]["profile_sha256"] = profile_fingerprint(self.profile)
        self.state["user_confirmation"]["brief_sha256"] = brief_fingerprint(self.state["brief_summary"])

    def test_blank_context_asks_in_rounds_and_cannot_execute(self):
        result = evaluate_gate(None, None, "draft")
        self.assertEqual(result["status"], "clarify")
        self.assertFalse(result["can_execute"])
        self.assertEqual([q["id"] for q in result["questions"]], ["course", "discipline"])
        self.assertEqual(result["intake_stage"], "course_and_discipline")
        self.assertGreater(result["remaining_blocker_count"], 0)

    def test_it_discipline_is_reused_while_course_is_unknown(self):
        result = evaluate_gate({"discipline": "Công nghệ thông tin"}, None, "draft")
        self.assertEqual([q["id"] for q in result["questions"]], ["course"])
        self.assertFalse(result["can_execute"])
        self.assertIn("topic", {q["id"] for q in result["all_blockers"]})

    def test_course_code_does_not_infer_discipline(self):
        result = evaluate_gate({"course_code": "DEMO-IT-01"}, None, "review")
        self.assertEqual([q["id"] for q in result["questions"]], ["discipline"])
        self.assertFalse(result["can_execute"])

    def test_confirmed_it_project_is_supported_without_marketing_default(self):
        self.profile["discipline"] = "Công nghệ thông tin"
        self.profile["course_name"] = "Cơ sở dữ liệu (GIẢ LẬP)"
        self.resign_test_state()
        result = evaluate_gate(self.profile, self.state, "draft")
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["questions"], [])

    def test_course_or_discipline_change_requires_new_confirmation(self):
        for field, value in (("course_name", "Môn mới (GIẢ LẬP)"),
                             ("discipline", "Công nghệ thông tin")):
            with self.subTest(field=field):
                profile = copy.deepcopy(self.profile)
                profile[field] = value
                self.assertEqual(evaluate_gate(profile, self.state, "draft")["status"], "confirm")

    def test_template_does_not_preselect_the_users_discipline(self):
        template = json.loads((ROOT / "templates/project.json").read_text(encoding="utf-8"))
        self.assertIsNone(template["discipline"])
        result = evaluate_gate(template, None, "general")
        self.assertEqual([q["id"] for q in result["questions"]], ["course", "discipline"])

    def test_following_round_asks_project_details_after_course_and_discipline(self):
        profile = {"course_name": "Software Engineering (GIẢ LẬP)", "discipline": "IT"}
        result = evaluate_gate(profile, None, "draft")
        self.assertEqual(result["intake_stage"], "project_details")
        self.assertEqual([q["id"] for q in result["questions"]], ["topic", "scope", "format"])
        self.assertGreater(result["remaining_blocker_count"], 0)
        self.assertNotIn("course", {q["id"] for q in result["all_blockers"]})
        self.assertNotIn("discipline", {q["id"] for q in result["all_blockers"]})

    def test_complete_fields_without_confirmation_still_wait(self):
        self.assertEqual(evaluate_gate(self.profile, None, "draft")["status"], "confirm")

    def test_confirmed_unchanged_project_continues_across_tasks(self):
        for task in ("draft", "review", "citations", "analysis"):
            with self.subTest(task=task):
                result = evaluate_gate(self.profile, self.state, task)
                self.assertEqual(result["status"], "ready")
                self.assertEqual(result["questions"], [])

    def test_changed_topic_invalidates_old_confirmation(self):
        self.profile["topic"] = "Đề tài GIẢ LẬP khác"
        self.assertEqual(evaluate_gate(self.profile, self.state, "draft")["status"], "confirm")

    def test_changed_brief_invalidates_old_confirmation(self):
        self.state["brief_summary"] += " Phạm vi GIẢ LẬP mới."
        self.assertEqual(evaluate_gate(self.profile, self.state, "draft")["status"], "confirm")

    def test_changed_context_revision_invalidates_old_confirmation(self):
        self.profile["context_revision"] += 1
        self.assertEqual(evaluate_gate(self.profile, self.state, "review")["status"], "confirm")

    def test_open_question_blocks_affected_task_only(self):
        self.state["open_questions"] = [{"id": "Q001", "question": "Mã biến GIẢ LẬP nào đang đúng?",
                                         "status": "open", "blocking": True, "affects": ["analysis"]}]
        result = evaluate_gate(self.profile, self.state, "analysis")
        self.assertEqual(result["status"], "clarify")
        self.assertEqual(result["questions"][0]["id"], "open:Q001")
        self.assertEqual(evaluate_gate(self.profile, self.state, "review")["status"], "ready")

    def test_resolved_question_with_answer_is_not_asked_again(self):
        self.state["open_questions"] = [{"id": "Q001", "question": "Tên biến GIẢ LẬP?",
                                         "status": "resolved", "blocking": True, "affects": ["analysis"],
                                         "answer": "GIẢ LẬP: value, đã có trong data_demo.csv."}]
        self.assertEqual(evaluate_gate(self.profile, self.state, "analysis")["questions"], [])

    def test_resolved_without_answer_is_invalid(self):
        self.state["open_questions"] = [{"id": "Q001", "question": "Câu hỏi GIẢ LẬP?", "status": "resolved"}]
        with self.assertRaises(ValueError):
            evaluate_gate(self.profile, self.state, "draft")

    def test_unknown_question_task_is_rejected(self):
        self.state["open_questions"] = [{"id": "Q001", "question": "Câu hỏi GIẢ LẬP?",
                                         "status": "open", "affects": ["analysiss"]}]
        with self.assertRaises(ValueError):
            evaluate_gate(self.profile, self.state, "analysis")

    def test_unknown_task_is_rejected_even_with_confirmed_profile(self):
        for task in ("analysiss", "", None, ["draft"]):
            with self.subTest(task=task), self.assertRaises(ValueError):
                evaluate_gate(self.profile, self.state, task)

    def test_invalid_profiles_are_rejected_by_gate_and_assembler(self):
        for profile in ([], "not an object", {"assignment_status": "self_defined", "assignment_notes": 123},
                        {"rubric_status": "provided", "rubric_notes": 123},
                        {"citation_style": []}, {"assignment_materials": [1]}):
            for operation in (lambda: evaluate_gate(profile, None, "draft"),
                              lambda: assemble("draft", profile)):
                with self.subTest(profile=profile), self.assertRaises(ValueError):
                    operation()

    def test_state_version_must_be_integer_one(self):
        for value in (True, 1.0, "1", None, 2):
            self.state["schema_version"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                evaluate_gate(self.profile, self.state, "draft")

    def test_blank_assignment_entry_does_not_pass_gate(self):
        self.profile["assignment_status"] = "provided"
        self.profile["assignment_materials"] = ["   ", "\t"]
        self.resign_test_state()
        result = evaluate_gate(self.profile, self.state, "draft")
        self.assertFalse(result["can_execute"])
        self.assertIn("assignment", {q["id"] for q in result["all_blockers"]})

    def test_task_names_agree_between_state_and_builder(self):
        self.assertEqual(TASK_NAMES, set(TASKS))

    def test_future_questions_are_preserved_in_general_prompt(self):
        self.state["open_questions"] = [{"id": "Q001", "question": "Cần hỏi khi tới phân tích GIẢ LẬP",
                                         "status": "open", "blocking": True, "affects": ["analysis"]}]
        content = assemble("general", self.profile, state=self.state)
        self.assertIn("Cần hỏi khi tới phân tích GIẢ LẬP", content)
        self.assertIn(self.state["brief_summary"], content)

    def test_no_response_is_not_confirmation(self):
        self.state["user_confirmation"]["message"] = ""
        self.assertEqual(evaluate_gate(self.profile, self.state, "draft")["status"], "confirm")

    def test_missing_data_blocks_analysis(self):
        self.profile["data_status"] = "not_provided"
        self.profile["data_notes"] = None
        self.resign_test_state()
        self.assertEqual(evaluate_gate(self.profile, self.state, "analysis")["status"], "clarify")
        self.assertEqual(evaluate_gate(self.profile, self.state, "review")["status"], "ready")

    def test_build_replaces_draft_module_with_clarification(self):
        content = assemble("draft", self.profile, request="Làm luôn {{topic}} với ${data}")
        self.assertIn("# Làm rõ dự án trước khi triển khai", content)
        self.assertNotIn("# Viết phần luận văn được giao", content)
        self.assertIn("Làm luôn {{topic}} với ${data}", content)
        self.assertIn('"status": "confirm"', content)

    def test_ready_build_uses_requested_module(self):
        content = assemble("draft", self.profile, state=self.state)
        self.assertIn("# Viết phần luận văn được giao", content)
        self.assertIn('"status": "ready"', content)

    def test_optimize_only_does_not_execute_underlying_thesis(self):
        result = evaluate_gate(None, None, "optimize")
        self.assertEqual(result["status"], "prompt_only")
        content = assemble("optimize", request="Viết một luận văn GIẢ LẬP")
        self.assertIn("# Chỉ tối ưu prompt được cung cấp", content)
        self.assertNotIn("# Viết phần luận văn được giao", content)

    def test_cli_blocked_ready_and_invalid_states(self):
        script = str(ROOT / "scripts/project_gate.py")
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            shutil.copytree(ROOT / "examples/demo-project", project)
            ready = subprocess.run([sys.executable, script, "--project", str(project), "--task", "review"], capture_output=True, text=True)
            self.assertEqual(ready.returncode, 0, ready.stderr)
            self.assertEqual(json.loads(ready.stdout)["status"], "ready")
            (project / "project_state.json").unlink()
            waiting = subprocess.run([sys.executable, script, "--project", str(project)], capture_output=True, text=True)
            self.assertEqual(waiting.returncode, 1, waiting.stderr)
            self.assertEqual(json.loads(waiting.stdout)["status"], "confirm")
            (project / "project_state.json").write_text("[]", encoding="utf-8")
            invalid = subprocess.run([sys.executable, script, "--project", str(project)], capture_output=True, text=True)
            self.assertEqual(invalid.returncode, 2)


if __name__ == "__main__":
    unittest.main()
