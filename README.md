# Vinh AI Skills

Bộ skill và quy trình hỗ trợ học, nghiên cứu và làm luận văn của Vinh.

## Thành phần

| Thư mục | Công dụng |
| --- | --- |
| skills/academic-research-vietnamese | Nghiên cứu, viết/chấm sửa học thuật, Harvard, hỏi rõ và xác nhận dự án |
| skills/prompt-optimizer | Sửa prompt rõ ràng, giữ ý định và biến |
| skills/vinh-candid-mentor | Phản biện có căn cứ, giọng vui/thẳng đúng lúc, tự rà công tâm |
| thesis-workbench | Bộ luận văn 1.2.0: prompt tổng, 15 công đoạn/chế độ, mẫu hồ sơ và công cụ kiểm tra |

## Dùng bộ luận văn

Mở `thesis-workbench/PROMPT_LUAN_VAN.md`, nạp nội dung làm hướng dẫn rồi cung cấp đề, rubric và tài liệu hiện hành. Trước khi làm bài, giải quyết các câu hỏi ảnh hưởng cách làm và xác nhận cách hiểu. Sau đó làm từng phạm vi được giao, đối chiếu nguồn và tự rà trước khi giao.

Xem `thesis-workbench/README.md` để dùng từng công đoạn và công cụ Python. Mỗi thư mục trong `skills/` là một skill độc lập có SKILL.md, metadata và tài nguyên cần thiết; dùng trong môi trường hỗ trợ skill hoặc đọc SKILL.md làm hướng dẫn tương ứng.

## Kiểm tra

Trong thư mục `thesis-workbench`:

```bash
python scripts/verify_repo.py
python -m unittest discover -s tests -v
python scripts/audit_self_review.py --report reviews/repo-v1.2.0.json
```

Kết quả kiểm tra công cụ không chứng minh mô hình luôn phản biện đúng hoặc luận văn đạt điểm. Hồ sơ nguồn, dữ liệu, rubric và xác nhận phải phản ánh đầu vào thực tế.

## Giấy phép

Xem LICENSES.md và các giấy phép trong từng thành phần. Bộ sưu tập có thành phần CC BY-NC 4.0, AGPL-3.0-only, MIT và CC0; giữ phạm vi của từng thành phần.
