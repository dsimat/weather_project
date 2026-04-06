# NOTE: RUN THE TESTS USING THE FOLLOWING COMMAND ->
# python -m pytest



# importing the module
import pytest
from data_processing import fetch_hourly_metric_data



from pathlib import Path
import json



#checking if the function returns a JSON
def test_fetch_hourly_metric_data():
    lat = 51.5072
    lng = -0.1275
    result = fetch_hourly_metric_data(lat, lng) 

    #checking if the function returns a JSON
    assert isinstance(result, dict)

    #checking if the JSON has hourly_units as a key
    assert "hourly_units" in result

    #checking if the JSON has hourly as a key
    assert "hourly" in result












BASE_DIR = Path(__file__).resolve().parent

def load_hourly_json():
    with open(BASE_DIR / "mock_data" / "hourly_metric.json") as f:
        return json.load(f)

def load_daily_json():
    with open(BASE_DIR / "mock_data" / "daily_imperial.json") as f:
        return json.load(f)




from data_processing import data_in_table, hourly_data_units

def test_data_in_table():
    data = load_hourly_json()

    df = data_in_table(data)

    assert not df.empty
    assert "temperature_2m" in df.columns
    
    assert "relative_humidity_2m" in df.columns
    assert "precipitation" in df.columns
    assert "cloud_cover" in df.columns
    assert "surface_pressure" in df.columns
    assert "wind_speed_10m" in df.columns
    assert "wind_direction_10m" in df.columns


# from data_processing import hourly_data_units

def test_hourly_data_units():
    data = load_hourly_json()

    units = hourly_data_units(data)

    assert isinstance(units, dict)
    assert "temperature_2m" in units

    assert "relative_humidity_2m" in units
    assert "precipitation" in units
    assert "wind_speed_10m" in units
    assert "cloud_cover" in units
    assert "surface_pressure" in units
    assert "wind_direction_10m" in units





from data_processing import daily_data_table, daily_data_units

def test_daily_data_table():
    data = load_daily_json()

    df = daily_data_table(data)

    assert not df.empty
    assert "temperature_2m_max" in df.columns

    assert "temperature_2m_min" in df.columns
    assert "wind_direction_10m_dominant" in df.columns
    assert "wind_speed_10m_max" in df.columns
    assert "sunshine_duration" in df.columns
    assert "precipitation_sum" in df.columns
    assert "apparent_temperature_mean" in df.columns
    


# from data_processing import daily_data_units

def test_daily_data_units():
    data = load_daily_json()

    units = daily_data_units(data)

    assert isinstance(units, dict)

    assert "temperature_2m_max" in units
    assert "temperature_2m_min" in units
    assert "wind_direction_10m_dominant" in units
    assert "wind_speed_10m_max" in units
    assert "sunshine_duration" in units
    assert "precipitation_sum" in units
    assert "apparent_temperature_mean" in units




