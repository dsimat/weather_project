import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

CURRENT_TIME = datetime.now()

class City:
    """
    Docstring for City
    
    :name: Name of the city
    :country: Country name
    :coords: (lat, lng)
    """
    def __init__(self, name, country):
        self.name = name
        self.country = country
        self.coords = ()

        self.coords = self.get_coords_csv()
    
    def __str__(self):
        return(f"{self.name}'s coordinates = {self.coords}")
    
    def get_coords_csv(self)-> tuple:
        """
        Docstring for get_coords_csv
        
        :param self: class 
        :return: a tuple of lattitude and longitude
        :rtype: tuple
        """
        res = ()
        dfc = pd.read_csv('worldcities.csv')
        dfc['city_ascii'] = dfc['city_ascii'].str.lower()
        dfc['country'] = dfc['country'].str.lower()

        search_city = self.name.lower().strip()
        serch_cntry = self.country.lower().strip()

        # exact match for city and country
        # because same city is in multiple countries like 'Kota' in Japan and India
        match = dfc[
            (dfc['city_ascii'] == search_city) & 
            (dfc['country'] == serch_cntry)
            ]
        
        # pick first value from csv if same city and country are multiple times
        # like 'Jaipur' in 'India' is multiple times
        if not match.empty:
            lat = match['lat'].iloc[0]
            lng = match['lng'].iloc[0]
            return (lat, lng)
        else:
            print(f"City '{self.name}' not found in database")
            return res

def get_user_city_coords()->tuple:
    """
    Asks for:
        1. City name
        2. Country name
    Checks if:
    1. Enter input is string or not including spaces
        a. if not returns message and asks again
        b. if yes, checks if the city name is in Data or not
    2. Returns latitude and longitude as tuple
    """
    user_city = input("Enter a city name: ")
    city_chars = user_city.strip()
    if not all(char.isalpha() or char.isspace() for char in city_chars):
        print("Enter only characters")
        user_city = input("Enter a city name: ")
    
    user_country = input("Enter country name: ")
    cntry_chars = user_country.strip()
    if not all(char.isalpha() or char.isspace() for char in cntry_chars):
        print("Enter only characters")
        user_country = input("Enter country name: ")
    
    city_coords = City(user_city, user_country).coords
    return city_coords

def get_configured_durations()-> None:
    """
    Returns the configured durations
    """
    durations = {
        '1': '5hr',
        '2': '24hr',
        '3': 'pst_4d',
        '4': 'nxt_3d',
        '5': '1m',
        '6': '2m',
        '7': '3m'
    }
    return durations

def get_value_titles(key)-> str:
    """
    Docstring for get_value_titles
    
    :param key: Dataframe label
    :return: Label on basis of the key
    :rtype: str
    """
    values = {
        'temperature_2m': 'Temperature',
        'relative_humidity_2m': 'Relative humidity (2 meters)',
        'precipitation': 'Precipitation',
        'wind_speed_10m': 'Wind speed (10 meters/second)',
        'cloud_cover': 'Cloud cover',
        'surface_pressure': 'Surface Pressure',
        'wind_direction_10m': 'Wind direction (10 meters)'
    }
    return values[key]

def get_user_duration()-> str:
    """
    Asks user to enter duration
    """
    options = get_configured_durations()
    print()
    print("-"*10)
    print("Select durations:")
    print("1: Last 5 hours || 2: Today || 3: Past 3 days || 4: Next 3 days")
    print("Or")
    print("5: Past 1 month || 6: Past 2 month || 7: Past 3 month")
    user_duration = input("Enter 1/2/3/4/5/6/7:")
    if not user_duration.isdigit() or user_duration == "" or (user_duration.isdigit() and len(user_duration)>1):
        print("Enter only single digits")
        get_user_duration()
    
    if not user_duration in ['1', '2', '3','4', '5', '6', '7']:
        print("Not a valid option")
        get_user_duration()
    return options[user_duration]

def plot_graph(df: pd.DataFrame, x_col, y_col, plt_title, gf_color, ax = None)-> None:
    df.plot(
        x = x_col,
        y = y_col,
        kind = 'line',
        linewidth = 2.0,
        title = plt_title,
        marker = "o",
        color = gf_color,
        ax = ax,
        label=y_col,
    )

def get_plot_title_hourly(anlyzd, duration: str)->tuple:
    if duration == '5hr':
        data_to_plot = anlyzd[1]
        plot_title = 'Weather over 5 hours'
    
    elif duration == '24hr':
        data_to_plot = anlyzd[2]
        plot_title = 'Weather whole day'

    elif duration == 'pst_4d':
        data_to_plot = anlyzd[3]
        plot_title = 'Weather over past 4 days'

    elif duration == 'nxt_3d':
        data_to_plot = anlyzd[4]
        plot_title = 'Weather forcast for next 3 days'
    return (data_to_plot, plot_title)

