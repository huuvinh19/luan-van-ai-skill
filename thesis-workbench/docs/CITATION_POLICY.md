# Chính sách nguồn và trích dẫn

## Chuẩn áp dụng

Mặc định Harvard theo mẫu giảng viên mà Vinh cung cấp. Đặt `citation_style` trong hồ sơ thành `Harvard` hoặc `APA`. Ghi đường dẫn/mô tả hướng dẫn vào `instructor_citation_guide`; để `null` khi chưa có, không tự cho rằng đã đọc mẫu. Chi tiết nhiều tác giả, cùng năm, loại tài liệu và dấu câu phải được đối chiếu với hướng dẫn thực tế.

Yêu cầu riêng của Vinh: trích dẫn tác giả–năm nằm ở cuối câu được hỗ trợ, trước dấu chấm. Đây là lựa chọn trình bày của dự án, không phải tuyên bố rằng mọi hệ Harvard/APA đều cấm cách dẫn nguồn trong câu.

Ví dụ hình thức, không phải nguồn thật:

> Nhận định đã được nguồn hỗ trợ (Họ tác giả, năm).

Mỗi câu có nội dung vay mượn phải có nguồn tương ứng, kể cả khi diễn giải. Không dùng một trích dẫn cuối đoạn bao phủ các nhận định khác căn cứ. Trích nguyên văn cần dấu ngoặc kép và định vị theo chuẩn/mẫu đang dùng. Đối với trích dẫn khối, áp dụng đúng quy định của giảng viên.

## Ba loại nội dung

| Loại | Căn cứ cần giữ | Cách xử lý |
| --- | --- | --- |
| external | Nguồn đã đọc và vị trí hỗ trợ | Trích tác giả–năm ở đúng câu; có entry danh mục |
| data | Dữ liệu, bước xử lý và output thật | Nêu nguồn dữ liệu và nguồn phép tính; không gán kết quả tự tính cho bài báo |
| interpretation | Kết quả/nguồn làm nền và lập luận | Nêu rõ đây là diễn giải; trích nguồn của tiền đề khi cần |

Mã nguồn S001 hay nhận định C001 chỉ thuộc hồ sơ làm việc. Không để mã đó thay cho trích dẫn trong văn bản nộp.

## Trạng thái kiểm chứng

- `unverified`: nguồn hoặc metadata chưa được xác minh.
- `metadata_only`: đã kiểm tra tác giả/năm/tiêu đề/DOI nhưng chưa đủ căn cứ xác nhận nội dung hỗ trợ nhận định.
- `content_checked`: đã đọc nội dung liên quan và ghi `checked_locations`. Trạng thái này vẫn cần người đọc đánh giá độ phù hợp của nghiên cứu và nhận định.

DOI hợp lệ về hình thức không chứng minh bài báo tồn tại hoặc hỗ trợ câu viết. Ghi rõ chỉ đọc tóm tắt nếu đó là phạm vi tiếp cận. Link không mở được phải được báo riêng; không tự bù thông tin còn thiếu. Hồ sơ chỉ có khai báo `content_checked` chưa phải bằng chứng độc lập rằng việc đọc đã xảy ra.

## Danh mục và các trường hợp thiếu

Sắp xếp alphabet theo tác giả/tổ chức và định dạng theo loại nguồn. Lưu DOI nếu có; với web, giữ URL và ngày truy cập khi hướng dẫn yêu cầu. Mỗi trích dẫn trong bài phải có entry danh mục, mỗi entry phải được dùng đúng phạm vi hoặc xử lý theo loại danh mục giảng viên yêu cầu.

Không tự đặt tác giả, năm, trang hoặc tiêu đề. Với metadata thiếu, đối chiếu hướng dẫn và hỏi khi ảnh hưởng đến tính đúng; phần chưa giải quyết được nêu ở ghi chú riêng. Với cùng tác giả/cùng năm, cần cách phân biệt rõ theo hướng dẫn. Không tự xóa hậu tố làm hai nguồn trở nên không phân biệt được.

Khi chuyển APA theo yêu cầu mới, cập nhật nhất quán cả thân bài, danh mục và các trường hợp đặc biệt, rồi kiểm tra lại. `build_prompt.py` đổi chuẩn trong chỉ dẫn; nó không tự định dạng hoặc sửa citation của bản luận văn.
