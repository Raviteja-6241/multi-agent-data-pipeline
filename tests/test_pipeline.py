"""
Lightweight smoke tests that don't require API calls -
they verify the project structure and data loading logic,
which is enough for a CI badge without burning API credits.
"""

import os
import pandas as pd


def test_sample_data_exists():
    assert os.path.exists("data/sample_sales_data.csv")


def test_sample_data_loads():
    df = pd.read_csv("data/sample_sales_data.csv")
    assert len(df) > 0
    assert "order_id" in df.columns
    assert "quantity" in df.columns


def test_project_structure():
    assert os.path.exists("src/agents.py")
    assert os.path.exists("src/tasks.py")
    assert os.path.exists("src/crew.py")
    assert os.path.exists("src/tools.py")
    assert os.path.exists("main.py")
