import pytest
import json
import pandas as pd
from pathlib import Path
from analysis import analyze_data_hourly, analyze_data_daily


@pytest.fixture
def filepath():
    """Fixture to provide the file path for the test data."""
    return Path(__file__).parent


@pytest.fixture
def mock_hourly_metric_data(filepath: Path):
    """Fixture to load the mock hourly metric data from a JSON file and return it as a DataFrame."""
    hourly_metric_data = json.load(
        open(f"{filepath}/mock_data/tabular_hourly_metric.json")
    )
    return pd.DataFrame(hourly_metric_data)


@pytest.fixture
def mock_hourly_imperial_data(filepath: Path):
    """Fixture to load the mock hourly imperial data from a JSON file and return it as a DataFrame."""
    hourly_imperial_data = json.load(
        open(f"{filepath}/mock_data/tabular_hourly_imperial.json")
    )
    return pd.DataFrame(hourly_imperial_data)


@pytest.fixture
def mock_daily_metric_data(filepath: Path):
    """Fixture to load the mock daily metric data from a JSON file and return it as a DataFrame."""
    daily_metric_data = json.load(
        open(f"{filepath}/mock_data/tabular_daily_metric.json")
    )
    return pd.DataFrame(daily_metric_data)


@pytest.fixture
def mock_daily_imperial_data(filepath: Path):
    """Fixture to load the mock daily imperial data from a JSON file and return it as a DataFrame."""
    daily_imperial_data = json.load(
        open(f"{filepath}/mock_data/tabular_daily_imperial.json")
    )
    return pd.DataFrame(daily_imperial_data)


@pytest.fixture
def analyzed_hourly_data(mock_hourly_metric_data):
    """Fixture to analyze the mock hourly metric data and return the results."""
    return analyze_data_hourly(mock_hourly_metric_data)


@pytest.fixture
def analyzed_daily_data(mock_daily_metric_data):
    """Fixture to analyze the mock daily metric data and return the results."""
    return analyze_data_daily(mock_daily_metric_data)


# Test without parametrization
def test_instance_of_dataFrames_1(
    analyzed_hourly_data: tuple[pd.DataFrame, ...],
    analyzed_daily_data: tuple[pd.DataFrame, ...],
) -> None:
    """Test that the outputs of the analysis functions are DataFrames."""

    for index, df in enumerate(analyzed_hourly_data):
        assert isinstance(df, pd.DataFrame), (
            f"Element at index {index} is not a DataFrame"
        )

    for index, df in enumerate(analyzed_daily_data):
        assert isinstance(df, pd.DataFrame), (
            f"Element at index {index} is not a DataFrame"
        )


# Test with parametrization to avoid code duplication
# Note: This test will not work.
# You can pass fixture functions as arguments in test functions but not in parametrization functions!
@pytest.mark.parametrize(
    "analyzed_data",
    [analyzed_hourly_data, analyzed_daily_data],
)
def test_instance_of_dataFrames_2(analyzed_data: tuple[pd.DataFrame, ...]) -> None:
    """Test that the outputs of the analysis functions are DataFrames."""

    for index, df in enumerate(analyzed_data):
        assert isinstance(df, pd.DataFrame), (
            f"Element at index {index} is not a DataFrame"
        )


# Test with parametrization to avoid code duplication
# Note: This test will work because we are using the fixture names as strings
# and retrieving the fixture value inside the test function.
@pytest.mark.parametrize(
    "fixture_name",
    ["analyzed_hourly_data", "analyzed_daily_data"],
)
def test_instance_of_dataFrames_3(
    fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Test that the outputs of the analysis functions are DataFrames."""

    # Get the analyzed data from the fixture
    analyzed_data = request.getfixturevalue(fixture_name)

    for index, df in enumerate(analyzed_data):
        assert isinstance(df, pd.DataFrame), (
            f"Element at index {index} is not a DataFrame"
        )


# Test with parametrization to avoid code duplication
# Note: This uses indirect parametrization
# The analyzed_data fixture will be called with the values from the parametrize decorator
# It will retrieve the corresponding fixture value based on the parameter value and pass it to the test function.
@pytest.fixture
def analyzed_data(request) -> tuple[pd.DataFrame, ...]:
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    "analyzed_data",
    ["analyzed_hourly_data", "analyzed_daily_data"],
    indirect=True,
    ids=["hourly", "daily"],
)
def test_instance_of_dataFrames_4(analyzed_data: tuple[pd.DataFrame, ...]) -> None:
    """Test that the outputs of the analysis functions are DataFrames."""

    for index, df in enumerate(analyzed_data):
        assert isinstance(df, pd.DataFrame), (
            f"Element at index {index} is not a DataFrame"
        )


def test_non_empty_dataFrames(
    analyzed_hourly_data: tuple[pd.DataFrame, ...],
    analyzed_daily_data: tuple[pd.DataFrame, ...],
) -> None:
    """Test that the DataFrames returned by the analysis functions are not empty."""

    for df in analyzed_hourly_data:
        assert not df.empty

    for df in analyzed_daily_data:
        assert not df.empty
