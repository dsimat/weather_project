


import pandas as pd
import requests

from datetime import date, timedelta


pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)



# url = "https://api.open-meteo.com/v1/forecast"

def main():

    # raw_data = fetch_hourly_rawdata(52.52, 13.41)

    # print(default_units(raw_data))

    # print(data_in_table(raw_data))

    daily_raw_data_i = raw_daily_data_imperial(52.52, 13.41)

    # print(daily_raw_data)


    print(daily_data_units(daily_raw_data_i))

    print(daily_data_table(daily_raw_data_i))

    # print("******")
    # print()
    
    # daily_raw_data = fetch_daily_data(52.52, 13.41)
    # # print(daily_raw_data)

    # print(daily_data_units(daily_raw_data))

    # print(daily_data_table(daily_raw_data))



"""
'fetch_hourly_rawdata' takes latitude and longitude of the place
you need to find the weather data on, and fetches the hourly weather data 
for that place in JSON format
It provides hourly data for a total of 8 days which includes the hourly weather 
for the next(future) 3 days.
"""
def fetch_hourly_rawdata(lat, lng):

    url = "https://api.open-meteo.com/v1/forecast"

    today = date.today()

    past_date = today - timedelta(days=4)
    future_date = today + timedelta(days=3)

    params = {
        "latitude": lat,
        "longitude": lng,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "cloud_cover",
            "surface_pressure",
            "wind_direction_10m"
        ],
        "start_date": past_date.isoformat(),
        "end_date": future_date.isoformat(),
        "timezone": "auto"
    }

    response = requests.get(url, params=params)

    # convert response to JSON
    data = response.json()

    return data


"""
This 'data_in_table' function converts the hourly data fetched from the open meteo API, 
which is in JSON format to a Pandas dataframe.
So what it takes as argument is the data one gets from 'fetch_hourly_rawdata(lat, lng)'
and returns a 2-D table.
"""
def data_in_table(raw_data):

    df_raw = pd.DataFrame()
       
    df_raw['time'] = raw_data['hourly']['time']
    df_raw['temperature_2m'] = raw_data['hourly']['temperature_2m']
    df_raw['relative_humidity_2m'] = raw_data['hourly']['relative_humidity_2m']
    df_raw['precipitation'] = raw_data['hourly']['precipitation']

    df_raw['cloud_cover'] = raw_data['hourly']['cloud_cover']

    df_raw['surface_pressure'] = raw_data['hourly']['surface_pressure']

    df_raw['wind_speed_10m'] = raw_data['hourly']['wind_speed_10m']
        
    df_raw['wind_direction_10m'] = raw_data['hourly']['wind_direction_10m']

    #print(df_raw)
    return df_raw


"""
Returns the units that the hourly weather data (raw_data) that is fetched, uses.
"""
def hourly_data_units(raw_data):
    # for paramtr, hrl_unit in raw_data['hourly_units'].items():
        # print(hrl_unit)
    return raw_data['hourly_units']



"""
'fetch_daily_data' takes latitude and longitude of the place
you need to find the weather data on, & optionally the start and end date 
in case you want to specify the timeframe, and fetches the daily weather data 
for that place in JSON format
The default duration is past 30 days.
The default data units use metric system.
"""
def fetch_daily_data(lat, lng, from_date = date.today()-timedelta(days=30), to_date = date.today()-timedelta(days=1)):

    url = "https://archive-api.open-meteo.com/v1/archive"
    
    params = {
    "latitude": lat,
	"longitude": lng,
    "start_date": from_date.isoformat(),
	"end_date": to_date.isoformat(),
	"daily": ["temperature_2m_max", 
           "temperature_2m_min", 
           "wind_direction_10m_dominant", 
           "wind_speed_10m_max", 
           "sunshine_duration", 
           "precipitation_sum", 
           "apparent_temperature_mean"],
    }
    response = requests.get(url, params=params)
    #response.raise_for_status()


    # convert response to JSON
    daily_data = response.json()

    return daily_data



"""
This 'daily_data_table' function converts the daily data fetched from the open meteo API, 
which is in JSON format to a Pandas dataframe.
So what it takes as argument is the data one gets from 'fetch_daily_data(lat, lng,....)'
and returns a 2-D table.
"""
def daily_data_table(daily_data):

    df_daily = pd.DataFrame()

    df_daily['time'] = daily_data['daily']['time']
    df_daily['temperature_2m_min'] = daily_data['daily']['temperature_2m_min']
    df_daily['temperature_2m_max'] = daily_data['daily']['temperature_2m_max']
    df_daily['apparent_temperature_mean'] = daily_data['daily']['apparent_temperature_mean']
    df_daily['precipitation_sum'] = daily_data['daily']['precipitation_sum']
    df_daily['sunshine_duration'] = daily_data['daily']['sunshine_duration']
    df_daily['wind_speed_10m_max'] = daily_data['daily']['wind_speed_10m_max']
    df_daily['wind_direction_10m_dominant'] = daily_data['daily']['wind_direction_10m_dominant']

    return df_daily


"""
Returns the units that the daily weather data (daily_data) that is fetched uses.
"""
def daily_data_units(daily_data):

    return daily_data['daily_units']


"""
'raw_daily_data_imperial' takes latitude and longitude of the place
you need to find the weather data on, & optionally the start and end date 
in case you want to specify the timeframe, and fetches the daily weather data 
for that place in JSON format
The default duration is past 30 days.
The default data units use imperial system.
"""
def raw_daily_data_imperial(lat, lng, from_date = date.today()-timedelta(days=30), to_date = date.today()-timedelta(days=1)):

    url = "https://archive-api.open-meteo.com/v1/archive"
 
    params = {
    "latitude": lat,
	"longitude": lng,
    "start_date": from_date.isoformat(),
	"end_date": to_date.isoformat(),
	"daily": ["temperature_2m_max", 
           "temperature_2m_min", 
           "wind_direction_10m_dominant", 
           "wind_speed_10m_max", 
           "sunshine_duration", 
           "precipitation_sum", 
           "apparent_temperature_mean"],
    "temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch",

    }
    response = requests.get(url, params=params)
    response.raise_for_status()


    # convert response to JSON
    daily_data = response.json()

    return daily_data




if __name__ == "__main__":
    main()


