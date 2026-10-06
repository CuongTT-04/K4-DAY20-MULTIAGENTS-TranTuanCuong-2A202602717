"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use when you need to inspect raw datasets, log files, READMEs, specifications, or docstrings "
                "before taking action. The explorer analyzes files and reports findings without making changes."
            ),
            "system_prompt": (
                "You are an exploratory subagent. Your role is to examine files, specifications, docstrings, "
                "and raw datasets or log files. Report facts, schemas, anomalous rows, and requirements clearly "
                "and accurately back to the main agent. Do NOT modify any files."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when you have a clear plan and need to execute code fixes, data transformations, or create output files, "
                "and verify them by running python or tests."
            ),
            "system_prompt": (
                "You are an implementation subagent. Your role is to edit files, implement bug fixes, write data cleaning "
                "scripts, or create required outputs. Always test your modifications using the shell before reporting completion. "
                "Report exact changes made and test outcomes."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use when work is finished or in progress to independently verify output files, schemas, edge cases, "
                "and compliance with instructions and house rules."
            ),
            "system_prompt": (
                "You are an independent reviewer subagent. Your role is to inspect modified and generated files, "
                "verify correctness against all requirements and constraints, check for edge cases and regressions, "
                "and report any issues or confirm that all checks pass. Do NOT modify files."
            ),
        },
    ]

