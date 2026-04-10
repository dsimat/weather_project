import pytest
import json
import pandas as pd
from pathlib import Path
from analysis import analyze_data_hourly, analyze_data_daily


@pytest.fixture
def filepath():
    """Fixture to provide the file path for the test data."""
    yield Path(__file__).parent


@pytest.fixture
def sample_hourly_metric_data(filepath):
    """Fixture to load the sample hourly metric data from a JSON file and yield it as a DataFrame."""
    hourly_metric_data = json.load(
        open(f"{filepath}/mock_data/tabular_hourly_metric.json")
    )
    yield pd.DataFrame(hourly_metric_data)


@pytest.fixture
def sample_hourly_imperial_data(filepath):
    """Fixture to load the sample hourly imperial data from a JSON file and yield it as a DataFrame."""
    hourly_imperial_data = json.load(
        open(f"{filepath}/mock_data/tabular_hourly_imperial.json")
    )
    yield pd.DataFrame(hourly_imperial_data)


@pytest.fixture
def sample_daily_metric_data(filepath):
    """Fixture to load the sample daily metric data from a JSON file and yield it as a DataFrame."""
    daily_metric_data = json.load(
        open(f"{filepath}/mock_data/tabular_daily_metric.json")
    )
    yield pd.DataFrame(daily_metric_data)


@pytest.fixture
def sample_daily_imperial_data(filepath):
    """Fixture to load the sample daily imperial data from a JSON file and yield it as a DataFrame."""
    daily_imperial_data = json.load(
        open(f"{filepath}/mock_data/tabular_daily_imperial.json")
    )
    yield pd.DataFrame(daily_imperial_data)


@pytest.fixture
def analyzed_hourly_data(sample_hourly_metric_data):
    """Fixture to analyze the sample hourly metric data and yield the results."""
    yield analyze_data_hourly(sample_hourly_metric_data)


@pytest.fixture
def analyzed_daily_data(sample_daily_metric_data):
    """Fixture to analyze the sample daily metric data and yield the results."""
    yield analyze_data_daily(sample_daily_metric_data)


def test_instance_of_dataFrames(analyzed_hourly_data, analyzed_daily_data):
    """Test that the outputs of the analysis functions are DataFrames."""

    for index, df in enumerate(analyzed_hourly_data):
        assert isinstance(df, pd.DataFrame), (
            f"Element at index {index} is not a DataFrame"
        )

    for index, df in enumerate(analyzed_daily_data):
        assert isinstance(df, pd.DataFrame), (
            f"Element at index {index} is not a DataFrame"
        )


def test_non_empty_dataFrames(analyzed_hourly_data, analyzed_daily_data):
    """Test that the DataFrames returned by the analysis functions are not empty."""

    for df in analyzed_hourly_data:
        assert not df.empty

    for df in analyzed_daily_data:
        assert not df.empty
