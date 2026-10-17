from __future__ import annotations

import csv
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_prompt import TASKS, assemble, load_profile
from audit_project import audit
from verify_repo import verify


class PromptTests(unittest.TestCase):
    def test_all_tasks_include_rules_and_resolve_style(self):
        for task in TASKS:
            with self.subTest(task=task):
                content = assemble(task)
                self.assertIn("Dùng thống nhất chuẩn Harvard", content)
                self.assertIn("trước dấu chấm", content)
                self.assertNotIn("{{CITATION_STYLE}}", content)

    def test_apa_profile_changes_active_instruction_and_preserves_context(self):
        profile = {"citation_style": "APA", "topic": "Đo {{metric}} cho ${market}",
                   "current_scope": "Giữ nguyên dữ liệu", "word_limit": 2000}
        content = assemble("review", profile)
        self.assertIn("Dùng thống nhất chuẩn APA", content)
        self.assertNotIn("Dùng thống nhất chuẩn Harvard", content)
        self.assertIn("{{metric}}", content)
        self.assertIn("${market}", content)
        self.assertIn(json.dumps(profile, ensure_ascii=False, indent=2), content)

    def test_invalid_profiles_and_task_fail(self):
        with self.assertRaises(ValueError):
            assemble("unknown")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "profile.json"
            for value in ([1], {"citation_style": "Harvard APA"}, {"word_limit": True},
                          {"word_limit": -1}, {"topic": [1]}, {"assignment_materials": "a.pdf"}):
                with self.subTest(value=value):
                    path.write_text(json.dumps(value), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        load_profile(path)

    def test_cli_writes_exact_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nested/prompt.md"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/build_prompt.py"),
                                     "--task", "analysis", "--out", str(out)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(out.read_text(encoding="utf-8"), assemble("analysis"))


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "project"
        shutil.copytree(ROOT / "examples/demo-project", self.project)

    def tearDown(self):
        self.tmp.cleanup()

    def write_rows(self, name, rows, fields):
        with (self.project / name).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def external_claim(self, source_id="S001"):
        row = {"claim_id": "C001", "text": "Nhận định giả lập dùng trong test",
               "claim_type": "external", "source_ids": source_id,
               "support_status": "supported", "evidence_locations": "Vị trí giả lập"}
        self.write_rows("claims.csv", [row], list(row))

    def test_demo_records_clear_with_explicit_semantic_limit(self):
        result = audit(self.project)
        self.assertEqual(result["mechanical_status"], "clear")
        self.assertEqual(result["semantic_checks"], "not_performed")
        self.assertTrue(result["limits"])

    def test_missing_source_is_detected(self):
        self.external_claim()
        codes = {x["code"] for x in audit(self.project)["issues"]}
        self.assertIn("unknown_source", codes)

    def test_metadata_only_does_not_support_claim(self):
        self.external_claim()
        source = {"id": "S001", "authors": ["Tác giả GIẢ LẬP"], "year": "2026",
                  "title": "Nguồn giả lập dùng trong unit test", "source_type": "report",
                  "verification_status": "metadata_only", "checked_locations": [],
                  "reference_entry": "Entry giả lập dùng trong unit test"}
        (self.project / "sources.json").write_text(json.dumps([source]), encoding="utf-8")
        codes = {x["code"] for x in audit(self.project)["issues"]}
        self.assertIn("source_not_content_checked", codes)

    def test_content_checked_without_location_and_duplicate_ids_fail(self):
        source = {"id": "S001", "authors": ["Tác giả GIẢ LẬP"], "year": "2026",
                  "title": "Nguồn giả lập", "source_type": "report",
                  "verification_status": "content_checked", "checked_locations": []}
        (self.project / "sources.json").write_text(json.dumps([source, source]), encoding="utf-8")
        codes = {x["code"] for x in audit(self.project)["issues"]}
        self.assertIn("missing_checked_location", codes)
        self.assertIn("duplicate_source_id", codes)

    def test_requirement_without_evidence_fails(self):
        row = {"requirement_id": "R1", "requirement_text": "Yêu cầu giả lập", "kind": "required",
               "criterion": "", "section": "II", "status": "covered", "evidence": ""}
        self.write_rows("requirements.csv", [row], list(row))
        codes = {x["code"] for x in audit(self.project)["issues"]}
        self.assertIn("missing_requirement_evidence", codes)

    def test_unresolved_claim_and_unmet_requirement_fail(self):
        self.external_claim("")
        path = self.project / "claims.csv"
        path.write_text(path.read_text(encoding="utf-8").replace("supported", "pending"), encoding="utf-8")
        row = {"requirement_id": "R1", "requirement_text": "Yêu cầu giả lập", "kind": "required",
               "criterion": "", "section": "II", "status": "partial", "evidence": "Chưa xong"}
        self.write_rows("requirements.csv", [row], list(row))
        codes = {x["code"] for x in audit(self.project)["issues"]}
        self.assertTrue({"unresolved_claim", "unmet_requirement", "external_without_source"}.issubset(codes))

    def test_cli_exit_codes_are_distinct(self):
        script = str(ROOT / "scripts/audit_project.py")
        ok = subprocess.run([sys.executable, script, "--project", str(self.project)], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.external_claim()
        findings = subprocess.run([sys.executable, script, "--project", str(self.project)], capture_output=True, text=True)
        self.assertEqual(findings.returncode, 1)
        self.assertEqual(json.loads(findings.stdout)["mechanical_status"], "findings")
        (self.project / "sources.json").write_text("{bad-json", encoding="utf-8")
        error = subprocess.run([sys.executable, script, "--project", str(self.project)], capture_output=True, text=True)
        self.assertEqual(error.returncode, 2)
        self.assertEqual(json.loads(error.stdout)["mechanical_status"], "error")


class RepositoryTests(unittest.TestCase):
    def test_repository_is_consistent(self):
        self.assertEqual(verify(), [])

    def test_tampered_snapshot_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "output"))
            path = copy / "upstream/selected-prompts.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            data[0]["prompt"] += " changed"
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("Snapshot" in error for error in verify(copy)))

    def test_stale_generated_prompt_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__", "output"))
            path = copy / "rules/core.vi.md"
            path.write_text(path.read_text(encoding="utf-8") + "\nQuy tắc mới.\n", encoding="utf-8")
            self.assertTrue(any("chưa được sinh lại" in error for error in verify(copy)))


if __name__ == "__main__":
    unittest.main()
