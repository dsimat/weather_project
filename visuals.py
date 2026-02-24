import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime
import numpy as np


import matplotlib.cm as cm
import matplotlib.colors as colors


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)

# Font sizes
FT_FS = 14 # Figure title font size
SP_FS = 12 # Sub plot title font size
LGND_FS = 9 # Legend font size

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
        dfc = pd.read_csv("worldcities.csv")
        dfc["city_ascii"] = dfc["city_ascii"].str.lower()
        dfc["country"] = dfc["country"].str.lower()

        search_city = self.name.lower().strip()
        serch_cntry = self.country.lower().strip()

        # exact match for city and country
        # because same city is in multiple countries like "Kota" in Japan and India
        match = dfc[
            (dfc["city_ascii"] == search_city) & 
            (dfc["country"] == serch_cntry)
            ]
        
        # pick first value from csv if same city and country are multiple times
        # like "Jaipur" in "India" is multiple times
        if not match.empty:
            lat = match["lat"].iloc[0]
            lng = match["lng"].iloc[0]
            return (lat, lng)
        else:
            print(f"City '{self.name}' not found in database")
            return res


#-------- Functions for configured values : Start--------

def get_configured_durations()-> dict:
    """
    Returns the configured durations
    """
    durations = {
        "1": "5hr",
        "2": "24hr",
        "3": "pst_4d",
        "4": "nxt_3d",
        "5": "1m",
        "6": "2m",
        "7": "3m"
    }
    return durations

def get_configured_units()-> dict:
    """
    Returns the configured units
    """
    units = {
        "1": "Metric",
        "2": "Imperial"
    }
    return units 

def get_label_value(key: str)-> str:
    """
    Docstring for get_label_value
    
    :param key: Dataframe label (str)
    :return: Label on basis of the key
    :rtype: str
    """
    values = {
        "temperature_2m": "Temperature",
        "relative_humidity_2m": "Relative humidity (2 meters)",
        "precipitation": "Precipitation",
        "wind_speed_10m": "Wind speed (10 meters/second)",
        "cloud_cover": "Cloud cover",
        "surface_pressure": "Surface Pressure",
        "wind_direction_10m": "Wind direction (10 meters)",
        "temperature_2m_min": "Minimum temperature (2 meters)",
        "temperature_2m_max": "Maximum temperature (2 meters)",
        "apparent_temperature_mean": "Mean apparent temperature",
        "precipitation_sum": "Precipitation sum",
        "sunshine_duration": "Sunshine duration",
        "wind_speed_10m_max": "Highest wind speed (10 meters/second)",
        "wind_direction_10m_dominant": "Dominant wind direction (10 meters)"
    }
    return values[key]

#-------- Functions for configured values : End --------

#-------- Functions for user input : Start --------
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

def get_user_duration()-> str:
    """
    Gets duration from user
    """
    options = get_configured_durations()
    print()
    print("-"*10)
    print("Select durations:")
    print("1: Last 5 hours || 2: Today || 3: Past 4 days || 4: Next 3 days")
    print("Or")
    print("5: Past 1 month || 6: Past 2 month || 7: Past 3 month")
    user_duration = input("Enter 1/2/3/4/5/6/7:")
    if not user_duration.isdigit() or user_duration == "" or (user_duration.isdigit() and len(user_duration)>1):
        print("Enter only single digits")
        get_user_duration()
    
    if not user_duration in options:
        print("Not a valid option")
        get_user_duration()
    return options[user_duration]

def get_user_unit()->str:
    """
    Gets unit from user
    """
    options = get_configured_units()
    print()
    print("-"*10)
    print("Select unit:")
    print("1: Metric (SI) || 2: Imperial")
    user_unit = input("Enter 1/2:")
    if not user_unit.isdigit() or user_unit == "" or (user_unit.isdigit() and len(user_unit)>1):
        print("Enter only single digits")
        get_user_unit()
    
    if not user_unit in options:
        print("Not a valid option")
        get_user_unit()
    return options[user_unit]

#-------- Functions for user input : End --------

