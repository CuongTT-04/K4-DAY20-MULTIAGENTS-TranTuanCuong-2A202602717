---
name: data-learn
description: Use when processing raw data into a structured JSON answer file and a clean CSV, ensuring correct schema, units, and file existence.
---
# Data Processing & Output Protocol

1. **File Existence**: Always create the required output files (e.g., `workspace/answer.json`, `workspace/clean.csv`) before finishing. Do not assume they exist.
2. **JSON Structure**:
   - Ensure `answer.json` contains all required keys (e.g., `north_q1_revenue`, `top_region`).
   - Include a `meta` block if required by rules.
3. **Data Cleaning**:
   - **Deduplication**: Remove duplicate rows based on the primary key (e.g., `order_id`).
   - **Missing Data**: Exclude rows with missing critical fields (e.g., `amount`) from revenue calculations but track them if required.
   - **Canonicalization**: Normalize region names (e.g., `North`, `South`, `East`, `West`) and timestamps to UTC (`YYYY-MM-DDTHH:MM:SSZ`).
4. **Unit Conversion**:
   - Convert monetary values to **integer cents** for storage in `clean.csv` and calculations.
   - Ensure `amount_cents` is an integer, not a float.
5. **CSV Formatting**:
   - Header order must match the rule (e.g., `order_id,timestamp_utc,region,amount_cents`).
   - One row per distinct order with a known amount.
6. **Verification**:
   - Check that `answer.json` is valid JSON and readable.
   - Verify `clean.csv` has the correct header and row count.
   - Ensure all calculated metrics (revenue, order counts) are derived from the cleaned data.