#!/usr/bin/env python3
"""Verify snapshot integrity, generated prompt and local documentation links."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

from build_prompt import ROOT, TASKS, assemble


def verify(root: Path = ROOT) -> list[str]:
    errors = []
    manifest = json.loads((root / "upstream/manifest.json").read_text(encoding="utf-8"))
    records = json.loads((root / "upstream/selected-prompts.json").read_text(encoding="utf-8"))
    for name, expected in manifest["files_sha256"].items():
        target = (root / name).resolve()
        if not target.is_relative_to(root.resolve()):
            errors.append(f"Đường dẫn snapshot vượt repo: {name}")
            continue
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            errors.append(f"Snapshot thiếu hoặc đổi nội dung: {name}")
    if len(records) != len(manifest["selected_prompts"]):
        errors.append("Số prompt trong snapshot và manifest không khớp.")
    for row, origin in zip(records, manifest["selected_prompts"]):
        actual = hashlib.sha256(row["prompt"].encode("utf-8")).hexdigest()
        if row["act"] != origin["act"] or actual != origin["prompt_sha256"]:
            errors.append(f"Nội dung prompt không khớp: {origin['act']}")
    with (root / "upstream/selected-prompts.csv").open(encoding="utf-8", newline="") as stream:
        csv_records = list(csv.DictReader(stream))
    if csv_records != records:
        errors.append("Hai dạng JSON và CSV của snapshot không khớp.")
    if (root / "PROMPT_LUAN_VAN.md").read_text(encoding="utf-8") != assemble("general", root=root):
        errors.append("PROMPT_LUAN_VAN.md chưa được sinh lại từ quy tắc/module hiện hành.")
    for filename in TASKS.values():
        if not (root / "prompts" / filename).is_file():
            errors.append(f"Thiếu module: {filename}")
    for path in root.rglob("*.md"):
        if ".git" in path.parts or "output" in path.parts:
            continue
        content = path.read_text(encoding="utf-8")
        for link in re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", content):
            parsed = urlsplit(link)
            if parsed.scheme or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f"Link nội bộ không hợp lệ: {path.relative_to(root)} -> {link}")
    for required in ("LICENSE", "THIRD_PARTY_NOTICES.md", "LICENSES/CC0-1.0.txt"):
        if not (root / required).is_file():
            errors.append(f"Thiếu giấy phép/notice: {required}")
    return errors


def main() -> int:
    try:
        errors = verify()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Không kiểm tra được repo: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"LỖI: {error}")
        return 1
    print("OK: snapshot, prompt tổng, module, giấy phép và link nội bộ khớp.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
