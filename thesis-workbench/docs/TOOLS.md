# Công cụ và giới hạn kiểm tra

Python 3.10 trở lên; không cần pip, API key hoặc kết nối mạng. Các lệnh dưới chạy trong thư mục repo. Công cụ không gọi mô hình AI.

## Ghép prompt

```bash
python scripts/build_prompt.py --task general --out PROMPT_LUAN_VAN.md
python scripts/build_prompt.py --task review --profile templates/project.json --out output/review.md
python scripts/build_prompt.py --task review --profile examples/demo-project/project.json --state examples/demo-project/project_state.json --out output/review.md
python scripts/build_prompt.py --task draft --profile path/to/project.json --state path/to/project_state.json --request-file path/to/request.txt --out output/request.md
python scripts/build_prompt.py --task citations --profile path/to/project.json
```

Task hợp lệ xem `prompts/README.md` hoặc `--help`. Nếu không truyền `--out`, prompt được in stdout. Khi có `--profile`, JSON được đưa vào như dữ liệu bối cảnh, giữ nguyên giá trị của người viết. `null` không bị điền bằng thông tin tự tạo. Đường dẫn nguồn trong hồ sơ không đồng nghĩa nội dung nguồn đã được truy cập.

`citation_style` nhận đúng `Harvard` hoặc `APA`; `word_limit` là số nguyên dương hoặc `null`. Script thay chuẩn trong quy tắc, không đọc/sửa luận văn. `--request-file` giữ nguyên yêu cầu gốc trong JSON để mô hình làm rõ ý nghĩa và cấu trúc. Không có lời gọi mô hình hay API trong script.

Với task làm bài, nếu hồ sơ chưa rõ hoặc chưa xác nhận, script thay module công đoạn bằng module hỏi/làm rõ. Tạo được file prompt trả 0 không có nghĩa được phép làm bài: đọc trạng thái trong prompt. Lỗi đầu vào trả exit code 2. `--task optimize` chỉ sửa prompt, không thực hiện nhiệm vụ bên trong.

Khi thiếu môn hoặc ngành, gate ưu tiên hỏi hai điểm đó trước (`intake_stage=course_and_discipline`), giữ các câu hỏi dự án khác để xử lý ở lượt sau. Không có prompt viết sẵn không cản việc hỗ trợ trong chat; script không phải điều kiện để bắt đầu. Ngành IT được xử lý theo đề và sản phẩm thực tế, không có mặc định ngành Marketing.

## Kiểm tra bước hỏi/xác nhận

```bash
python scripts/project_gate.py --project templates --task draft
python scripts/project_gate.py --project examples/demo-project --task review
```

Đọc `project.json` và `project_state.json` nếu có. `clarify` là còn câu hỏi; `confirm` là cần xác nhận bản tóm tắt; `ready` là hồ sơ khai báo cho phép triển khai. Exit 1 khi chưa sẵn sàng, 0 khi ready hoặc chỉ tối ưu prompt, 2 khi lỗi đầu vào. Câu hỏi được chia lượt tối đa 3 câu; vẫn giữ toàn bộ điểm chưa giải quyết để không bỏ sót.

Chỉ sau xác nhận thực tế mới lưu message, profile_sha256 và brief_sha256 tương ứng. Không dùng fingerprint để tự tạo sự đồng ý. Đây là kiểm tra trạng thái khai báo, không chứng minh người viết đã xác nhận hoặc mô hình đã hiểu đúng. Mô hình phải hỏi tiếp nếu phát hiện mâu thuẫn ngay cả khi trạng thái máy là ready. Xem [PROJECT_DIALOGUE](PROJECT_DIALOGUE.md).

## Kiểm tra hồ sơ dự án

```bash
python scripts/audit_project.py --project examples/demo-project
python scripts/audit_project.py --project path/to/project --out output/audit.json
```

Thư mục cần có `project.json`, `sources.json`, `claims.csv`, `requirements.csv`. Script kiểm tra:

- Cấu trúc hồ sơ, trường quan trọng còn trống và các trạng thái khai báo.
- ID nguồn/nhận định/yêu cầu thiếu hoặc trùng.
- Nhận định ngoài không liên kết nguồn, nguồn liên kết không tồn tại trong sổ.
- Nhận định ghi supported nhưng nguồn chưa khai kiểm tra nội dung hoặc thiếu entry danh mục.
- Nguồn ghi đã đọc nhưng thiếu vị trí bằng chứng; nhận định thiếu ghi chú căn cứ.
- Yêu cầu bắt buộc còn pending/partial; yêu cầu covered thiếu phần/bằng chứng.
- Hình thức URL, DOI và ngày truy cập nếu có.
- Bước hỏi/xác nhận dự án còn thiếu hoặc không còn khớp hồ sơ hiện hành.

Exit code: `0` = không có lỗi cấu trúc được phát hiện; `1` = có findings; `2` = không đọc/kiểm tra được đầu vào. Báo cáo luôn có `semantic_checks: not_performed` và giới hạn kiểm tra. `notes` chỉ là ghi chú, không đổi exit code.

Script không kiểm chứng web hoặc file bằng chứng, không đánh giá nguồn có thật hay hỗ trợ đúng câu, không so citation với thân bài, không chấm rubric và không chứng nhận sẵn sàng nộp. Trạng thái supported/content_checked/covered là khai báo cần được đối chiếu bởi người đọc. Chỉ sau các bước đọc, phân tích và tự rà thực tế mới được nhận xét về chất lượng bài.

## Kiểm tra hồ sơ tự chấm

```bash
python scripts/audit_self_review.py --report reviews/repo-v1.2.0.json
```

Kiểm tra tiêu chí có lý do/bằng chứng, lỗi resolved có căn cứ kiểm tra sau sửa, kết luận ready không mâu thuẫn với tiêu chí/lỗi còn mở và điểm/mức đạt có khai báo rubric. Exit 0 là không có mâu thuẫn cấu trúc được phát hiện; 1 là có findings; 2 là lỗi đầu vào. Công cụ không đọc bài, xác minh căn cứ, tính điểm hoặc chứng minh đánh giá không thiên vị. Xem [CANDID_REVIEW](CANDID_REVIEW.md).

## Kiểm tra repo

```bash
python scripts/verify_repo.py
python -m unittest discover -s tests -v
```

`verify_repo.py` đối chiếu hash snapshot được phân phối, JSON/CSV gốc, prompt tổng so với nguồn và các liên kết nội bộ. Manifest giúp phát hiện thay đổi so với bản đã ghi nhận, không phải chữ ký số xác thực độc lập. Tests bao gồm lỗi hồ sơ, bảo toàn biến trong bối cảnh, chuyển chuẩn trong prompt và snapshot bị sửa.

Thay quy tắc/module thì sinh lại `PROMPT_LUAN_VAN.md`, chạy kiểm tra và tests. Khi cập nhật kho prompt upstream, giữ nguyên metadata tác giả, ghi commit mới, tuyển lại có đọc nội dung và cập nhật manifest/provenance; không tự nhập tất cả prompt làm chỉ dẫn thi hành.
