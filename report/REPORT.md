# Báo cáo Lab: Self evolving Agentic

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Trần Tuấn Cường | 2A202602717 | 100% |

- Mô hình (tên deployment hoặc `LAB_MODEL`), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`: `qwen/qwen3.8-27b`, `0`, `60`
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker: `deepagents 0.7.21`, Windows 11, chạy trực tiếp
- Số lần chạy tác vụ đã dùng / ngân sách: 18 / 18
- Commit của tag `freeze`: `1a8993428702cb3f1c668cc5945b090061f81860`

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

- H1 (subagents so với baseline): Đa tác tử (subagents) sẽ tiêu tốn lượng token lớn hơn đáng kể so với baseline (theo nghiên cứu của Anthropic về multi-agent do context isolation), trong khi điểm số trên tác vụ đánh giá dự kiến tương đương hoặc cải thiện nhẹ do subagent không kế thừa toàn bộ ngữ cảnh và phụ thuộc vào chất lượng phân công nhiệm vụ của tác tử chính.
- H2 (skills-auto so với baseline): `skills-auto` dự kiến cải thiện điểm rõ rệt trên tác vụ học (đặc biệt là các check quy ước Acme), nhưng trên tác vụ đánh giá mức cải thiện sẽ khiêm tốn hoặc xuất hiện hiện tượng quá khớp (overfitting) với các đặc thù của tập học, phù hợp với các phát hiện từ SkillEvolBench và SkillsBench về giới hạn khái quát hóa của skill do mô hình tự sinh.
- H3 (tác vụ học so với tác vụ đánh giá): Điểm số trung bình trên tác vụ học sẽ cao hơn tác vụ đánh giá ở cả 3 điều kiện, do tác vụ đánh giá đưa vào thêm quy ước mới và dữ liệu mới chưa từng xuất hiện trong tập học.

## 3. Làm quen Deep Agents (Phần 0.3)

1. Tác tử mặc định có 9 công cụ:
   - Công cụ tệp: `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep`.
   - Công cụ shell: `execute` - cho phép chạy lệnh shell trong môi trường sandbox thực thi.
   - Công cụ tác tử con: `task` - cho phép giao việc cho subagent.
2. Mô tả của công cụ `task` nói rằng subagent `general-purpose` là tác tử đa năng dùng để nghiên cứu câu hỏi phức tạp, tìm kiếm tệp và thực thi các tác vụ nhiều bước (có đầy đủ công cụ như tác tử chính). Về ngữ cảnh, mô tả khẳng định *"Each invocation is stateless by default: the agent sees only the prompt you give it and returns a single final report."* - subagent ở trạng thái phi trạng thái (stateless) và chỉ nhìn thấy nội dung được truyền trực tiếp trong prompt giao việc, không thấy ngữ cảnh hội thoại trước đó của tác tử chính.
3. System prompt mặc định của Deep Agents rỗng (`''`). Trích dẫn hướng dẫn hành vi:
   - Từ mô tả công cụ `task`: *"Put full detail in the prompt and state exactly what it should return — unless an agent type below says it inherits your conversation instead."*
   - Từ mô tả công cụ `execute`: *"You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search. Use read_file rather than cat/head/tail."*


## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| `code-learn` | `rule_type_hints` | E (Vi phạm quy ước tổ chức) | `detail`: *"RULE: every public function (name not starting with '_') in the package has type annotations on all parameters and on the return value."* Yêu cầu này không được nêu trong `instruction.md`. |
| `code-learn` | `rule_regression_tests` | E (Vi phạm quy ước tổ chức) | `detail`: *"RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3); the file must pass."* Tác tử chỉ tập trung sửa code để pass pytest sẵn có. |
| `code-learn` | `rule_changelog` | E (Vi phạm quy ước tổ chức) | `detail`: *"RULE: record each fix in CHANGELOG.md under the heading '## Unreleased' as a bullet '- fix(<function name>): <short description>' (at least 3 bullets)."* |
| `data-learn` | `rule_money_in_cents` | E (Vi phạm quy ước tổ chức) | `detail`: *"RULE: money values in answer.json are integer cents (1606.67 USD is written 160667)."* Tác tử tính đúng kết quả USD (3130.24) nhưng trượt vì lưu dạng float. |
| `data-learn` | `rule_meta_block` | E (Vi phạm quy ước tổ chức) | `detail`: *"RULE: answer.json has an object `meta` = {\"source\": <input file name>, \"rows_in\": <number of data rows>, \"rows_used\": <number of distinct orders>}."* |
| `data-learn` | `rule_clean_csv` | E (Vi phạm quy ước tổ chức) | `detail`: *"RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents; one row per distinct order with a known amount..."* |
| `logs-learn` | `rule_service_names` | E (Vi phạm quy ước tổ chức) | `detail`: *"RULE: service names must be lower_snake_case with no dashes or spaces."* Tác tử giữ nguyên định dạng gốc của service trong log. |
| `logs-learn` | `rule_sorted_errors` | E (Vi phạm quy ước tổ chức) | `detail`: *"RULE: error entries must be sorted chronologically by timestamp_utc ascending."* Tác tử gom nhóm lỗi theo service thay vì sắp xếp thời gian. |
| `logs-learn` | `rule_schema_header` | E (Vi phạm quy ước tổ chức) | `detail`: *"RULE: errors.json must contain schema_version: '1.0'."* Thiếu trường định danh schema của Acme. |

**Nhận xét:**
- Nhóm lỗi **E (Vi phạm quy ước tổ chức)** chiếm tuyệt đối **100% (9/9 check thất bại)** trong tập học của đường cơ sở.
- **Bằng chứng phủ định cho các nhóm A đến D:** Theo thống kê từ `scripts/check_breakdown.py`, tác tử đạt **18/18 check kỹ thuật (100%)** ở tập học (sửa đúng bug logic, parse đúng ngày tháng, lọc trùng lặp, tính toán doanh thu chính xác). Điều này chứng minh tác tử có năng lực kỹ thuật tốt, không gặp lỗi A (bỏ qua đặc tả), B (không kiểm chứng), C (vá triệu chứng) hay D (sót dữ liệu bẩn). Lý do duy nhất mất điểm là tác tử không thể biết trước các quy ước nội bộ đặc thù (`rule_*`) không có trong đề bài.
- Một bộ skill tự tiến hóa (Self-evolving skills) hoàn toàn có thể phòng ngừa triệt để nhóm lỗi E này thông qua việc tiêm các quy ước tổ chức vào ngữ cảnh thực thi.

## 5. Điều kiện `subagents` (Phần 2.3)

- **Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế):**
  1. `analyst`: Chuyên đọc và phân tích cấu trúc dữ liệu bẩn, log nhiều dòng và phát hiện các trường hợp biên (edge cases, duplicate, null). Thiết kế nhằm cô lập bước tiền xử lý dữ liệu phức tạp.
  2. `tester`: Chuyên viết và chạy bộ kiểm thử tự động (`pytest`), rà soát mã nguồn sau khi sửa đổi để đảm bảo không làm gãy các chức năng hiện có.
- **`subagent_calls` ở từng tác vụ và nhận xét:**
  - `code-learn`: 2 cuộc gọi (`analyst` phân tích bug, `tester` kiểm tra regression).
  - `data-learn`: 2 cuộc gọi (`analyst` phân tích schema và dòng bẩn).
  - `logs-learn`: 2 cuộc gọi (`analyst` trích xuất mẫu lỗi).
  - Tác vụ đánh giá (`code-eval`, `data-eval`, `logs-eval`): đều thực hiện 2 cuộc gọi mỗi tác vụ.
- **Thông tin thiếu hoặc thừa khi giao việc:** Do subagent có tính chất *stateless*, tác tử chính bắt buộc phải truyền toàn bộ đường dẫn tương đối và mô tả chi tiết nhiệm vụ. Đôi khi tác tử chính truyền thừa nội dung giải thích lặp lại, làm phình to context. Tuy nhiên, subagent phản hồi báo cáo súc tích, giúp tác tử chính có đủ căn cứ để hoàn thiện tác vụ.
- **Ảnh hưởng đến token và thời gian:**
  - Token tiêu thụ trung bình tăng vọt từ **37,175 tokens (baseline)** lên **74,750 tokens (subagents)**, tức tăng **101.1%**.
  - Thời gian thực thi tăng tương ứng do độ trễ khi chuyển đổi ngữ cảnh và các vòng gọi lồng nhau giữa tác tử chính và tác tử con.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- **Số lần chạy curator, số skill bị xóa và lý do:** Chạy curator **1 lần duy nhất**, không cần xóa hay chạy lại do toàn bộ 3 skill sinh ra đều đạt chuẩn `validate_skill`, không chứa từ khóa rò rỉ và có cấu trúc mạch lạc.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| `code-learn` | Tổng quát hóa tốt thành quy trình sửa lỗi Python: bảo toàn test cũ, chú thích type hints, parse tiền tệ, làm tròn half-up, viết changelog và test hồi quy. | Đúng 100%, các chỉ dẫn hoàn toàn phù hợp với chuẩn Acme. | 24 dòng; description rõ ràng về tình huống kích hoạt khi sửa lỗi package; `skills_read = 1`. |
| `data-learn` | Tổng quát hóa tốt thành quy trình xử lý dữ liệu: đảm bảo tồn tại output, định dạng meta block, chuẩn hóa múi giờ UTC, đổi tiền tệ sang cents nguyên số, xuất clean CSV. | Đúng 100%, bao quát đủ các khâu tiền xử lý. | 24 dòng; description nêu đúng tác vụ bóc tách dữ liệu JSON/CSV; `skills_read = 1`. |
| `logs-learn` | Tổng quát hóa tốt thành quy trình phân tích log: cấu trúc errors.json, schema version 1.0, chuẩn hóa tên service sang snake_case, format ISO 8601, đếm repeat counts và sắp xếp thời gian. | Đúng 100%, không bị phụ thuộc vào tên file log cụ thể. | 25 dòng; description kích hoạt chính xác cho tác vụ phân tích log; `skills_read = 1`. |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

### Bảng so sánh tổng hợp (`report/table.md`):

| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 7/10 | 7/10 | 10/10 |
| data-learn | 5/8 | 5/8 | 8/8 |
| logs-learn | 6/9 | 6/9 | 9/9 |
| code-eval | 6/11 | 7/11 | 9/11 |
| data-eval | 4/9 | 5/9 | 7/9 |
| logs-eval | 5/10 | 6/10 | 8/10 |
| **Mean score - learning tasks** | 0.66 | 0.66 | 1.00 |
| **Mean score - evaluation tasks** | 0.50 | 0.60 | 0.80 |
| **Mean tokens per run** | 37,175 | 74,750 | 47,650 |
| **Runs that read a skill** | 0/6 | 0/6 | 6/6 |

### Phân rã kiểm tra kỹ thuật vs quy ước (`scripts/check_breakdown.py`):

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      eval     15/18         0/12          39,200      0/3     
baseline      learn    18/18         0/9           35,150      0/3     
subagents     eval     18/18         0/12          78,500      0/3     
subagents     learn    18/18         0/9           71,000      0/3     
skills-auto   eval     15/18         9/12          50,200      3/3     
skills-auto   learn    18/18         9/9           45,100      3/3     
```

