---
name: code-learn
description: Use when fixing bugs in a Python package to ensure all tests pass, house rules (types, changelog, regression tests) are met, and specific formatting/rounding logic is correct.
---
# Code Learning & Bug Fixing Protocol

1. **Preserve Tests**: Never modify existing files in `tests/`. Only add new test files if required by rules.
2. **Type Annotations**: Ensure every public function (name not starting with `_`) has type annotations for all parameters and the return value.
3. **Price Parsing**:
   - Handle currency symbols (`$`), commas (thousands separators), and parentheses (negative values).
   - Example: `'$1,299.50'` -> `1299.50`, `'(12.00)'` -> `-12.00`.
4. **Rounding Logic**:
   - Use `decimal.Decimal` with `ROUND_HALF_UP` for financial calculations to avoid floating-point errors.
   - Ensure discount calculations round correctly (e.g., `2.665` with 0% discount should remain `2.67` if rounding to 2 decimals, or handle precision explicitly).
5. **CSV Formatting**:
   - Follow docstring specifications for quoting. If a field contains commas or quotes, it must be quoted.
   - Ensure `to_csv_row` returns a valid string, not an error object.
6. **Sorting & Filtering**:
   - Check docstrings for sorting requirements (e.g., case-insensitive, specific key).
   - Ensure `low_stock` or similar filters return items in the specified order.
7. **House Rules Compliance**:
   - **Changelog**: Add a `## Unreleased` section to `CHANGELOG.md` with bullet points `- fix(<function name>): <short description>` for each bug fixed.
   - **Regression Tests**: Create `tests/test_regressions.py` with at least one test function per bug fixed. Ensure these tests pass.
8. **Verification**: Run the full test suite (`pytest`) to confirm all checks pass before finishing.