# Luận Văn AI Workbench

Bộ prompt và quy trình hỗ trợ luận văn theo ngành và môn thực tế, bao gồm IT và Marketing. Repo kết hợp 12 prompt học thuật được tuyển từ [f/prompts.chat](https://github.com/f/prompts.chat) với yêu cầu viết, kiểm chứng, trích dẫn và tự rà soát của người viết.

## Dùng ngay

Có thể chat thẳng như “Tao cần làm luận”, không cần tự viết prompt. AI hỏi môn và ngành còn thiếu trước, rồi hỏi tiếp từng nhóm cho đến khi hiểu công việc. Xem [cách bắt đầu và câu hỏi cho IT](docs/PROJECT_INTAKE.md).

1. Mở [PROMPT_LUAN_VAN.md](PROMPT_LUAN_VAN.md), copy toàn bộ vào cuộc trò chuyện.
2. Gửi đề, rubric, dàn ý, mẫu trích dẫn của giảng viên và tài liệu liên quan.
3. Nói rõ việc cần làm. Ở lần bắt đầu dự án, AI cần đọc đầu vào, hỏi những điểm chưa rõ, tóm tắt cách hiểu và đợi mày xác nhận trước khi viết hoặc phân tích.
4. Sau khi chốt, tiếp tục công việc trong phạm vi đó. Khi có thông tin mới ảnh hưởng cách làm, hỏi lại phần bị ảnh hưởng và cập nhật hồ sơ; không hỏi lại những điều đã chốt còn hiệu lực.

Từ bản 1.1.0, mỗi yêu cầu trong dự án được tự làm rõ thành mục tiêu, đầu vào, phạm vi, ràng buộc và đầu ra trước khi thực hiện. Không cần gọi `$prompt-optimizer` mỗi lần. Điểm chưa rõ được đưa thành câu hỏi, không được tự lấp bằng giả định. Xem [quy trình hỏi và xác nhận](docs/PROJECT_DIALOGUE.md).

Từ bản 1.2.0, phản biện dựa trên căn cứ thay vì mặc nhiên đồng ý, trao đổi thẳng và có thể cà khịa nhẹ theo bối cảnh. Phần nộp bài giữ giọng học thuật. Mỗi kết quả được tự rà công tâm theo cùng tiêu chí; không tự cho điểm hoặc kết luận đạt D thiếu căn cứ. Xem [CANDID_REVIEW](docs/CANDID_REVIEW.md).

Khi chỉ cần một công đoạn, đọc [danh mục prompt](prompts/README.md). Quy tắc chung luôn đi kèm prompt công đoạn. Không cần cài thư viện Python để copy prompt.

## Repo có gì?

| Thành phần | Công dụng |
| --- | --- |
| [PROMPT_LUAN_VAN.md](PROMPT_LUAN_VAN.md) | Prompt tổng đã gộp, dùng trực tiếp |
| [rules/core.vi.md](rules/core.vi.md) | Quy tắc dùng chung; nguồn để tạo prompt tổng |
| [prompts/](prompts/README.md) | 11 prompt công đoạn, điều phối, tối ưu prompt, làm rõ dự án và tự chấm |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | Từ đọc đề đến kiểm tra bản nộp |
| [docs/CITATION_POLICY.md](docs/CITATION_POLICY.md) | Harvard, đối chiếu nguồn và chuyển APA khi được yêu cầu |
| [templates/](templates/README.md) | Hồ sơ dự án, bảng yêu cầu, nguồn, nhận định và nhật ký tiến độ |
| [examples/](examples/README.md) | Cách đưa dữ liệu vào mẫu, bằng tình huống giả lập được ghi rõ |
| [upstream/](docs/PROVENANCE.md) | 12 prompt gốc, tác giả đóng góp, commit và mã kiểm tra |
| [scripts/](docs/TOOLS.md) | Ghép prompt, kiểm tra hồ sơ và kiểm tra tính toàn vẹn repo |

## Dùng công cụ tùy chọn

Cần Python 3.10 trở lên, chỉ dùng thư viện chuẩn. Chạy trong thư mục repo:

```bash
python scripts/build_prompt.py --task review --profile templates/project.json --out output/review.md
python scripts/project_gate.py --project examples/demo-project --task review
python scripts/audit_self_review.py --report reviews/repo-v1.2.0.json
python scripts/audit_project.py --project examples/demo-project
python scripts/verify_repo.py
python -m unittest discover -s tests -v
```

Thay `templates/project.json` bằng hồ sơ thực tế khi sử dụng. Khi tạo prompt cho phạm vi đã được xác nhận, truyền thêm `--state` như hướng dẫn trong [TOOLS](docs/TOOLS.md). Thiếu thông tin hoặc xác nhận hiện hành thì prompt được chuyển sang hỏi/làm rõ. Thư mục mẫu còn trống để điền, không phải một nghiên cứu đã hoàn thành. Công cụ audit chỉ kiểm tra hồ sơ có cấu trúc; việc đọc nguồn, đánh giá lập luận và chấm rubric cần được thực hiện riêng.

Có thể đọc và dùng prompt trực tiếp trên GitHub; không cần tải hay giải nén. Chỉ clone mã nguồn khi muốn chạy công cụ Python hoặc quản lý hồ sơ bằng file.

Để bắt đầu một dự án, copy các file trong `templates/` sang thư mục riêng, điền thông tin, rồi làm theo [WORKFLOW](docs/WORKFLOW.md). Giữ các tài liệu cá nhân, dữ liệu khảo sát và bản thảo riêng tư ngoài phần mã nguồn dùng chung.

## Nguồn và phạm vi

Các prompt cộng đồng được chuyển thành quy trình dùng theo ngành, môn và đề thực tế; những ví dụ đề tài và mặc định ngôn ngữ/APA trong prompt gốc được thay bằng hồ sơ dự án và yêu cầu của giảng viên. Kho prompt gốc được giữ riêng để đối chiếu, không phải chỉ dẫn tự động thi hành.

Bài [Brands Vietnam](https://help.brandsvietnam.com/vi/article/dau-hieu-nhan-biet-noi-dung-duoc-viet-boi-ai-3zy07d/) là tham khảo về chất lượng diễn đạt. Mục tiêu là văn bản rõ ràng, có lập luận và đúng nguồn. Repo không cung cấp công cụ xác định tác giả văn bản hay cam kết kết quả từ công cụ phát hiện AI.

Xem [PROVENANCE](docs/PROVENANCE.md), [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md) và [LICENSE](LICENSE) để biết nguồn, thay đổi và giấy phép. Repo dùng được cho nhiều môn; mã môn, cấu trúc chương, số từ và tiêu chí P/M/D chỉ được áp dụng khi đề hiện tại xác định.
