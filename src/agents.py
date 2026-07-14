"""
Agent definitions for the multi-agent data pipeline.

Three specialized agents, each with a narrow responsibility -
this separation of concerns is what makes the pipeline "agentic"
rather than just one long prompt.
"""

from crewai import Agent, LLM
from src.tools import read_csv_data, write_report_file, write_issues_json
import os

# Centralized LLM config so it's easy to swap providers/models later.
llm = LLM(
    model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
    temperature=0.2,
)


def build_extractor_agent() -> Agent:
    return Agent(
        role="Data Extraction Specialist",
        goal="Load raw business data accurately and describe its structure "
             "so downstream agents know exactly what they're working with.",
        backstory=(
            "You are a meticulous data engineer who has spent years pulling "
            "data out of messy source systems. You never guess at data you "
            "haven't actually loaded."
        ),
        tools=[read_csv_data],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def build_validator_agent() -> Agent:
    return Agent(
        role="Data Quality Analyst",
        goal="Identify data quality issues such as missing values, negative "
             "quantities, duplicate orders, or inconsistent formatting, and "
             "produce a clear list of issues with row-level detail.",
        backstory=(
            "You are a former auditor turned data quality analyst. You are "
            "skeptical by nature and flag anything that looks off before it "
            "reaches a business stakeholder."
        ),
        tools=[write_issues_json],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def build_summarizer_agent() -> Agent:
    return Agent(
        role="Business Reporting Analyst",
        goal="Turn validated data and the data quality findings into a "
             "concise, executive-friendly markdown report with key metrics "
             "and recommended next steps.",
        backstory=(
            "You are a business systems analyst who translates technical "
            "findings into clear, actionable summaries for non-technical "
            "stakeholders."
        ),
        tools=[write_report_file],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
