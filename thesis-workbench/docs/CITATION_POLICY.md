# Dùng nguồn khi viết

Khi chấm, áp dụng [nhóm 2–4 của bộ tiêu chí chung](../rules/review-criteria.vi.md). Tài liệu dưới đây hướng dẫn cách chuẩn bị bài và lưu bằng chứng.

## Chọn mẫu cho dự án

Ghi chuẩn được yêu cầu vào `citation_style` và mẫu/biến thể vào `instructor_citation_guide`. Với mẫu riêng, chọn `custom`; xem [các giá trị được hỗ trợ](TOOLS.md). Một đường dẫn trong hồ sơ chưa chứng minh đã đọc mẫu. Khi đổi chuẩn, cập nhật cả thân bài lẫn danh mục; công cụ ghép prompt không tự định dạng luận văn.

Ví dụ hình thức theo lựa chọn tác giả–năm mặc định của dự án, không phải nguồn thật: “Nhận định được nguồn hỗ trợ (Họ tác giả, năm).” Nếu mẫu yêu cầu đánh số hoặc chú thích, giữ đúng cách dẫn và thứ tự danh mục của mẫu đó.

## Ghi xuất xứ của nhận định

| Loại trong hồ sơ | Giữ lại làm bằng chứng |
| --- | --- |
| `external` – ý mượn nguồn | Tài liệu, đoạn hoặc trang thực sự hỗ trợ câu và mục danh mục tương ứng. |
| `data` – kết quả tự tính | Nguồn dữ liệu, bước xử lý và kết quả thực tế. Nếu tự tính tỷ lệ từ một bảng, phân biệt nguồn của bảng với phép tính của người viết. |
| `interpretation` – suy luận | Kết quả hoặc tiền đề làm căn cứ và lý do cho cách diễn giải. |

Trong `sources.json`, dùng `unverified` khi chưa xác minh; `metadata_only` khi mới kiểm tra thông tin xuất bản; `content_checked` khi đã đọc nội dung liên quan và ghi vị trí ở `checked_locations`. Mã S001/C001 chỉ dùng để lần lại hồ sơ, không thay cho dấu dẫn trong bản nộp.
