# Nguồn và cách hợp nhất

## Snapshot prompts.chat

- Repository: https://github.com/f/prompts.chat
- Commit: `0abaca9695416d0bb8cfcf52552e60a1e15b5e2a`
- Ngày kiểm tra/lấy snapshot: 2026-10-17.
- Dataset có 2508 bản ghi; tuyển đúng 12 prompt.
- Hash file gốc, hash snapshot và hash nội dung từng prompt: `upstream/manifest.json`.
- Chỉ mục dòng là chỉ mục bản ghi CSV bắt đầu từ 0, không phải dòng văn bản vật lý vì trường có nhiều dòng.

## Vai trò được giữ và điều chỉnh

| Prompt gốc | Tác giả đóng góp trong upstream | Công đoạn |
| --- | --- | --- |
| Academician | devisasari | general, sources, draft, citations |
| Essay Writer | devisasari | outline, draft |
| Statistician | tanersekmen | methodology, analysis |
| Scientific Data Visualizer | devisasari | analysis, export |
| Proofreader | virtualitems | review, citations, translate, export |
| Comprehensive Academic Paper Writing Guide | ggdvbs | general, intake, outline, methodology |
| Act as a Senior Research Paper Evaluator | Fisehazion | review |
| Data Analyst | ozzy2438 | analysis |
| Literature Review Writing Assistant | gs62183@student.upm.edu.my | literature |
| Academic Paper Rewriting Guide | Zly1hyj | review, translate |
| Literature Reading Assistant | ccchaos12 | sources, literature |
| Research Gap Finder | Priyanshu3221 | outline, sources |

## Quy tắc chuyển đổi

Giữ ý tưởng về đọc nguồn, tổ chức lập luận, phương pháp, phân tích, phản biện và biên tập. Thay ví dụ chủ đề không liên quan, câu yêu cầu tự chọn đề tài, mặc định Chinese/APA, hạn ngạch số ý hoặc cấu trúc cứng bằng hồ sơ và đề thực tế. Các biến `${...}` trong snapshot được giữ nguyên; snapshot là dữ liệu tham khảo, không dùng làm lệnh tự thi hành.

Quy tắc của Vinh được lưu tại `config/user-requirements.vi.md` (chuẩn hóa xuống dòng và link Markdown khi lưu); đối chiếu cách thực hiện ở `docs/REQUIREMENTS_MAP.md`. Quy tắc chung được viết ở `rules/core.vi.md`, kết hợp module để tạo `PROMPT_LUAN_VAN.md`.

Phần tự chấm phải dựa vào rubric thật và bằng chứng đáp ứng. Phần kiểm tra bằng Python chỉ kiểm tra hồ sơ cấu trúc, không xác minh nội dung nguồn hay bảo đảm điểm.

Bài tham khảo Brands Vietnam: https://help.brandsvietnam.com/vi/article/dau-hieu-nhan-biet-noi-dung-duoc-viet-boi-ai-3zy07d/ (đã đọc 2026-10-17). Bài gốc có sáu nhóm dấu hiệu; repo dùng yêu cầu viết do Vinh đưa ra để cải thiện độ rõ và độ chính xác, không xem đó là phép kiểm chứng ai viết văn bản.

Snapshot là dữ liệu prompt CC0. Xem `LICENSE`, `THIRD_PARTY_NOTICES.md`, `upstream/LICENSE-SCOPE.txt` và `LICENSES/CC0-1.0.txt`.