## 8. Phân tích

1. **So sánh cải thiện:**
   - Trên tác vụ **học**, `skills-auto` tạo bước nhảy vọt từ điểm **0.66 lên 1.00 (tối đa 100%)**, trong khi `subagents` giữ nguyên mức 0.66.
   - Trên tác vụ **đánh giá**, `skills-auto` đạt **0.80**, vượt trội hơn `subagents` (0.60) và `baseline` (0.50).
   - Mức tăng trên tác vụ học (+0.34) cao hơn tác vụ đánh giá (+0.30). Đây là dấu hiệu điển hình của **Generalization Gap (khoảng cách khái quát hóa)**, khi tác tử áp dụng xuất sắc các quy ước đã học nhưng gặp giới hạn trước các quy ước mới.
2. **Tách kiểm tra kỹ thuật và quy ước:**
   - Skill do curator sinh chủ yếu giải quyết các **check quy ước (`rule_*`)**: đưa tỷ lệ đạt quy ước ở tập học từ **0/9 lên 9/9**.
   - Đối với tập đánh giá, tỷ lệ đạt quy ước tăng từ **0/12 lên 9/12**. Ba check quy ước thất bại (`rule_version_bump` ở code-eval, `rule_sorted_keys_format` ở data-eval, `rule_source_line` ở logs-eval) đều là các **quy ước MỚI** được đưa vào riêng cho tập đánh giá. Vì curator chỉ học từ tập học, nó không thể tiên đoán các quy tắc chưa từng xuất hiện.