def visuals_plotter_hourly(anlyzd: tuple, duration: str = '24hr') -> None:
    # Figure with 4 subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (12, 8))

    data_to_plot, plot_title = get_plot_title_hourly(anlyzd, duration)
    print(data_to_plot)

    # Panel 1: Temperature and humidity
    data_to_plot.plot('time', 'temperature_2m', ax = ax1, color = 'blue')
    ax1b = ax1.twinx()
    data_to_plot.plot('time', 'relative_humidity_2m', ax = ax1b, color = 'red')
    ax1.set_ylabel('Temp')
    ax1b.set_ylabel('Humidity')
    ax1.legend(loc='upper left')
    ax1b.legend(loc='upper right')
    ax1.set_title('Temperature & humidity')

    # Panel 2: Precipitation
    # type: line steps
    data_to_plot.plot(
        x='time',
        y='precipitation',
        ax=ax2,
        color='green',
        kind='line',
        drawstyle='steps-post'
    )
    ax2.set_ylabel('Precipitation')
    ax2.set_title('Precipitation')
    
    # Panel 3: Cloud cover
    # type: line steps
    data_to_plot.plot(x='time', y='cloud_cover', ax=ax3, color='black', kind='line', drawstyle="steps-post")
    ax3.set_ylabel('Cloud')
    ax3.set_title('Cloud')

    # Panel 4: Wind direction and Wind speed
    # type: Rose
    angles = np.deg2rad(data_to_plot['wind_direction_10m'])
    speeds = data_to_plot['wind_speed_10m']

    ax4 = fig.add_subplot(2,2,4, projection= 'polar')
    ax4.bar(angles, speeds, width=0.2, color='blue', alpha=0.7)

    ax4.set_theta_zero_location('N')
    ax4.set_theta_direction(-1)
    ax4.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
    ax4.set_title('Wind speed & direction')

    fig.suptitle(plot_title)

    plt.grid(True)
    plt.tight_layout()
    plt.show()


def visuals_plotter_daily(anlyzd: pd.DataFrame, duration: str = '1m')-> None:
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

    plot_title = "Daily Weather data"
    plt_all_df = anlyzd[0]

    if duration == "1m":
        data_to_plot = plt_all_df.iloc[50:89]
        plot_title += " over last 1 month"
    elif duration == "2m":
        data_to_plot = plt_all_df.iloc[30:89]
        plot_title += " over last 2 months"
    elif duration == "3m":
        data_to_plot = plt_all_df.iloc[0:89]
        plot_title += " over last 3 months"

    # Panel 1: Temperature min and max
    ax1.plot(data_to_plot['time'], data_to_plot['temperature_2m_max'], color="#8E18B9", label='Max Temp')
    ax1.plot(data_to_plot['time'], data_to_plot['temperature_2m_min'], color="#16519F", label='Min Temp')
    ax1.plot(data_to_plot['time'], data_to_plot['apparent_temperature_mean'], color = "#09BAB1", label = 'Mean Temp')
    
    # fill between max and min temperatures
    ax1.fill_between(
        data_to_plot['time'],
        data_to_plot['temperature_2m_min'],
        data_to_plot['temperature_2m_max'],
        color = "#C67BD9",
        alpha = 0.3,
        label = 'Temp range'
    )
    ax1.legend(loc = 'upper left', frameon = True)
    # ax1.set_xlabel('Days')
    ax1.set_ylabel('Temperature')
    ax1.set_title('Temperature for past month')

    #Panel 2: precipitation_sum
    # type: bar
    ax2.bar(
        data_to_plot['time'],
        data_to_plot['precipitation_sum'],
        color = "#E18915"
    )
    # ax2.set_xlabel('Days')
    ax2.set_ylabel('Precipitation sum')
    ax2.set_title('Precipitation sum')

    #Panel 3: sunshine_duration
    # type: bar
    ax3.plot(
        data_to_plot['time'],
        data_to_plot['sunshine_duration'],
        color = "#DBDB07"
    )
    # ax3.set_xlabel('Days')
    ax3.set_ylabel('Sunshine duration')
    ax3.set_title('Sunshine duration')

    #Panel 4:  wind_speed_10m_max,  wind_direction_10m_dominant
    # type: rose
    angles = data_to_plot['wind_direction_10m_dominant']
    speed = data_to_plot['wind_speed_10m_max']
    ax4 = fig.add_subplot(2, 2, 4, projection = 'polar')

    ax4.bar(angles, speed, width = 0.2, color = "#B90F12", alpha = 0.7)

    ax4.set_theta_zero_location('N')
    ax4.set_theta_direction(-1) # Clockwise

    ticks_deg = [0, 45, 90, 135, 180, 225, 270, 315]
    ticks_rad = np.deg2rad(ticks_deg) # Show full circle
    labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ax4.set_xticks(ticks_rad)
    ax4.set_xticklabels(labels)
    ax4.set_title('Wind speed & direction')

    fig.suptitle(plot_title)

    # to avoid overlap x-axis labels
    for ax in [ax1, ax2, ax3]:
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def visualize_weather(coords: tuple, duration: str):
    """
    Docstring for visualize_weather
    
    :param coords: A tuple of latitude and longitude
    :type coords: tuple
    :param duration: User duration code defined in get_configured_durations()
    :type duration: str
    """
    # conf_dura = get_configured_durations()
    if duration in ('5hr','24hr','pst_4d','nxt_3d'):
        # print("Hourly data")

        raw_data = fetch_hourly_metric_data(coords[0], coords[1])
        df_hourly = data_in_table(raw_data)
        hr_anls_df = analyze_data_hourly(df_hourly)

        visuals_plotter_hourly(hr_anls_df, duration)
        # some not used functions:
        # 1:    visuals_plotter_single(hr_anls_df, "24hr", "temperature_2m")
        # 2:    visuals_plotter_all(hr_anls_df, "24hr")
    else:
        max_past = 90
        start = date.today()-timedelta(days= max_past)
        end = date.today()-timedelta(days=1)

        raw_data = fetch_daily_data(coords[0], coords[1], from_date = start, to_date = end)
        df_daily = daily_data_table(raw_data)
        daily_anlyzd = analyze_data_daily(df_daily, max_past)

        visuals_plotter_daily(daily_anlyzd, duration)

