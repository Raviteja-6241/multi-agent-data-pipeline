"""
Custom tools shared by the agents in the pipeline.

CrewAI agents call these tools to interact with the outside world
(reading raw data, writing the final report) instead of hallucinating
file contents.
"""

import os
import json
import pandas as pd
from crewai.tools import tool


@tool("Read CSV Data")
def read_csv_data(file_path: str) -> str:
    """
    Reads a CSV file and returns its contents as a markdown table string,
    along with basic shape info. Use this to load raw business data
    before validating or summarizing it.
    """
    if not os.path.exists(file_path):
        return f"ERROR: File not found at {file_path}"

    df = pd.read_csv(file_path)
    summary = f"Loaded {len(df)} rows, {len(df.columns)} columns from {file_path}.\n\n"
    summary += df.to_markdown(index=False)
    return summary


@tool("Write Report File")
def write_report_file(content: str, output_path: str = "output/final_report.md") -> str:
    """
    Writes the given text content to a markdown file at output_path.
    Use this as the final step to save the summarized report to disk.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Report successfully written to {output_path}"


@tool("Write Issues JSON")
def write_issues_json(issues_json: str, output_path: str = "output/issues.json") -> str:
    """
    Writes a JSON array of data-quality issues to output_path, following the
    shared Issue schema used across the Business Ops Agent Suite (see
    ISSUE_SCHEMA.md in the ticket-triage-agent repo). Each issue must have:
    issue_id, source, category, description, affected_records, raised_at,
    raw_severity_hint. Pass issues_json as a valid JSON array string.
    Use this so downstream agents (e.g. the Ticket Triage Agent) can consume
    the findings directly.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Validate it's parseable JSON before writing, fail loudly if not.
    parsed = json.loads(issues_json)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2)
    return f"Wrote {len(parsed)} issues to {output_path}"
