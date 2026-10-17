#!/usr/bin/env python3
"""Check consistency of a declared self-review; does not judge the work itself."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

JUDGMENTS = {"met", "partly_met", "not_met", "not_checked"}
VERDICTS = {"ready_for_scope", "needs_revision", "not_fully_checked"}


def audit_review(report: dict) -> dict:
    if not isinstance(report, dict):
        raise ValueError("Báo cáo phải là JSON object.")
    for key in ("criteria", "findings", "remaining_limits"):
        if not isinstance(report.get(key), list):
            raise ValueError(f"{key} phải là danh sách.")
    issues = []

    def has_text(value) -> bool:
        return isinstance(value, str) and bool(value.strip())

    def flag(code: str, location: str, message: str) -> None:
        issues.append({"code": code, "location": location, "message": message})

    for field in ("scope", "artifact", "review_basis"):
        if not has_text(report.get(field)):
            flag("missing_review_context", field, f"Chưa ghi {field}.")
    if report.get("reviewer_mode") != "same_assistant_separate_pass":
        flag("reviewer_mode_mismatch", "reviewer_mode", "Mẫu này là cùng trợ lý tự rà ở lượt riêng, không phải reviewer độc lập.")
    if not report["criteria"]:
        flag("no_criteria", "criteria", "Chưa có tiêu chí để tự đánh giá.")
    criteria_ids = set()
    judgments = []
    for index, item in enumerate(report["criteria"], 1):
        if not isinstance(item, dict):
            raise ValueError("Mỗi tiêu chí phải là object.")
        loc = f"criteria[{index}]"
        cid = item.get("id")
        if not has_text(cid) or cid in criteria_ids:
            flag("invalid_criterion_id", loc, "ID tiêu chí trống hoặc trùng.")
        if isinstance(cid, str):
            criteria_ids.add(cid)
        if not has_text(item.get("criterion")) or not has_text(item.get("reason")):
            flag("missing_criterion_reason", loc, "Cần tiêu chí và lý do đánh giá cụ thể.")
        judgment = item.get("judgment")
        if not isinstance(judgment, str) or judgment not in JUDGMENTS:
            flag("invalid_judgment", loc, "Trạng thái tiêu chí không hợp lệ.")
        judgments.append(judgment)
        if judgment in ("met", "partly_met", "not_met") and not has_text(item.get("evidence")):
            flag("missing_review_evidence", loc, "Kết luận tiêu chí cần vị trí/bằng chứng.")
        if judgment in ("partly_met", "not_met", "not_checked") and not has_text(item.get("next_action")):
            flag("missing_next_action", loc, "Cần ghi việc sửa/kiểm tra tiếp theo.")
    finding_ids = set()
    open_findings = False
    for index, item in enumerate(report["findings"], 1):
        if not isinstance(item, dict):
            raise ValueError("Mỗi lỗi phải là object.")
        loc = f"findings[{index}]"
        fid = item.get("id")
        if not has_text(fid) or fid in finding_ids:
            flag("invalid_finding_id", loc, "ID lỗi trống hoặc trùng.")
        if isinstance(fid, str):
            finding_ids.add(fid)
        for field in ("location", "issue", "action"):
            if not has_text(item.get(field)):
                flag("missing_finding_detail", loc, f"Lỗi cần {field} cụ thể.")
        if item.get("severity") not in ("critical", "major", "minor"):
            flag("invalid_severity", loc, "Mức ảnh hưởng cần critical/major/minor.")
        if item.get("status") not in ("open", "resolved"):
            flag("invalid_finding_status", loc, "Trạng thái lỗi cần open hoặc resolved.")
        if item.get("status") == "open":
            open_findings = True
        elif item.get("status") == "resolved" and not has_text(item.get("verification")):
            flag("unverified_fix", loc, "Đã ghi sửa xong nhưng chưa ghi căn cứ kiểm tra sau sửa.")
    if not all(has_text(x) for x in report["remaining_limits"]):
        flag("invalid_limits", "remaining_limits", "Giới hạn cần ghi bằng chuỗi có nội dung.")
    if "not_checked" in judgments and not report["remaining_limits"]:
        flag("undisclosed_unchecked_item", "remaining_limits", "Có tiêu chí chưa kiểm tra nhưng chưa nêu giới hạn.")
    verdict = report.get("overall_verdict")
    if not isinstance(verdict, str) or verdict not in VERDICTS:
        flag("invalid_overall_verdict", "overall_verdict", "Kết luận chung không hợp lệ.")
    if verdict == "ready_for_scope" and (not judgments or any(x != "met" for x in judgments) or open_findings):
        flag("premature_ready_verdict", "overall_verdict", "Chưa thể ghi sẵn sàng khi tiêu chí chưa đạt/chưa kiểm tra hoặc lỗi còn mở.")
    grade = report.get("grade")
    if grade is not None:
        basis = report.get("grading_basis")
        if not isinstance(basis, dict) or basis.get("provided") is not True or not has_text(basis.get("source")) or not has_text(basis.get("scale")):
            flag("unsupported_grade", "grading_basis", "Điểm/mức đạt cần thang/rubric thực tế và nguồn được cung cấp.")
        if not isinstance(grade, dict):
            flag("invalid_grade", "grade", "grade cần object hoặc null.")
        else:
            ids = grade.get("criterion_ids")
            if not has_text(grade.get("value")) or not isinstance(ids, list) or not ids or not all(isinstance(x, str) and x in criteria_ids for x in ids):
                flag("grade_without_criteria", "grade", "Điểm cần giá trị và liên kết tiêu chí đã đánh giá.")
        if verdict != "ready_for_scope":
            flag("premature_grade", "grade", "Chưa đủ căn cứ ghi điểm/mức đạt hoàn thành cho phạm vi còn thiếu.")
    return {
        "mechanical_status": "findings" if issues else "clear",
        "issues": issues,
        "semantic_checks": "not_performed",
        "limits": "Chỉ kiểm tra mâu thuẫn và thiếu khai báo. Không xác minh bằng chứng, đọc bài, tính điểm hoặc chứng minh đánh giá không thiên vị.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = audit_review(json.loads(args.report.read_text(encoding="utf-8-sig")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result["issues"] else 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"mechanical_status": "error", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
