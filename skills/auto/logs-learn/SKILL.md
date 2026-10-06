---
name: logs-learn
description: Use when parsing log files to extract error entries into a structured JSON file with specific schema, sorting, and aggregation rules.
---
# Log Parsing & Error Extraction Protocol

1. **File Existence**: Always create the required output file (e.g., `workspace/errors.json`) before finishing.
2. **Schema Compliance**:
   - Ensure the JSON structure matches the required schema (e.g., list of error objects).
   - Include a `schema_header` or metadata block if required by rules.
3. **Timestamp Handling**:
   - Convert all timestamps to UTC.
   - Format as ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
4. **Field Extraction**:
   - Extract exception details (type, message, stack trace) into dedicated fields.
   - Ensure service names are canonicalized (e.g., lowercase, no spaces).
5. **Aggregation**:
   - Calculate `repeat_counts` for each unique error signature.
   - Calculate `counts_by_service` for each service.
6. **Sorting**:
   - Sort the final list of errors according to the rule (e.g., by timestamp, service name, or error type).
7. **Verification**:
   - Check that `errors.json` is valid JSON.
   - Verify that all required fields are present for each entry.
   - Ensure counts and aggregations are consistent with the extracted entries.