# Chọn prompt theo việc cần làm

Luôn dùng `rules/core.vi.md`, `rules/project-dialogue.vi.md`, `rules/request-refinement.vi.md` và `rules/candid-review.vi.md` cùng module. `build_prompt.py` ghép tự động, thay chuẩn trích dẫn và chuyển sang module làm rõ nếu hồ sơ chưa đủ điều kiện. Trong chat thông thường, dùng prompt tổng trước; AI cần hỏi/xác nhận, tự làm rõ yêu cầu, phản biện có căn cứ và tự rà xuyên suốt dự án.

| Task cho CLI | File | Kết quả cần có |
| --- | --- | --- |
| general | [00-general.md](00-general.md) | Chọn đúng việc hiện tại, không tự làm cả dự án |
| intake | [01-intake.md](01-intake.md) | Bảng yêu cầu và thông tin còn thiếu |
| outline | [02-outline.md](02-outline.md) | Câu hỏi, lập luận chính và dàn ý bám rubric |
| sources | [03-sources.md](03-sources.md) | Danh sách nguồn có trạng thái kiểm chứng |
| literature | [04-literature.md](04-literature.md) | Tổng hợp, so sánh và giới hạn của tài liệu |
| methodology | [05-methodology.md](05-methodology.md) | Thiết kế nghiên cứu phù hợp câu hỏi và dữ liệu |
| analysis | [06-analysis.md](06-analysis.md) | Phân tích có bằng chứng, diễn giải đúng |
| draft | [07-draft.md](07-draft.md) | Phần luận văn được yêu cầu, có nguồn đúng câu |
| review | [08-review.md](08-review.md) | Nhận xét theo rubric và bản đã sửa |
| citations | [09-citations.md](09-citations.md) | Đối chiếu nhận định, trích dẫn và danh mục |
| translate | [10-translate.md](10-translate.md) | Bản dịch đầy đủ, giữ cấu trúc và dữ liệu |
| export | [11-export.md](11-export.md) | Bản tổng hợp và kiểm tra hình thức theo mẫu |
| optimize | [12-optimize.md](12-optimize.md) | Chỉ sửa prompt, giữ nguyên ý định và biến |
| clarify | [13-clarify.md](13-clarify.md) | Hỏi điểm chưa rõ và xác nhận cách hiểu trước khi triển khai |
| self-review | [14-self-review.md](14-self-review.md) | Tự chấm bản hiện hành bằng bằng chứng, sửa và kiểm tra lại |

Nguồn tuyển chọn và cách chuyển đổi từng vai trò được ghi ở [PROVENANCE](../docs/PROVENANCE.md). Module dịch và xuất bản là phần bổ sung của repo, kết hợp vai trò biên tập/kiểm tra với yêu cầu Vinh.
