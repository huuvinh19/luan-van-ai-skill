#!/usr/bin/env python3
"""Check structured project records; does not verify sources or grade prose."""
from __future__ import annotations

import argparse
import csv
from datetime import date
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

from build_prompt import load_profile
from project_gate import evaluate_gate, load_state

CLAIM_FIELDS = {"claim_id", "text", "claim_type", "source_ids", "support_status", "evidence_locations"}
REQUIREMENT_FIELDS = {"requirement_id", "requirement_text", "kind", "criterion", "section", "status", "evidence"}
SOURCE_STATES = {"unverified", "metadata_only", "content_checked"}


def read_table(path: Path, required: set[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        if len(set(fields)) != len(fields) or not required.issubset(fields):
            raise ValueError(f"{path.name}: header thiếu trường bắt buộc hoặc trùng tên.")
        rows = []
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"{path.name}: số ô không khớp header.")
            if any(row.values()):
                rows.append({key: value.strip() for key, value in row.items()})
        return rows


def split_ids(value: str) -> list[str]:
    return [part.strip() for part in value.split("|") if part.strip()]


def audit(project: Path) -> dict:
    profile = load_profile(project / "project.json")
    sources = json.loads((project / "sources.json").read_text(encoding="utf-8-sig"))
    if not isinstance(sources, list) or not all(isinstance(s, dict) for s in sources):
        raise ValueError("sources.json phải là danh sách object.")
    claims = read_table(project / "claims.csv", CLAIM_FIELDS)
    requirements = read_table(project / "requirements.csv", REQUIREMENT_FIELDS)
    state_path = project / "project_state.json"
    state = load_state(state_path) if state_path.exists() else None
    readiness = evaluate_gate(profile, state, "general")
    issues = []
    notes = []

    def flag(code: str, location: str, message: str) -> None:
        issues.append({"code": code, "location": location, "message": message})

    for key in ("topic", "current_scope"):
        if not (profile.get(key) or "").strip():
            flag("missing_project_context", "project.json", f"Chưa điền {key}.")
    if not profile.get("instructor_citation_guide"):
        notes.append("Chưa khai báo mẫu trích dẫn của giảng viên; chưa thể kiểm tra biến thể cụ thể.")
    if not readiness["can_execute"]:
        flag("project_not_ready", "project_state.json", readiness["next_action"])

    source_map = {}
    for index, source in enumerate(sources, 1):
        sid = source.get("id")
        loc = f"sources.json[{index}]"
        if not isinstance(sid, str) or not sid.strip():
            flag("missing_source_id", loc, "Nguồn thiếu id hợp lệ.")
            continue
        if sid in source_map:
            flag("duplicate_source_id", loc, f"Trùng id {sid}.")
        source_map[sid] = source
        for field in ("year", "title", "source_type"):
            if not isinstance(source.get(field), str) or not source[field].strip():
                flag("missing_source_metadata", loc, f"Nguồn {sid} thiếu {field}.")
        authors = source.get("authors")
        if not isinstance(authors, list) or not authors or not all(isinstance(a, str) and a.strip() for a in authors):
            flag("missing_authors", loc, f"Nguồn {sid} thiếu tác giả/tổ chức.")
        status = source.get("verification_status")
        if status not in SOURCE_STATES:
            flag("invalid_source_status", loc, f"Trạng thái nguồn {sid} không hợp lệ.")
        locations = source.get("checked_locations", [])
        if not isinstance(locations, list) or not all(isinstance(x, str) and x.strip() for x in locations):
            flag("invalid_evidence_locations", loc, f"Nguồn {sid}: checked_locations phải là danh sách chuỗi.")
        elif status == "content_checked" and not locations:
            flag("missing_checked_location", loc, f"Nguồn {sid} khai đã đọc nhưng chưa ghi vị trí.")
        for field in ("url", "doi", "accessed", "reference_entry"):
            if field in source and not isinstance(source[field], str):
                flag("invalid_source_field", loc, f"Nguồn {sid}: {field} phải là chuỗi.")
        url = source.get("url", "")
        if isinstance(url, str) and url:
            parsed = urlsplit(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                flag("invalid_url_shape", loc, f"URL nguồn {sid} chưa đúng dạng http/https.")
        doi = source.get("doi", "")
        if isinstance(doi, str) and doi:
            bare = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", doi, flags=re.I)
            if not re.fullmatch(r"10\.\d{4,9}/\S+", bare):
                flag("invalid_doi_shape", loc, f"DOI nguồn {sid} chưa đúng hình thức.")
        accessed = source.get("accessed", "")
        if isinstance(accessed, str) and accessed:
            try:
                date.fromisoformat(accessed)
            except ValueError:
                flag("invalid_access_date", loc, f"Ngày truy cập {sid} cần dạng YYYY-MM-DD.")

    seen_claims = set()
    for index, claim in enumerate(claims, 2):
        loc = f"claims.csv: record {index}"
        cid = claim["claim_id"]
        if not cid or cid in seen_claims:
            flag("invalid_claim_id", loc, "ID nhận định trống hoặc trùng.")
        seen_claims.add(cid)
        if not claim["text"]:
            flag("empty_claim", loc, "Nhận định thiếu nội dung.")
        ctype = claim["claim_type"]
        if ctype not in {"external", "data", "interpretation"}:
            flag("invalid_claim_type", loc, "claim_type không hợp lệ.")
        support = claim["support_status"]
        if support not in {"pending", "supported", "contradicted"}:
            flag("invalid_support_status", loc, "support_status không hợp lệ.")
        elif support != "supported":
            flag("unresolved_claim", loc, f"Nhận định {cid} đang ở trạng thái {support}.")
        if not claim["evidence_locations"]:
            flag("missing_claim_evidence", loc, f"Nhận định {cid} chưa ghi căn cứ/vị trí bằng chứng.")
        ids = split_ids(claim["source_ids"])
        if ctype == "external" and not ids:
            flag("external_without_source", loc, f"Nhận định {cid} thiếu nguồn ngoài.")
        for sid in ids:
            source = source_map.get(sid)
            if source is None:
                flag("unknown_source", loc, f"Không có nguồn {sid} trong sources.json.")
            elif ctype == "external" and support == "supported":
                if source.get("verification_status") != "content_checked":
                    flag("source_not_content_checked", loc, f"Nguồn {sid} chưa khai kiểm tra nội dung.")
                if not isinstance(source.get("reference_entry"), str) or not source["reference_entry"].strip():
                    flag("missing_reference_entry", loc, f"Nguồn {sid} chưa có entry danh mục.")

    if not requirements:
        flag("no_requirements", "requirements.csv", "Chưa có yêu cầu đề bài để đối chiếu.")
    seen_requirements = set()
    for index, req in enumerate(requirements, 2):
        loc = f"requirements.csv: record {index}"
        rid = req["requirement_id"]
        if not rid or rid in seen_requirements:
            flag("invalid_requirement_id", loc, "ID yêu cầu trống hoặc trùng.")
        seen_requirements.add(rid)
        if not req["requirement_text"]:
            flag("empty_requirement", loc, "Thiếu nội dung yêu cầu.")
        if req["kind"] not in {"required", "suggestion"}:
            flag("invalid_requirement_kind", loc, "kind phải là required hoặc suggestion.")
        status = req["status"]
        if status not in {"pending", "partial", "covered", "not_applicable"}:
            flag("invalid_requirement_status", loc, "status yêu cầu không hợp lệ.")
        if req["kind"] == "required" and status in {"pending", "partial"}:
            flag("unmet_requirement", loc, f"Yêu cầu {rid} chưa được ghi nhận đáp ứng đủ.")
        if status in {"covered", "not_applicable"} and not req["evidence"]:
            flag("missing_requirement_evidence", loc, f"Yêu cầu {rid} thiếu bằng chứng hoặc lý do loại trừ.")
        if status == "covered" and not req["section"]:
            flag("missing_requirement_section", loc, f"Yêu cầu {rid} chưa chỉ mục/phần đáp ứng.")

    return {
        "mechanical_status": "findings" if issues else "clear",
        "counts": {"sources": len(sources), "claims": len(claims), "requirements": len(requirements)},
        "issues": issues,
        "notes": notes,
        "semantic_checks": "not_performed",
        "project_gate": readiness,
        "limits": [
            "Không truy cập web, DOI hoặc file bằng chứng để xác minh nguồn/địa chỉ.",
            "Không đọc/đối chiếu thân luận văn, kiểm tra vị trí citation hoặc chấm rubric.",
            "Khai báo supported/content_checked/covered vẫn phải được kiểm chứng bằng đọc và đối chiếu thực tế.",
            "clear chỉ có nghĩa không phát hiện lỗi hồ sơ theo các quy tắc này; không phải chứng nhận sẵn sàng nộp.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--out", type=Path, help="Ghi báo cáo JSON; mặc định in stdout.")
    args = parser.parse_args(argv)
    try:
        report = audit(args.project)
        code = 1 if report["issues"] else 0
    except (OSError, ValueError, TypeError, csv.Error) as exc:
        report = {"mechanical_status": "error", "error": str(exc), "semantic_checks": "not_performed"}
        code = 2
    result = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        try:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(result, encoding="utf-8")
        except OSError as exc:
            print(f"Không ghi được báo cáo: {exc}", file=sys.stderr)
            return 2
    else:
        sys.stdout.write(result)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