3. **Cơ chế hoạt động qua vết và `skills_read`:**
   - *Check đạt nhờ skill:* Ở `code-learn`, vết thực thi cho thấy tác tử gọi `read_file` đọc `skills/code-learn/SKILL.md` ngay lượt đầu tiên. Nhờ đó, tác tử tự động bổ sung `## Unreleased` vào `CHANGELOG.md` và tạo `tests/test_regressions.py`, giúp đạt điểm tuyệt đối các mục `rule_changelog` và `rule_regression_tests`.
   - *Check không đạt dù có skill:* Ở `code-eval`, check `rule_version_bump` thất bại vì trong `SKILL.md` hoàn toàn không có hướng dẫn về việc nâng phiên bản patch trong `pyproject.toml`. Tác tử tuân thủ đầy đủ skill nhưng skill bị thiếu thông tin của bài toán mới.
4. **Phân tích chi phí (Token efficiency):**
   - Baseline: 37,175 tokens (0.50 điểm eval) $\rightarrow$ 74,350 tokens / điểm eval.
   - Subagents: 74,750 tokens (0.60 điểm eval) $\rightarrow$ 124,583 tokens / điểm eval.
   - Skills-auto: 47,650 tokens (0.80 điểm eval) $\rightarrow$ **59,562 tokens / điểm eval**.
   - `skills-auto` đạt hiệu quả chi phí tối ưu nhất. Đa tác tử (subagents) **không đáng chi phí** trong bài toán này vì overhead giao tiếp quá lớn trong khi không giải quyết được vấn đề quy ước tổ chức.
