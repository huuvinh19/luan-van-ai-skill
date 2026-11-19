# Chính sách nguồn và trích dẫn

## Chuẩn áp dụng

Đề và mẫu giảng viên quyết định chuẩn, phiên bản, vị trí dấu dẫn và thứ tự danh mục. Ghi chuẩn vào `citation_style`: có thể chọn Harvard (mặc định), APA, IEEE, Vancouver, Chicago, MLA hoặc AMA. Với chuẩn riêng hoặc chuẩn khác, chọn `custom`, ghi tên/biến thể và mẫu vào `instructor_citation_guide`. Nếu chưa có mẫu, để trống trường hướng dẫn, hỏi phần cần biết khi định dạng; không nhận đã đối chiếu hoặc tự thay chuẩn riêng bằng Harvard.

Khi bài dùng cấu hình tác giả–năm mặc định của dự án, đặt dấu dẫn ở cuối câu được hỗ trợ, trước dấu chấm. Một đề yêu cầu cách khác thì theo đề. Với kiểu đánh số, theo từng số từ câu đến đúng mục, kiểm tra số dùng lại và thứ tự theo mẫu. Với kiểu chú thích, kiểm tra dấu dẫn và chú thích tương ứng.

Ví dụ hình thức, không phải nguồn thật:

> Nhận định đã được nguồn hỗ trợ (Họ tác giả, năm).

Mỗi câu có nội dung vay mượn phải có nguồn tương ứng, kể cả khi diễn giải. Không dùng một trích dẫn cuối đoạn bao phủ các nhận định khác căn cứ. Trích nguyên văn cần dấu ngoặc kép và định vị theo chuẩn/mẫu đang dùng. Đối với trích dẫn khối, áp dụng đúng quy định của giảng viên.

## Ba loại nội dung

| Loại | Căn cứ cần giữ | Cách xử lý |
| --- | --- | --- |
| external | Nguồn đã đọc và vị trí hỗ trợ | Trích đúng câu/ý theo chuẩn của bài; đối chiếu với mục nguồn tương ứng |
| data | Dữ liệu, bước xử lý và output thật | Nêu nguồn dữ liệu và nguồn phép tính; không gán kết quả tự tính cho bài báo |
| interpretation | Kết quả/nguồn làm nền và lập luận | Nêu rõ đây là diễn giải; trích nguồn của tiền đề khi cần |

Mã nguồn S001 hay nhận định C001 chỉ thuộc hồ sơ làm việc. Không để mã đó thay cho trích dẫn trong văn bản nộp.

## Trạng thái kiểm chứng

- `unverified`: nguồn hoặc metadata chưa được xác minh.
- `metadata_only`: đã kiểm tra tác giả/năm/tiêu đề/DOI nhưng chưa đủ căn cứ xác nhận nội dung hỗ trợ nhận định.
- `content_checked`: đã đọc nội dung liên quan và ghi `checked_locations`. Trạng thái này vẫn cần người đọc đánh giá độ phù hợp của nghiên cứu và nhận định.

DOI hợp lệ về hình thức không chứng minh bài báo tồn tại hoặc hỗ trợ câu viết. Ghi rõ chỉ đọc tóm tắt nếu đó là phạm vi tiếp cận. Link không mở được phải được báo riêng; không tự bù thông tin còn thiếu. Hồ sơ chỉ có khai báo `content_checked` chưa phải bằng chứng độc lập rằng việc đọc đã xảy ra.

## Danh mục và các trường hợp thiếu

Sắp xếp theo tác giả/tổ chức nếu chuẩn yêu cầu alphabet, hoặc theo số/thứ tự xuất hiện khi đề quy định; định dạng theo loại nguồn. Lưu DOI nếu có; với web, giữ URL và ngày truy cập khi hướng dẫn yêu cầu. Mỗi trích dẫn trong bài phải có entry danh mục, mỗi entry phải được dùng đúng phạm vi hoặc xử lý theo loại danh mục giảng viên yêu cầu.

Không tự đặt tác giả, năm, trang hoặc tiêu đề. Với metadata thiếu, đối chiếu hướng dẫn và hỏi khi ảnh hưởng đến tính đúng; phần chưa giải quyết được nêu ở ghi chú riêng. Với cùng tác giả/cùng năm, cần cách phân biệt rõ theo hướng dẫn. Không tự xóa hậu tố làm hai nguồn trở nên không phân biệt được.

Khi chuyển chuẩn theo yêu cầu mới, cập nhật nhất quán cả thân bài, danh mục và các trường hợp đặc biệt, rồi kiểm tra lại. `build_prompt.py` đổi chuẩn trong chỉ dẫn; nó không tự định dạng hoặc sửa citation của bản luận văn.
