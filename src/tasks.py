"""
Task definitions - these describe *what* each agent must do and
*what output* is expected, and chain together via `context` so each
agent can see the previous agent's work.
"""

from crewai import Task


def build_extraction_task(agent, data_path: str) -> Task:
    return Task(
        description=(
            f"Load the CSV file located at '{data_path}' using the Read CSV "
            "Data tool. Report the number of rows/columns and list the "
            "column names and data types you observe."
        ),
        expected_output=(
            "A short structural summary of the dataset plus the full data "
            "rendered as a markdown table."
        ),
        agent=agent,
    )


def build_validation_task(agent, context_tasks) -> Task:
    return Task(
        description=(
            "Review the extracted data for quality issues. Specifically "
            "check for: missing/null values, negative or zero quantities, "
            "duplicate order_ids, and any pricing anomalies. For each issue "
            "found, build a JSON object with fields: issue_id (e.g. "
            "'DQ-<order_id>'), source ('data-pipeline-validator'), category "
            "(one of 'missing_value', 'negative_quantity', 'duplicate', "
            "'pricing_anomaly'), description, affected_records (list of "
            "order_ids), raised_at (use today's date in ISO 8601), and "
            "raw_severity_hint ('low'/'medium'/'high' based on your best "
            "judgment). Collect all issues into a single JSON array and "
            "save it using the Write Issues JSON tool to "
            "'output/issues.json'."
        ),
        expected_output=(
            "A markdown bulleted list of data quality issues, grouped by "
            "issue type, each referencing the specific order_id(s) affected, "
            "plus confirmation that output/issues.json was written "
            "successfully in the shared Issue schema."
        ),
        agent=agent,
        context=context_tasks,
    )


def build_summary_task(agent, context_tasks) -> Task:
    return Task(
        description=(
            "Using the extracted data and the data quality findings, write "
            "a business-facing report. Include: (1) total revenue and units "
            "sold, (2) revenue by region, (3) top-selling product, "
            "(4) a 'Data Quality Notes' section summarizing the issues found, "
            "(5) 2-3 recommended next steps. Save the final report using the "
            "Write Report File tool to 'output/final_report.md'."
        ),
        expected_output=(
            "Confirmation that the report was written to disk, plus the "
            "full report content."
        ),
        agent=agent,
        context=context_tasks,
    )
