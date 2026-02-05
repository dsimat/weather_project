import pandas as pd
from datetime import timedelta


def analyze_data(df: pd.DataFrame) -> tuple:
    """Analyze the weather data and calculate min, max and average values for different time intervals.

    Args:
        df (pd.DataFrame): DataFrame containing weather data with a 'time' column.

    Returns:
        tuple: A tuple containing DataFrames for 5 hour, 7 day, and 30 day intervals,
               as well as DataFrames with min, max, and average statistics for each interval.
    """

    # Convert timestamp strings to datetime objects
    df["time"] = pd.to_datetime(df["time"], utc=True)

    hours_5 = timedelta(hours=5)
    days_7 = timedelta(days=7)
    days_30 = timedelta(days=30)

    # From the last timestamp, go back 5 hours, 7 days and 30 days
    df_5h = df[df["time"] >= (df.iloc[-1].loc["time"] - hours_5).isoformat()]
    df_7d = df[df["time"] >= (df.iloc[-1].loc["time"] - days_7).isoformat()]
    df_30d = df[df["time"] >= (df.iloc[-1].loc["time"] - days_30).isoformat()]

    # Calculate min, max and average values for the entire DataFrame
    min_data = df.drop("time", axis=1).min()
    max_data = df.drop("time", axis=1).max()
    avg_data = df.drop("time", axis=1).mean()

    # Calculate min, max and average values for the 5 hour DataFrame
    min_data_5h = df_5h.drop("time", axis=1).min()
    max_data_5h = df_5h.drop("time", axis=1).max()
    avg_data_5h = df_5h.drop("time", axis=1).mean()

    # Calculate min, max and average values for the 7 day DataFrame
    min_data_7d = df_7d.drop("time", axis=1).min()
    max_data_7d = df_7d.drop("time", axis=1).max()
    avg_data_7d = df_7d.drop("time", axis=1).mean()

    # Calculate min, max and average values for the 30 day DataFrame
    min_data_30d = df_30d.drop("time", axis=1).min()
    max_data_30d = df_30d.drop("time", axis=1).max()
    avg_data_30d = df_30d.drop("time", axis=1).mean()

    # Combine the series into a DataFrame (first combine into columns and then transpose)
    df_stats = pd.concat([min_data, max_data, avg_data], axis=1).T
    df_stats_5h = pd.concat([min_data_5h, max_data_5h, avg_data_5h], axis=1).T
    df_stats_7d = pd.concat([min_data_7d, max_data_7d, avg_data_7d], axis=1).T
    df_stats_30d = pd.concat([min_data_30d, max_data_30d, avg_data_30d], axis=1).T

    # Rename the row labels
    df_stats.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)
    df_stats_5h.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)
    df_stats_7d.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)
    df_stats_30d.rename(index={0: "min", 1: "max", 2: "avg"}, inplace=True)

    return df_5h, df_7d, df_30d, df_stats, df_stats_5h, df_stats_7d, df_stats_30d


if __name__ == "__main__":
    from data_processing import hourly_imperial_data, data_in_table

    raw_data = hourly_imperial_data(52.52, 13.41)
    df = data_in_table(raw_data)
    print(analyze_data(df)[0])  # Print 5 hour DataFrame for testing