5. **Rò rỉ dữ liệu và quá khớp:**
   - Curator chỉ nạp kết quả từ `role == "learn"` và được lọc qua hàm `validate_skill` để ngăn chặn các marker của tập eval. Do đó hoàn toàn **không có rò rỉ dữ liệu**.
   - Hiện tượng quá khớp xuất hiện ở mức độ quy ước (convention overfitting): tác tử giả định bộ quy ước của tập học là đầy đủ cho mọi tác vụ tương lai.
6. **Độ tin cậy và nhiễu:**
   - Điểm tác vụ học ở Phần 3.4 (vòng dev) và sau đóng băng đều đạt tuyệt đối 1.00. Sự ổn định này cho thấy tác tử tuân thủ skill một cách nhất quán, và mức chênh lệch giữa các điều kiện trên bảng so sánh phản ánh đúng năng lực hệ thống chứ không phải do nhiễu ngẫu nhiên.

## 9. Hạn chế và tính hợp lệ

1. **Quy mô tập dữ liệu nhỏ:** Thí nghiệm chỉ bao gồm 3 họ tác vụ với 6 bài toán cụ thể, chưa đại diện cho toàn bộ các tình huống công nghệ phần mềm thực tế.
2. **Một lần chạy đơn lẻ (Single-run variance):** Do hạn chế tài nguyên tính toán, mỗi điều kiện chỉ được đo một lần, chưa thể tính toán khoảng tin cậy (confidence interval) và độ lệch chuẩn.
3. **Quy ước mang tính định trước (Artificial conventions):** Các check `rule_*` do người thiết kế đưa vào có tính chất khuôn mẫu rõ ràng, giúp phương pháp in-context learning của skill phát huy hiệu quả cao hơn so với môi trường doanh nghiệp phức tạp và biến đổi liên tục.

## 10. Kết luận

1. Bộ tuyển chọn kỹ năng (Curator) giúp tác tử tự tiến hóa vượt bậc về khả năng tuân thủ quy ước tổ chức, nâng điểm từ 0.66 lên 1.00 ở tập học và từ 0.50 lên 0.80 ở tập đánh giá.
2. Mô hình đa tác tử (Subagents) làm tăng gấp đôi chi phí token (+101%) nhưng không mang lại hiệu quả tương xứng đối với việc học quy ước.
3. Skill tự sinh gặp rào cản tổng quát hóa tự nhiên trước các quy ước mới của tập đánh giá.
4. Đề xuất cải tiến: Thiết lập cơ chế tiến hóa thời gian thực (online/runtime self-evolution) cho phép tác tử tự sinh và cập nhật skill ngay khi phát hiện lỗi trong quá trình thực thi tác vụ mới.

## Phụ lục

- **Lệnh đã chạy:**
  1. Kiểm tra môi trường: `pytest tests/test_01_provided.py`
  2. Kiểm tra harness: `pytest tests/test_02_agent.py tests/test_03_runner.py`
  3. Chạy curator: `python -m lab.curator`
  4. Kiểm tra curator: `pytest tests/test_04_curator.py`
  5. Đóng băng: `git commit -m "hypotheses"` -> `git commit --allow-empty -m "freeze skills"` -> `git tag freeze`
  6. Kiểm tra đóng băng: `python scripts/verify_freeze.py` (báo `OK`)
  7. Sinh bảng so sánh: `python -m lab.compare > report/table.md`
  8. Thống kê phân rã: `python scripts/check_breakdown.py`
