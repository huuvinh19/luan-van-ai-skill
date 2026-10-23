# Đối chiếu yêu cầu của người viết với repo

| Yêu cầu | Nơi thực hiện |
| --- | --- |
| Bắt đầu từ chat tự nhiên, hỏi môn/ngành trước, dùng được theo bối cảnh IT | project-dialogue; intake/clarify; project_gate; PROJECT_INTAKE.md; discipline để null trong mẫu |
| Chỉ tuyển prompt liên quan luận văn từ prompts.chat | 12 prompt có nguồn/hash trong upstream/manifest.json; công đoạn điều chỉnh trong PROVENANCE.md |
| Tích hợp skill tối ưu prompt từ linshenkx/prompt-optimizer | skills/prompt-optimizer ở gốc repo; module optimize; request-refinement |
| Đọc đề, rubric, dàn ý và tài liệu trước khi làm | `rules/core.vi.md` mục 1; module intake; `requirements.csv` |
| Tách yêu cầu bắt buộc/gợi ý; hỏi đến khi hiểu phạm vi hiện tại | Mục 1; project-dialogue; intake/clarify; trạng thái câu hỏi trong project_state.json |
| Giải thích ngắn, viết tự nhiên, có chiều sâu | Mục 2–3; draft; literature; review |
| Phân biệt nguồn, phân tích dữ liệu và suy luận | Mục 2; `CITATION_POLICY.md`; claim_type trong claims.csv |
| Tránh sáo rỗng, lặp ý, danh sách vụn và lạm dụng gạch dài | Mục 3; draft; review; CHECKLIST |
| Không bịa dữ liệu, kết quả hoặc nguồn | Mục 2–4; sources; methodology; analysis |
| Không lẫn lời dẫn chatbot; giọng văn nhất quán | Mục 3 và 5; draft; export |
| Harvard mặc định; chuyển APA nếu giảng viên yêu cầu | Mục 4; project.json; build_prompt.py; citations |
| Không giả nhận đã đọc đúng mẫu trích dẫn khi ảnh thiếu/không mở được | Mục 4; CITATION_POLICY; instructor_citation_guide để null khi chưa có |
| Tác giả–năm cuối đúng câu, trước dấu chấm | Mục 4; CITATION_POLICY; citations |
| Trích nguyên văn có ngoặc kép/định vị | Mục 4; CITATION_POLICY; citations |
| Danh mục alphabet, metadata và đối chiếu hai chiều | Mục 4; CITATION_POLICY; citations |
| Tự kiểm tra yêu cầu, kiến thức, phương pháp, nguồn và hình thức | Mục 5; review; CHECKLIST |
| Sửa lỗi trước khi gửi; nêu riêng phần thiếu căn cứ | Mục 5; review; export; progress.md |
| Áp dụng xuyên suốt; tách nhận xét và phần nộp | Mục 5; toàn bộ module; AGENTS.md |
| Tóm tắt và đợi xác nhận trước khi triển khai lần đầu | project-dialogue; PROJECT_DIALOGUE; project_gate.py; build_prompt.py |
| Tự làm rõ prompt mà không bịa hoặc đổi ý định | request-refinement; optimize; --request-file giữ yêu cầu gốc |
| Hỏi lại khi có thay đổi quan trọng, không hỏi lại điều đã chốt | project-dialogue; trạng thái câu hỏi theo task và fingerprint hồ sơ |
| Không mặc nhiên tin hoặc đồng ý; phản biện bằng căn cứ | candid-review; CANDID_REVIEW; review và self-review |
| Giao tiếp vui, thẳng, hơi cà khịa có chừng mực theo bối cảnh | candid-review; giữ riêng giọng trao đổi và giọng học thuật |
| Tự chấm công tâm, không ưu ái bài do mình viết hoặc tự cho điểm | candid-review; self-review.json; audit_self_review.py |

Bảng này đối chiếu thiết kế chỉ dẫn với yêu cầu. Nó không phải kết quả đánh giá một luận văn cụ thể và không chứng nhận rằng mô hình luôn thực hiện đúng mọi chỉ dẫn.

Kết quả đối chiếu nguồn, các điểm đã sửa và giới hạn còn lại: [đợt rà ngày 2026-10-17](AUDIT_2026-10-17.md).

## Bổ sung 2026-10-23: prompt và bộ nhớ dự án

| Yêu cầu | Nơi thực hiện |
| --- | --- |
| Tự chọn prompt sau hỏi bối cảnh, không bắt người viết chọn | rules/project-memory.vi.md; gate select_prompt; active_prompt |
| Giữ prompt thực sự dùng và lý do, dùng xuyên suốt chat | active_prompt.task/reason/content trong project_state.json; quy tắc bàn giao |
| Sau chọn prompt lấy đề/câu hỏi, rubric nếu có và mục tiêu | project-dialogue.vi.md; thứ tự assignment/rubric/target_outcome của gate |
| Bóc từng chi tiết của đề thành yêu cầu có căn cứ/cách kiểm tra | project_memory.requirements; prompts/01-intake.md và 02-outline.md |
| Dàn ý liên kết đủ yêu cầu và dùng khi viết/sửa/tự rà | project_memory.outline; gate plan; prompts/07-draft.md và 08-review.md |
| Giữ tiêu chí, thay đổi và lỗi từng mắc để tránh lặp | project_memory, known_errors, progress.md; fingerprint và xác nhận hiện hành |
| Hồ sơ trong chat/tệp, không hứa trí nhớ vĩnh viễn | project-memory.vi.md; mẫu và quy tắc bàn giao |
