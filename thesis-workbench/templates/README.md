# Mẫu hồ sơ dự án

Copy bộ file này sang thư mục dự án riêng rồi điền. Mẫu cố ý để trống các thông tin nghiên cứu chưa có; không dùng tên người học hoặc trường để suy ra đề hay rubric.

| File | Điền gì |
| --- | --- |
| project.json | Đề tài, môn, phạm vi hiện tại, ngôn ngữ, số từ và hướng dẫn |
| project_state.json | Tóm tắt, lời xác nhận thực tế và các câu hỏi của dự án |
| requirements.csv | Từng yêu cầu thật và bằng chứng đáp ứng |
| sources.json | Nguồn và trạng thái đã đọc |
| claims.csv | Nhận định và căn cứ nguồn/dữ liệu/suy luận |
| draft.md | Nội dung dự thảo; ghi chú kiểm tra giữ ở file khác |
| review.md | Nhận xét theo rubric, lỗi cụ thể và hướng sửa |
| self-review.json | Kết quả tự rà có tiêu chí, bằng chứng, lỗi, giới hạn và kết luận |
| progress.md | Tiến độ, kết quả hiện hành, phần thiếu và bước tiếp theo |

## Cấu trúc nguồn

`sources.json` là mảng JSON. Mỗi nguồn có:

```json
{
  "id": "S001",
  "authors": ["<tác giả hoặc tổ chức thực tế>"],
  "year": "<năm thực tế>",
  "title": "<tiêu đề thực tế>",
  "source_type": "<journal/book/report/web/lecture/dataset>",
  "doi": "",
  "url": "",
  "accessed": "",
  "verification_status": "unverified",
  "checked_locations": [],
  "reference_entry": ""
}
```

Đây là cấu trúc minh họa, không phải một nguồn. Với bài in, URL/DOI có thể trống; ghi vị trí bằng chứng trong `checked_locations` sau khi đọc. `reference_entry` là entry hoàn chỉnh theo mẫu giảng viên. Chuyển từ `metadata_only` sang `content_checked` chỉ sau khi thật sự đọc nội dung hỗ trợ. Công cụ không tự đánh giá sự thật của khai báo.

## Bảng nhận định

`claim_type`: `external`, `data`, `interpretation`. `support_status`: `pending`, `supported`, `contradicted`. Dùng dấu `|` để ngăn nhiều source_ids hoặc evidence_locations. Với `external`, chỉ đánh `supported` khi nguồn đã được đọc và có vị trí bằng chứng cụ thể. Với dữ liệu hoặc diễn giải, vẫn ghi đầu vào/output/tiền đề ở evidence_locations.

## Bảng yêu cầu

`kind`: `required`, `suggestion`. `status`: `pending`, `partial`, `covered`, `not_applicable`. `criterion` giữ đúng rubric đã cung cấp, không tự thêm P/M/D. `evidence` cần chỉ được nội dung/bằng chứng khi đánh `covered`, hoặc lý do khi `not_applicable`.

Mẫu trống chưa đủ điều kiện nộp. `audit_project.py` sẽ báo thông tin dự án còn thiếu. Xem [demo](../examples/README.md) và [giới hạn công cụ](../docs/TOOLS.md).

## Trạng thái dự án từ bản 1.1.0

`output_format` ghi đầu ra cần làm. `assignment_status` nhận `not_provided`, `provided` hoặc `self_defined`; với self_defined, ghi lựa chọn thực tế vào `assignment_notes`. `rubric_status` nhận `not_provided`, `provided`, `not_applicable`, có `rubric_notes` chỉ tài liệu/tiêu chí hoặc lý do không áp dụng. `data_status` và `data_notes` làm rõ đầu vào phân tích khi đến công đoạn analysis.

`context_revision` là số nguyên dương. Tăng số này khi thay bản đề, dữ liệu hoặc tài liệu quan trọng nhưng giữ nguyên tên file; công cụ không tự theo dõi nội dung mọi file bên ngoài.

Trong `project_state.json`, `brief_summary` là cách hiểu đã đưa cho người viết xem. Chỉ ghi `user_confirmation` sau khi có xác nhận thực tế, gồm `message`, `profile_sha256` của hồ sơ và `brief_sha256` của bản tóm tắt tương ứng. Không tự tạo câu xác nhận để mở bước làm bài. CLI xuất fingerprint để lưu đúng phiên bản; hash không chứng minh nội dung đã được hiểu đúng.

Mỗi câu hỏi trong `open_questions` có `id`, `question`, `status` (`open`/`resolved`), `blocking` (boolean), `affects` (danh sách task, trống là toàn dự án), và `answer` khi đã resolved. Câu hỏi chưa đến bước cần quyết định có thể ghi blocking=false; việc chọn trạng thái cần đúng bối cảnh, không dùng để lách điểm chưa hiểu. Xem [PROJECT_DIALOGUE](../docs/PROJECT_DIALOGUE.md).
