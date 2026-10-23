#!/usr/bin/env python3
"""Read declared project state and decide clarify/confirm/ready; no model calls."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

TASK_NAMES = {"general", "intake", "outline", "sources", "literature", "methodology",
              "analysis", "draft", "review", "citations", "translate", "export", "optimize", "clarify", "self-review"}


def validate_profile(profile: dict) -> None:
    """Validate the same input contract for both CLI and imported callers."""
    if not isinstance(profile, dict):
        raise ValueError("Hồ sơ phải là một JSON object.")
    if profile.get("citation_style", "Harvard") not in ("Harvard", "APA"):
        raise ValueError("citation_style chỉ nhận Harvard hoặc APA.")
    limit = profile.get("word_limit")
    if limit is not None and (type(limit) is not int or limit <= 0):
        raise ValueError("word_limit phải là số nguyên dương hoặc null.")
    for field in ("author", "institution", "discipline", "course_code", "course_name",
                  "topic", "research_question", "current_scope", "language",
                  "instructor_citation_guide", "target_language", "output_format",
                  "assignment_status", "assignment_notes", "rubric_status", "rubric_notes",
                  "data_status", "data_notes", "target_outcome"):
        value = profile.get(field)
        if value is not None and not isinstance(value, str):
            raise ValueError(f"{field} phải là chuỗi hoặc null.")
    materials = profile.get("assignment_materials", [])
    if not isinstance(materials, list) or not all(isinstance(x, str) for x in materials):
        raise ValueError("assignment_materials phải là danh sách chuỗi.")
    if "context_revision" in profile and (type(profile["context_revision"]) is not int or profile["context_revision"] < 1):
        raise ValueError("context_revision phải là số nguyên dương.")


def profile_fingerprint(profile: dict) -> str:
    canonical = json.dumps(profile, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def brief_fingerprint(summary: str) -> str:
    return hashlib.sha256(summary.encode("utf-8")).hexdigest()


def memory_fingerprint(state: dict) -> str:
    return profile_fingerprint(state.get("project_memory"))


def validate_memory(state: dict) -> None:
    prompt = state.get("active_prompt")
    if prompt is not None:
        if not isinstance(prompt, dict):
            raise ValueError("active_prompt phải là object hoặc null.")
        for field in ("task", "reason", "content"):
            if not isinstance(prompt.get(field), str) or not prompt[field].strip():
                raise ValueError(f"active_prompt.{field} phải có nội dung.")
        if prompt["task"] not in TASK_NAMES:
            raise ValueError("active_prompt.task không hợp lệ.")
    errors = state.get("known_errors", [])
    if not isinstance(errors, list) or not all(isinstance(x, str) and x.strip() for x in errors):
        raise ValueError("known_errors phải là danh sách chuỗi có nội dung.")
    memory = state.get("project_memory")
    if memory is None:
        return
    if not isinstance(memory, dict) or not isinstance(memory.get("profile_sha256"), str):
        raise ValueError("project_memory cần object có profile_sha256.")
    ids = set()
    for key, fields in (("requirements", ("id", "text", "origin", "check")),
                        ("outline", ("id", "title", "evidence_needed"))):
        rows = memory.get(key)
        if not isinstance(rows, list):
            raise ValueError(f"project_memory.{key} phải là danh sách.")
        seen = set()
        for row in rows:
            if not isinstance(row, dict) or any(not isinstance(row.get(f), str) or not row[f].strip() for f in fields):
                raise ValueError(f"Mỗi mục {key} cần {', '.join(fields)} có nội dung.")
            if row["id"] in seen:
                raise ValueError(f"ID trong {key} không được trùng.")
            seen.add(row["id"])
            if key == "requirements":
                if row.get("kind") not in ("required", "suggestion"):
                    raise ValueError("Yêu cầu phải phân biệt required hoặc suggestion.")
                ids.add(row["id"])
            else:
                refs = row.get("requirement_ids")
                if not isinstance(refs, list) or not refs or not all(isinstance(x, str) and x in ids for x in refs):
                    raise ValueError("Mỗi mục dàn ý cần liên kết mã yêu cầu thực sự có trong hồ sơ.")


def memory_gaps(state: dict | None, digest: str) -> list[str]:
    memory = (state or {}).get("project_memory")
    if not memory:
        return ["Chưa bóc tách yêu cầu và lập dàn ý."]
    gaps = []
    if memory["profile_sha256"] != digest:
        gaps.append("Đề/mục tiêu/phạm vi đã đổi; cần cập nhật bảng yêu cầu và dàn ý.")
    if not memory["requirements"] or not memory["outline"]:
        gaps.append("Bảng yêu cầu và dàn ý chưa có nội dung.")
    covered = {rid for section in memory["outline"] for rid in section["requirement_ids"]}
    missing = [r["id"] for r in memory["requirements"] if r["kind"] == "required" and r["id"] not in covered]
    if missing:
        gaps.append("Dàn ý chưa bao phủ yêu cầu bắt buộc: " + ", ".join(missing))
    return gaps


def load_state(path: Path) -> dict:
    state = json.loads(path.read_text(encoding="utf-8-sig"))
    validate_state(state)
    return state


def validate_state(state: dict) -> None:
    if not isinstance(state, dict) or type(state.get("schema_version")) is not int or state["schema_version"] != 1:
        raise ValueError("project_state.json cần object có schema_version=1.")
    validate_memory(state)
    summary = state.get("brief_summary")
    if summary is not None and not isinstance(summary, str):
        raise ValueError("brief_summary phải là chuỗi hoặc null.")
    confirmation = state.get("user_confirmation")
    if confirmation is not None:
        if not isinstance(confirmation, dict):
            raise ValueError("user_confirmation phải là object hoặc null.")
        for field in ("message", "profile_sha256", "brief_sha256"):
            if not isinstance(confirmation.get(field), str):
                raise ValueError(f"user_confirmation.{field} phải là chuỗi.")
    questions = state.get("open_questions", [])
    if not isinstance(questions, list):
        raise ValueError("open_questions phải là danh sách.")
    seen = set()
    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Mỗi câu hỏi phải là object.")
        qid = question.get("id")
        if not isinstance(qid, str) or not qid.strip() or qid in seen:
            raise ValueError("ID câu hỏi phải có nội dung và không trùng.")
        seen.add(qid)
        if not isinstance(question.get("question"), str) or not question["question"].strip():
            raise ValueError(f"Câu hỏi {qid} thiếu nội dung.")
        if question.get("status") not in ("open", "resolved"):
            raise ValueError(f"Câu hỏi {qid} có status không hợp lệ.")
        if type(question.get("blocking", True)) is not bool:
            raise ValueError(f"Câu hỏi {qid}: blocking phải là boolean.")
        affects = question.get("affects", [])
        if not isinstance(affects, list) or not all(isinstance(x, str) for x in affects):
            raise ValueError(f"Câu hỏi {qid}: affects phải là danh sách chuỗi.")
        if any(task not in TASK_NAMES for task in affects):
            raise ValueError(f"Câu hỏi {qid}: affects chứa tên công đoạn không hợp lệ.")
        if question["status"] == "resolved" and not (
            isinstance(question.get("answer"), str) and question["answer"].strip()
        ):
            raise ValueError(f"Câu hỏi {qid} đã ghi resolved nhưng thiếu câu trả lời.")


def evaluate_gate(profile: dict | None, state: dict | None, task: str) -> dict:
    profile = {} if profile is None else profile
    validate_profile(profile)
    if not isinstance(task, str) or task not in TASK_NAMES:
        raise ValueError(f"Không có công đoạn {task!r}.")
    if state is not None:
        validate_state(state)
    digest = profile_fingerprint(profile)
    if task == "optimize":
        return {
            "status": "prompt_only", "can_execute": True, "requested_task": task,
            "profile_sha256": digest, "questions": [], "all_blockers": [],
            "semantic_verification": "not_performed",
            "next_action": "Chỉ tối ưu prompt; chưa được thực hiện bài luận bên trong prompt.",
        }
    blockers = []

    def ask(qid: str, question: str, reason: str) -> None:
        blockers.append({"id": qid, "question": question, "reason": reason})

    course_known = any(isinstance(profile.get(field), str) and profile[field].strip()
                       for field in ("course_name", "course_code"))
    if not course_known:
        ask("course", "Mày đang làm luận cho môn nào? Cho tao tên môn, mã môn nếu có.",
            "Cần xác định môn trước khi chọn cách hỗ trợ dự án.")
    if not isinstance(profile.get("discipline"), str) or not profile["discipline"].strip():
        ask("discipline", "Mày học ngành hoặc chuyên ngành gì?",
            "Không mặc định Marketing, IT hoặc suy ra ngành từ mã môn.")
    identity_questions = list(blockers)

    for field, qid, question in (
        ("topic", "topic", "Dự án đang về vấn đề/đề tài nào, hoặc mày đang cần cùng chọn đề tài?"),
        ("current_scope", "scope", "Phạm vi đang giao là toàn bài hay phần nào, và cần kết quả gì?"),
        ("output_format", "format", "Đầu ra cần là nội dung trong chat, Word, PDF hay dạng nào?"),
    ):
        if not isinstance(profile.get(field), str) or not profile[field].strip():
            ask(qid, question, "Thông tin này làm thay đổi cách thực hiện.")
    if not isinstance(profile.get("language"), str) or not profile["language"].strip():
        ask("language", "Ngôn ngữ bài cần dùng là gì?", "Cần xác định ngôn ngữ đầu ra.")
    assignment = profile.get("assignment_status")
    if assignment == "provided":
        if not any(item.strip() for item in profile.get("assignment_materials", [])):
            ask("assignment", "Đề/hướng dẫn hiện hành là tài liệu nào?", "Chưa chỉ được đầu vào của đề.")
    elif assignment == "self_defined":
        if not (profile.get("assignment_notes") or "").strip():
            ask("assignment", "Phạm vi tự xác định nào đã được mày chọn?", "Cần ghi nhận lựa chọn thực tế của người viết.")
    else:
        ask("assignment", "Mày có đề/hướng dẫn giảng viên không, hay đây là công việc tự xác định?", "Không tự suy đoán yêu cầu dự án.")
    rubric = profile.get("rubric_status")
    if rubric not in ("provided", "not_applicable") or not (profile.get("rubric_notes") or "").strip():
        ask("rubric", "Có rubric/tiêu chí cụ thể nào phải theo, hay phạm vi này không chấm theo rubric?", "Cần căn cứ kiểm tra kết quả, không tự tạo tiêu chí.")
    if not (profile.get("target_outcome") or "").strip():
        ask("target_outcome", "Mục tiêu mày muốn đạt được ở phần việc này là gì?", "Tách mục tiêu mong muốn khỏi tiêu chí chấm thực tế.")
    if task == "analysis":
        if profile.get("data_status") not in ("provided", "not_applicable") or not (profile.get("data_notes") or "").strip():
            ask("data", "Dữ liệu/output nào sẽ dùng, hay mày chỉ cần hướng dẫn phương pháp?", "Chưa rõ căn cứ và phạm vi phân tích.")
    for item in (state or {}).get("open_questions", []):
        affects = item.get("affects", [])
        if item["status"] == "open" and item.get("blocking", True) and (not affects or task in affects):
            ask("open:" + item["id"], item["question"], "Điểm chưa rõ của dự án chưa được giải quyết.")
    confirmation = (state or {}).get("user_confirmation") or {}
    summary = (state or {}).get("brief_summary")
    confirmed = (
        isinstance(summary, str) and bool(summary.strip())
        and bool(confirmation.get("message", "").strip())
        and confirmation.get("profile_sha256") == digest
        and confirmation.get("brief_sha256") == brief_fingerprint(summary)
        and confirmation.get("memory_sha256") == memory_fingerprint(state or {})
    )
    gaps = memory_gaps(state, digest)
    if blockers:
        status, action = "clarify", "Chỉ đọc đầu vào để làm rõ và hỏi tối đa 3 câu chính; chưa triển khai nội dung bài."
    elif gaps:
        status, action = "plan", "Bóc tách từng yêu cầu, lập dàn ý liên kết tiêu chí và ghi project_memory; chưa viết/phân tích bài."
    elif not confirmed:
        status, action = "confirm", "Tóm tắt cách hiểu cụ thể, đợi người viết xác nhận; không tự ghi xác nhận."
    else:
        status, action = "ready", "Tiếp tục phạm vi đã được xác nhận; hỏi lại nếu phát hiện điểm mới ảnh hưởng cách làm."
    priority = [q for q in blockers if q["id"] in {"assignment", "rubric", "target_outcome"}]
    questions = identity_questions or (priority + [q for q in blockers if q not in priority])[:3]
    stage = "course_and_discipline" if identity_questions else "project_details" if blockers else status
    if identity_questions:
        action = "Lượt này chỉ hỏi môn/ngành còn thiếu; chưa triển khai bài. Sau câu trả lời, tiếp tục làm rõ dự án theo ngành thực tế."
    elif not (state or {}).get("active_prompt"):
        status, stage, questions = "select_prompt", "prompt_selection", []
        action = "Trợ lý tự chọn, đọc và ghi prompt phù hợp vào active_prompt (task, reason, content), rồi lấy đề/câu hỏi, tiêu chí nếu có và mục tiêu; không bắt người dùng chọn prompt."
    return {
        "status": status, "can_execute": status == "ready", "requested_task": task,
        "intake_stage": stage,
        "profile_sha256": digest, "questions": questions,
        "brief_sha256": brief_fingerprint(summary) if isinstance(summary, str) else None,
        "remaining_blocker_count": max(0, len(blockers) - len(questions)), "all_blockers": blockers,
        "memory_gaps": gaps, "memory_sha256": memory_fingerprint(state or {}),
        "semantic_verification": "not_performed", "next_action": action,
    }


def main(argv: list[str] | None = None) -> int:
    from build_prompt import TASKS, load_profile

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--task", choices=TASKS, default="general")
    args = parser.parse_args(argv)
    try:
        profile = load_profile(args.project / "project.json")
        state_path = args.project / "project_state.json"
        state = load_state(state_path) if state_path.exists() else None
        result = evaluate_gate(profile, state, args.task)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["can_execute"] else 1
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
