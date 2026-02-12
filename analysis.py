import pandas as pd
from datetime import timedelta, date


def analyze_data_hourly(
    df: pd.DataFrame,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """Analyze the hourly weather data and calculate min, max and average values for different time intervals.
    The hourly data include today's data, archived data up to 4 days and forecast data up to 3 days.

    Args:
        df (pd.DataFrame): DataFrame containing weather data with a 'time' column.

    Returns:
        tuple: A tuple containing DataFrames for 5 hour, 1 day and the archived 4 day intervals,
               as well as DataFrames with min, max, and average statistics for each interval and the forecast data.
    """

    # Convert timestamp strings to datetime objects
    df["time"] = pd.to_datetime(df["time"], utc=True)

    today = date.today()
    hours_5 = timedelta(hours=5)
    days_1 = timedelta(days=1)

    # Split historical and forecast data
    # .dt.date is used to compare only the date part of the timestamp, ignoring the time part

    # Future data (forecast) - 3 days ahead
    df_forecast = df[df["time"].dt.date > today]

    # Past data (archived) - 4 days past
    df_archive = df[df["time"].dt.date <= today]

    # From today, go back 5 hours and 1 day
    # This assumes that the DataFrame is sorted by time in ascending order
    df_5h = df_archive[
        df_archive["time"] >= (df_archive.iloc[-1].loc["time"] - hours_5).isoformat()
    ]
    df_1d = df_archive[
        df_archive["time"] >= (df_archive.iloc[-1].loc["time"] - days_1).isoformat()
    ]

    # Calculate min, max and average values for the entire DataFrame
    min_data = df.drop("time", axis=1).min()
    max_data = df.drop("time", axis=1).max()
    avg_data = df.drop("time", axis=1).mean()

    # Calculate min, max and average values for the 5 hour DataFrame
    min_data_5h = df_5h.drop("time", axis=1).min()
    max_data_5h = df_5h.drop("time", axis=1).max()
    avg_data_5h = df_5h.drop("time", axis=1).mean()

    # Calculate min, max and average values for the 1 day DataFrame
    min_data_1d = df_1d.drop("time", axis=1).min()
    max_data_1d = df_1d.drop("time", axis=1).max()
    avg_data_1d = df_1d.drop("time", axis=1).mean()

    # Calculate min, max and average values for the archived 4 day DataFrame
    min_data_archive = df_archive.drop("time", axis=1).min()
    max_data_archive = df_archive.drop("time", axis=1).max()
    avg_data_archive = df_archive.drop("time", axis=1).mean()

    # Calculate min, max and average values for the forecast 3 day DataFrame
    min_data_forecast = df_forecast.drop("time", axis=1).min()
    max_data_forecast = df_forecast.drop("time", axis=1).max()
    avg_data_forecast = df_forecast.drop("time", axis=1).mean()

    # Combine the series into a DataFrame (first combine into columns and then transpose)
    df_stats = pd.concat([min_data, max_data, avg_data], axis=1).T
    df_stats_5h = pd.concat([min_data_5h, max_data_5h, avg_data_5h], axis=1).T
    df_stats_1d = pd.concat([min_data_1d, max_data_1d, avg_data_1d], axis=1).T
    df_stats_archive = pd.concat(
        [min_data_archive, max_data_archive, avg_data_archive], axis=1
    ).T
    df_stats_forecast = pd.concat(
        [min_data_forecast, max_data_forecast, avg_data_forecast], axis=1
    ).T

    # Rename the row labels
    df_stats.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)
    df_stats_5h.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)
    df_stats_1d.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)
    df_stats_archive.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)
    df_stats_forecast.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)

    return (
        df_5h,
        df_1d,
        df_archive,
        df_forecast,
        df_stats,
        df_stats_5h,
        df_stats_1d,
        df_stats_archive,
        df_stats_forecast,
    )


def analyze_data_daily(
    df: pd.DataFrame, time_limit: int = 30
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Analyze the daily weather data and calculate min, max and average values for different time intervals.
    The daily data include archived data from yesterday up to a custom time limit set by the user.
    The default time limit is 30 days in the past and the maximum time limit is 90 days in the past.

    Args:
        df (pd.DataFrame): DataFrame containing weather data with a 'time' column.

    Returns:
        tuple: A tuple containing DataFrames for 7 day, 30 day, and 90 day intervals,
               as well as DataFrames with min, max, and average statistics for each interval.
    """

    # Convert timestamp strings to datetime objects
    df["time"] = pd.to_datetime(df["time"], utc=True)

    if time_limit < 1 or time_limit > 90:
        raise ValueError("Time limit must be between 1 and 90 days.")

    days_limit = timedelta(days=time_limit)

    # From the last timestamp, go back  a custom time limit set by the user (default is 30 days)
    # This assumes that the DataFrame is sorted by time in ascending order
    df_custom = df[df["time"] >= (df.iloc[-1].loc["time"] - days_limit).isoformat()]

    # Calculate min, max and average values for the entire DataFrame
    min_data = df.drop("time", axis=1).min()
    max_data = df.drop("time", axis=1).max()
    avg_data = df.drop("time", axis=1).mean()

    # Calculate min, max and average values for the custom time limit DataFrame
    min_data_custom = df_custom.drop("time", axis=1).min()
    max_data_custom = df_custom.drop("time", axis=1).max()
    avg_data_custom = df_custom.drop("time", axis=1).mean()

    # Combine the series into a DataFrame (first combine into columns and then transpose)
    df_stats = pd.concat([min_data, max_data, avg_data], axis=1).T
    df_stats_custom = pd.concat(
        [min_data_custom, max_data_custom, avg_data_custom], axis=1
    ).T

    # Rename the row labels
    df_stats.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)
    df_stats_custom.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)

    return df_custom, df_stats, df_stats_custom


if __name__ == "__main__":
    from data_processing import (
        fetch_hourly_metric_data,
        hourly_imperial_data,
        data_in_table,
        hourly_data_units,
        fetch_daily_data,
        raw_daily_data_imperial,
        daily_data_table,
        daily_data_units,
    )

    raw_data = fetch_hourly_metric_data(52.52, 13.41)
    df_hourly = data_in_table(raw_data)
    print(analyze_data_hourly(df_hourly)[0])  # Print 5 hour DataFrame for testing

    # raw_data = fetch_daily_data(52.52, 13.41)
    # df_daily = daily_data_table(raw_data)
    # print(analyze_data_daily(df_daily, 2)[0])  # Print custom time limit DataFrame for testing