#-------- Functions for getting data and plotting : Start --------
def get_plot_title_hourly(anlyzd:tuple, duration: str)->tuple:
    """
    returns a tuple of:
    1. hourly data as per the selected duration to plot
    2. plot title
    3. dataframe state: min, max, mean for the duration
    """
    if duration == "5hr":
        data_to_plot = anlyzd[1]
        min_max_mean = anlyzd[6]
        plot_title = "Weather over 5 hours"
    
    elif duration == "24hr":
        data_to_plot = anlyzd[2]
        min_max_mean = anlyzd[7]
        plot_title = "Weather whole day"

    elif duration == "pst_4d":
        data_to_plot = anlyzd[3]
        min_max_mean = anlyzd[8]
        plot_title = "Weather over past 4 days"

    elif duration == "nxt_3d":
        data_to_plot = anlyzd[4]
        min_max_mean = anlyzd[9]
        plot_title = "Weather forcast for next 3 days"
    return (data_to_plot, plot_title, min_max_mean)

def visuals_plotter_hourly(anlyzd: tuple, duration: str="24hr", unit_sys: str="Metric") -> None:
    """
    Creats plot for hourly data
    1. Panel 1: Temperature and humidity
    2. Panel 2: Precipitation and Cloud cover
    3. Panel 3: Surface pressure
    4. Panel 4. Wind speed and Wind direction
    """
    # Figure with 4 subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (12, 8))

    data_to_plot, plot_title, min_max_mean = get_plot_title_hourly(anlyzd, duration)
    plot_title += f"({unit_sys})"

    # Panel 1: Temperature and humidity ----------------

    # 1.1 Get title value for the dataframe parameter
    temp_label = get_label_value("temperature_2m")
    temp_postfix = " (\u00b0F)" if unit_sys == "Imperial" else " (\u2103)"
    temp_label += temp_postfix
    humidity_lable = get_label_value("relative_humidity_2m")

    # 1.2 Plot Temperature
    data_to_plot.plot("time", "temperature_2m", ax = ax1, color = "blue", label = "Temperature")
    # 1.3 Create a new twin axes sharing the same x axis
    ax1b = ax1.twinx()
    # 1.4 Plot Relative humidity on new axes
    data_to_plot.plot("time", "relative_humidity_2m", ax = ax1b, color = "red", label = "Relative humidity")
    # 1.5 Add labels
    ax1.set_xlabel("Time")
    ax1.set_ylabel(temp_label)
    ax1b.set_ylabel(humidity_lable)
    # 1.6 Customize legends
    ax1.legend(loc="upper left", frameon = True, fontsize = LGND_FS)
    ax1b.legend(loc="upper right", frameon = True, fontsize = LGND_FS)
    # 1.7 Add title for the sub plot
    ax1.set_title("Temperature & humidity", fontsize = SP_FS)

    # Panel 2: Precipitation and Cloud cover ----------------
    # type: line steps

    # 2.1 Get title value
    precip_label = get_label_value("precipitation")
    cloud_label = get_label_value("cloud_cover")

    # 2.2 Plot Precipitation
    data_to_plot.plot(
        x="time",
        y="precipitation",
        ax=ax2,
        color="red",
        kind="line",
        drawstyle="steps-post",
        label = "Precipitation",
        linewidth = 2.0
    )
    # 2.3 Create a new twin axes sharing the same x axis
    ax2b = ax2.twinx()
    # 2.4 Plot Cloud cover on new axes
    data_to_plot.plot(
        x = "time",
        y = "cloud_cover",
        ax = ax2b,
        color = "green",
        kind = "line",
        drawstyle = "steps-post",
        label = "Cloud cover"
    )
    # 2.5 Add labels
    ax2.set_ylabel(precip_label)
    ax2b.set_ylabel(cloud_label)
    ax2.set_xlabel("Time")
    # 2.6 Customize legends
    ax2.legend(loc="upper left", fontsize = LGND_FS)
    ax2b.legend(loc="upper right", fontsize = LGND_FS)
    # 2.7 Add title for the sub plot
    ax2.set_title("Precipitation & cloud cover", fontsize = SP_FS)
    # Set bottom val as 0 for both
    ax2.set_ylim(bottom=0)
    ax2b.set_ylim(bottom=0)
    
    # Panel 3: Surface Pressure ----------------
    # type: line and steps

    # 3.1 Get title value
    sp_label = get_label_value("surface_pressure")
    # 3.2 Optional marker only for 5hr and 24hr plotting
    marker_sign = "o" if duration in ("5hr","24hr") else None
    # 3.3 Plot Surface pressure
    data_to_plot.plot(
        x="time",
        y="surface_pressure",
        ax=ax3,
        color="purple",
        kind="line",
        label = sp_label,
        marker = marker_sign
        )
    # 3.4 Set labels
    ax3.set_xlabel("Time")
    ax3.set_ylabel(sp_label)
    # 3.5 Set sub plot title
    ax3.set_title(sp_label, fontsize = SP_FS)
    # 3.6 Customize the legend
    ax3.legend(loc="upper left", fontsize = LGND_FS)

    # Panel 4: Wind direction and Wind speed ----------------
    # type: Rose

    # 4.1 Hide the x and y ticks of the sub plot
    ax4.set_xticks([])
    ax4.set_yticks([])

    # 4.2 Getting stats for Wind speed
    stats_text_ws = (f"Wind Speed\n"
              f"Min: {min_max_mean["wind_speed_10m"]["min"]:.1f}\n"
              f"Max: {min_max_mean["wind_speed_10m"]["max"]:.1f}\n"
              f"Avg: {min_max_mean["wind_speed_10m"]["avg"]:.1f}")
    
    # 4.3 Add text to show min, max and avg values
    ax4.text(0.05, 0.85, stats_text_ws, 
         transform=ax4.transAxes, 
         fontsize=10, 
         verticalalignment="top",
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))

    # 4.4 Get labels
    wd_label = get_label_value("wind_direction_10m")
    ws_label = get_label_value("wind_speed_10m")
    
    # 4.5 Wind direction as angles
    angles = np.deg2rad(data_to_plot["wind_direction_10m"])
    speeds = data_to_plot["wind_speed_10m"]
    # 4.6 Add subplot
    ax4 = fig.add_subplot(2,2,4, projection= "polar")
    # 4.7 Plotting
    ax4.bar(angles+np.pi, speeds, width=0.2, color=["blue","pink","purple","red","green","orange"], alpha=0.7)
    # 4.8 Set location
    ax4.set_theta_zero_location("N")
    ax4.set_theta_direction(-1)
    # 4.9 Fix positions
    ax4.set_xticks(np.deg2rad([0,45,90,135,180,225,270,315]))
    ax4.set_xticklabels(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
    # 4.10 Set sub plot title
    ax4.set_title("Wind speed & direction", fontsize = SP_FS)
    # To add a text inside after plotting: this will add text inside the polar graph
    # inner_txt = f"{wd_label} \n & \n {ws_label}"
    # ax4.text(0.02, 0.95, inner_txt)
    # To remove the outer circle
    # ax4.spines["polar"].set_visible(False)

    # 4.11 Set the figure title
    fig.suptitle(plot_title, fontsize = FT_FS, fontweight = "bold")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def visuals_plotter_daily(anlyzd: pd.DataFrame, duration: str = "1m", unit_sys: str = "Metric")-> None:
    """
    Creats plot for Daily data
    1. Panel 1: Temperature: temperature_2m_max, temperature_2m_min, apparent_temperature_mean
    2. Panel 2: Precipitation: precipitation
    3. Panel 3: Sunshine duration: sunshine_duration
    4. Panel 4. Wind speed and Wind direction: wind_speed_10m_max, wind_direction_10m_dominant
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

    plot_title = f"Daily Weather data ({unit_sys})"
    plt_all_df, min_max_mean = anlyzd

    if duration == "1m":
        data_to_plot = plt_all_df.iloc[50:89]
        plot_title += " over last 1 month"
    elif duration == "2m":
        data_to_plot = plt_all_df.iloc[30:89]
        plot_title += " over last 2 months"
    elif duration == "3m":
        data_to_plot = plt_all_df.iloc[0:89]
        plot_title += " over last 3 months"

    # print(data_to_plot)

    # Panel 1: Temperature min and max
    # 1.1 Plotting for temperature_2m_max, temperature_2m_min, apparent_temperature_mean
    ax1.plot(data_to_plot["time"], data_to_plot["temperature_2m_max"], color="#8E18B9", label="Max Temp.")
    ax1.plot(data_to_plot["time"], data_to_plot["temperature_2m_min"], color="#16519F", label="Min Temp.")
    ax1.plot(data_to_plot["time"], data_to_plot["apparent_temperature_mean"], color = "#09BAB1", label = "Mean Temp.")
    
    # 1.2 Fill between max and min temperatures
    ax1.fill_between(
        data_to_plot["time"],
        data_to_plot["temperature_2m_min"],
        data_to_plot["temperature_2m_max"],
        color = "#C67BD9",
        alpha = 0.3,
        label = "Temp. range"
    )
    # 1.3 Customize legend
    ax1.legend(loc = "upper left", frameon = True, fontsize = LGND_FS)
    # 1.4 Set labels
    # ax1.set_xlabel("Days")
    temp_label = "Temperature"
    temp_postfix = " (\u00b0F)" if unit_sys == "Imperial" else " (\u2103)"
    ax1.set_ylabel(temp_label+temp_postfix)
    # 1.5 Set sub plot title
    ax1.set_title(temp_label, fontsize = SP_FS)

    #Panel 2: precipitation_sum
    # type: bar
    # 2.1 Plot values
    ax2.bar(
        data_to_plot["time"],
        data_to_plot["precipitation_sum"],
        color = "#E18915",
        label = "Precipitation"
    )
    # 2.2 Set labels
    # ax2.set_xlabel("Days")
    ax2.set_ylabel("Precipitation sum")
    # 2.3 Set sub plot title
    ax2.set_title("Precipitation", fontsize = SP_FS)
    # 2.4 Customize legend
    ax2.legend(loc = "upper left", frameon = True, fontsize = LGND_FS)

    #Panel 3: sunshine_duration
    # type: bar
    # 3.1 Get title value
    ss_label = get_label_value("sunshine_duration")
    # 3.2 Plot sunshine_duration
    ax3.plot(
        data_to_plot["time"],
        data_to_plot["sunshine_duration"],
        color = "#DBDB07",
        label = ss_label
    )
    # 3.3 Set labels
    # ax3.set_xlabel("Days")
    ax3.set_ylabel(ss_label)
    # 3.4 Get title value
    ax3.set_title(ss_label, fontsize = SP_FS)

    #Panel 4:  wind_speed_10m_max,  wind_direction_10m_dominant
    # type: Rose

    # 4.1 Hide the x and y ticks of the sub plot
    ax4.set_xticks([])
    ax4.set_yticks([])

    # 4.2 Getting stats for Wind speed
    stats_text_ws = (f"Wind Speed\n"
              f"Min: {min_max_mean["wind_speed_10m_max"]["min"]:.1f}\n"
              f"Max: {min_max_mean["wind_speed_10m_max"]["max"]:.1f}\n"
              f"Avg: {min_max_mean["wind_speed_10m_max"]["avg"]:.1f}")
    
    # 4.3 Add text to show min, max and avg values
    ax4.text(0.05, 0.85, stats_text_ws, 
         transform=ax4.transAxes, 
         fontsize=10, 
         verticalalignment="top",
         bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))
    
    # 4.4 Get labels
    # wd_label = get_label_value("wind_direction_10m_dominant")
    # ws_label = get_label_value("wind_speed_10m_max")
    
    # 4.5 Wind direction as angles
    angles = data_to_plot["wind_direction_10m_dominant"]
    speed = data_to_plot["wind_speed_10m_max"]
    # 4.6 Add subplot
    ax4 = fig.add_subplot(2, 2, 4, projection = "polar")
    # 4.6 Plotting
    ax4.bar(angles+np.pi, speed, width = 0.2, color =["blue","pink","purple","red","green","orange"], alpha = 0.7)
    # 4.8 Set location
    ax4.set_theta_zero_location("N")
    ax4.set_theta_direction(-1) # Clockwise
    # 4.9 Fix positions
    ticks_deg = [0, 45, 90, 135, 180, 225, 270, 315]
    ticks_rad = np.deg2rad(ticks_deg) # Show full circle
    labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    # 4.10 Set labels
    ax4.set_xticks(ticks_rad)
    ax4.set_xticklabels(labels)
    # 4.11 Set sub plot title
    ax4.set_title("Wind speed & direction", fontsize = SP_FS)
    fig.suptitle(plot_title, fontsize = FT_FS, fontweight = "bold")

    # to avoid overlap x-axis labels
    for ax in [ax1, ax2, ax3]:
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def visualize_weather(coords: tuple, duration: str, unit_sys: str):
    """
    Docstring for visualize_weather
    
    :param coords: A tuple of latitude and longitude
    :type coords: tuple
    :param duration: User duration code defined in get_configured_durations()
    :type duration: str
    """
    # conf_dura = get_configured_durations()
    # Check if the data is hourly
    if duration in ("5hr","24hr","pst_4d","nxt_3d"):
        # Check if unit is ISO or Imperial
        if unit_sys == "Metric":
            raw_data = fetch_hourly_metric_data(coords[0], coords[1])
        else:
            raw_data = hourly_imperial_data(coords[0], coords[1])
        df_hourly = data_in_table(raw_data)
        hr_anls_df = analyze_data_hourly(df_hourly)

        #Visualize the hourly data
        visuals_plotter_hourly(hr_anls_df, duration, unit_sys)
    else:# the data is daily
        max_past = 90
        start = date.today()-timedelta(days= max_past)
        end = date.today()-timedelta(days=1)

        if unit_sys == "Metric":
            raw_data = fetch_daily_data(coords[0], coords[1], from_date = start, to_date = end)
        else:
            raw_data = raw_daily_data_imperial(coords[0], coords[1], from_date = start, to_date = end)

        df_daily = daily_data_table(raw_data)
        daily_anlyzd = analyze_data_daily(df_daily, max_past)

        visuals_plotter_daily(daily_anlyzd, duration, unit_sys)

def get_user_input()-> tuple:
    """
    Docstring for get_user_input
    
    :return: A tuple of city coordinate (tuple), user duration, Unit system
    :rtype: tuple
    """
    city_coords = ()
    while city_coords == ():
        city_coords = get_user_city_coords()
    
    user_duration = ""
    while user_duration == "":
        user_duration = get_user_duration()
    
    user_unit = ""
    while user_unit == "":
        user_unit = get_user_unit()

    return (city_coords, user_duration, user_unit)

#-------- Functions for getting data and plotting : End --------

#-------------------Adiitional functions--------
def visuals_plotter_single(anlyzd: tuple, duration: str, label: str) -> None:
    """
    function to plot using anlyzed data
    
    :param adf: Description
    :type adf: pd.DataFrame
    """
    label_val = get_label_value(label)
    if duration == "5hr":#--------
        data_to_plot = anlyzd[1]
        plot_title = f"{label_val} over 5 hours"
    
    elif duration == "24hr":
        data_to_plot = anlyzd[2]
        plot_title = f"{label_val} whole day"

    elif duration == "pst_4d":
        data_to_plot = anlyzd[3]
        plot_title = f"{label_val} over past 4 days"

    elif duration == "nxt_3d":
        data_to_plot = anlyzd[4]
        plot_title = f"{label_val} forcast for next 3 days"
    
    # print(data_to_plot)

    data_to_plot.plot(
        x="time",
        y = label,
        kind = "line",
        linewidth = 2.0,
        title = plot_title,
        marker = "o",
        color = "#09637E"
    )
    plt.xlabel("Time", color = "#09637E")
    plt.ylabel(label_val, color = "#09637E")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    from data_processing import (
        fetch_hourly_metric_data,
        hourly_imperial_data,
        data_in_table,
        fetch_daily_data,
        raw_daily_data_imperial,
        daily_data_table
    )
    from analysis import (
        analyze_data_daily,
        analyze_data_hourly
    )

    # get user input
    city_coords, user_duration, user_unit= get_user_input()

    #Visualize
    visualize_weather(city_coords, user_duration, user_unit)