def get_user_input()-> tuple:
    """
    Docstring for get_user_input
    
    :return: A tuple of city coordinate (tuple) and user duration
    :rtype: tuple
    """
    city_coords = ()
    while city_coords == ():
        city_coords = get_user_city_coords()
    lat= city_coords[0]
    lng= city_coords[1]
    
    user_duration = ''
    while user_duration == '':
        user_duration = get_user_duration()

    return (city_coords, user_duration)


#-------------------Adiitional functions--------
def visuals_plotter_single(anlyzd: tuple, duration: str, label: str) -> None:
    """
    function to plot using anlyzed data
    
    :param adf: Description
    :type adf: pd.DataFrame
    """
    label_val = get_value_titles(label)
    if duration == '5hr':#--------
        data_to_plot = anlyzd[1]
        plot_title = f'{label_val} over 5 hours'
    
    elif duration == '24hr':
        data_to_plot = anlyzd[2]
        plot_title = f'{label_val} whole day'

    elif duration == 'pst_4d':
        data_to_plot = anlyzd[3]
        plot_title = f'{label_val} over past 4 days'

    elif duration == 'nxt_3d':
        data_to_plot = anlyzd[4]
        plot_title = f'{label_val} forcast for next 3 days'
    
    # print(data_to_plot)

    data_to_plot.plot(
        x='time',
        y = label,
        kind = 'line',
        linewidth = 2.0,
        title = plot_title,
        marker = "o",
        color = '#09637E'
    )
    plt.xlabel('Time', color = '#09637E')
    plt.ylabel(label_val, color = '#09637E')
    plt.grid(True)
    plt.show()

def visuals_plotter_all(anlyzd: tuple, duration: str) -> None:
    """
    function to plot using anlyzed data
    
    :param anlyzd: Analyzed data
    :type duration: doration to visualize
    example: visuals_plotter_all(hr_anls_df, "24hr")
    """
    
    if duration == '5hr':#--------
        data_to_plot = anlyzd[1]
        plot_title = 'Temperature over 5 hours'
    
    elif duration == '24hr':
        data_to_plot = anlyzd[2]
        plot_title = 'Temperature whole day'

    elif duration == 'pst_4d':
        data_to_plot = anlyzd[3]
        plot_title = 'Temperature over past 4 days'

    elif duration == 'nxt_3d':
        data_to_plot = anlyzd[4]
        plot_title = 'Temperature forcast for next 3 days'

    print(data_to_plot)

    fig, ax = plt.subplots(figsize=(10, 6))

    plot_graph(data_to_plot, 'time', 'temperature_2m', plot_title, "#0ad2ff", ax)
    plot_graph(data_to_plot, 'time', 'relative_humidity_2m', plot_title,"#2962ff", ax)
    plot_graph(data_to_plot, 'time', 'precipitation', plot_title, "#9500ff", ax)
    plot_graph(data_to_plot, 'time', 'cloud_cover', plot_title, "#ff0059", ax)
    plot_graph(data_to_plot, 'time', 'surface_pressure', plot_title, "#ff8c00", ax)
    plot_graph(data_to_plot, 'time', 'wind_speed_10m', plot_title, "#b4e600", ax)
    plot_graph(data_to_plot, 'time', 'wind_direction_10m', plot_title, "#0fffdb", ax)

    plt.xlabel('Time', color = '#09637E')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    from data_processing import (
        fetch_hourly_metric_data,
        data_in_table,
        fetch_daily_data,
        daily_data_table
    )
    from analysis import (
        analyze_data_daily,
        analyze_data_hourly
    )

    # get input
    city_coords, user_duration= get_user_input()

    #Visualize
    visualize_weather(city_coords, user_duration)