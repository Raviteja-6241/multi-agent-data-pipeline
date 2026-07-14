"""
Assembles the agents and tasks into a sequential Crew and exposes a
single `run_pipeline` function used by main.py.
"""

from crewai import Crew, Process
from src.agents import (
    build_extractor_agent,
    build_validator_agent,
    build_summarizer_agent,
)
from src.tasks import (
    build_extraction_task,
    build_validation_task,
    build_summary_task,
)


def run_pipeline(data_path: str) -> str:
    extractor = build_extractor_agent()
    validator = build_validator_agent()
    summarizer = build_summarizer_agent()

    extraction_task = build_extraction_task(extractor, data_path)
    validation_task = build_validation_task(validator, context_tasks=[extraction_task])
    summary_task = build_summary_task(summarizer, context_tasks=[extraction_task, validation_task])

    crew = Crew(
        agents=[extractor, validator, summarizer],
        tasks=[extraction_task, validation_task, summary_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return result
