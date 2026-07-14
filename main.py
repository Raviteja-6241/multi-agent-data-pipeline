"""
Multi-Agent Data Pipeline
--------------------------
Entry point. Run with:

    python main.py

This kicks off a 3-agent CrewAI pipeline:
  1. Extractor Agent  - loads raw CSV data
  2. Validator Agent   - flags data quality issues
  3. Summarizer Agent  - writes an executive markdown report to output/

Requires OPENAI_API_KEY (or your chosen provider's key) set in a .env file.
"""

from dotenv import load_dotenv
from src.crew import run_pipeline

load_dotenv()

DATA_PATH = "data/sample_sales_data.csv"


def main():
    print(f"Starting pipeline on: {DATA_PATH}\n{'=' * 50}")
    result = run_pipeline(DATA_PATH)
    print("\n" + "=" * 50)
    print("PIPELINE COMPLETE")
    print("=" * 50)
    print(result)


if __name__ == "__main__":
    main()
