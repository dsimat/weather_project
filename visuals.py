import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
import numpy as np
import matplotlib.ticker as ticker

from data_processing import (
    fetch_hourly_metric_data,
    hourly_imperial_data,
    data_in_table,
    fetch_daily_data,
    raw_daily_data_imperial,
    daily_data_table,
    hourly_data_units,
    daily_data_units
)
from analysis import (
    analyze_data_daily,
    analyze_data_hourly
)

# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
# pd.set_option("display.max_colwidth", None)

# Font sizes
FT_FS = 14 # Figure title font size
SP_FS = 12 # Sub plot title font size
LGND_FS = 9 # Legend font size

class Visuals:
    """
    Class for visualization
    """
    def __init__(self, city_coords, duration, unit_sys):
        self.coords = city_coords
        self.duration = duration
        self.unit_sys = unit_sys
        self.anlyzd = pd.DataFrame()
        self.units_used = {}

        self.visualize_weather()
    
    def visualize_weather(self):
        """
        Docstring for visualize_weather
        
        :param coords: A tuple of latitude and longitude
        :type coords: tuple
        :param duration: User duration code defined in get_configured_durations()
        :type duration: str
        """
        # conf_dura = get_configured_durations()
        # Check if the data is hourly
        if self.duration in ("5hr","24hr","pst_4d","nxt_3d"):
            # Check if unit is ISO or Imperial
            if self.unit_sys == "Metric":
                raw_data = fetch_hourly_metric_data(self.coords[0], self.coords[1])
                # print(hourly_data_units(raw_data))# to delete
            else:
                raw_data = hourly_imperial_data(self.coords[0], self.coords[1])
            self.units_used = hourly_data_units(raw_data)
            hourly_df = data_in_table(raw_data)
            self.anlyzd = analyze_data_hourly(hourly_df)

            #Visualize the hourly data
            self.visuals_plotter_hourly()
        else:# the data is daily
            max_past = 90
            start = date.today()-timedelta(days= max_past)
            end = date.today()-timedelta(days=1)

            if self.unit_sys == "Metric":
                raw_data = fetch_daily_data(
                    self.coords[0],
                    self.coords[1],
                    from_date = start,
                    to_date = end
                )
                # print(daily_data_units(raw_data))# to delete
            else:
                raw_data = raw_daily_data_imperial(
                    self.coords[0],
                    self.coords[1],
                    from_date = start,
                    to_date = end
                )
            self.units_used = daily_data_units(raw_data)
            df_daily = daily_data_table(raw_data)
            self.anlyzd = analyze_data_daily(df_daily, max_past)

            self.visuals_plotter_daily()
    
    def visuals_plotter_hourly(self):
        """
        Creats plot for hourly data
        1. Panel 1: Temperature and humidity
        2. Panel 2: Precipitation and Cloud cover
        3. Panel 3: Surface pressure
        4. Panel 4. Wind speed and Wind direction
        """
         # Figure with 4 subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize = (12, 8))

        data_to_plot, plot_title, min_max_mean = self.get_plot_title_hourly()
        plot_title += f"({self.unit_sys})"

        # print(data_to_plot)
        # Panel 1: Temperature and humidity ----------------

        # 1.1 Get title value for the dataframe parameter
        temp_label = self.get_label_value("temperature_2m")
        # temp_postfix = " (\u00b0F)" if unit_sys == "Imperial" else " (\u2103)"
        temp_lbl_unit = temp_label + f" ({self.units_used["temperature_2m"]})"
        humidity_lable = self.get_label_value("relative_humidity_2m")
        humidity_lbl_unit = humidity_lable + f" ({self.units_used["relative_humidity_2m"]})"

        # 1.2 Plot Temperature
        data_to_plot.plot("time", "temperature_2m", ax = ax1, color = "blue", label = temp_label)
        # 1.3 Create a new twin axes sharing the same x axis
        ax1b = ax1.twinx()
        # 1.4 Plot Relative humidity on new axes
        data_to_plot.plot("time", "relative_humidity_2m", ax = ax1b, color = "red", label = humidity_lable)
        # 1.5 Add labels
        ax1.set_xlabel("Time")
        ax1.set_ylabel(temp_lbl_unit)
        ax1b.set_ylabel(humidity_lbl_unit)
        # 1.6 Customize legends
        ax1.legend(loc="upper left", frameon = True, fontsize = LGND_FS)
        ax1b.legend(loc="upper right", frameon = True, fontsize = LGND_FS)
        # 1.7 Add title for the sub plot
        ax1.set_title("Temperature & humidity", fontsize = SP_FS)

        # Panel 2: Precipitation and Cloud cover ----------------
        # type: line steps

        # 2.1 Get title value
        precip_label = self.get_label_value("precipitation")
        precip_lbl_unit = precip_label + f" ({self.units_used["precipitation"]})"
        cloud_label = self.get_label_value("cloud_cover")
        cloud_lbl_unit = cloud_label + f" ({self.units_used["cloud_cover"]})"

        # 2.2 Plot Precipitation
        data_to_plot.plot(
            x="time",
            y="precipitation",
            ax=ax2,
            color="red",
            kind="line",
            drawstyle="steps-post",
            label = precip_label,
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
            label = cloud_label
        )
        # 2.5 Add labels
        ax2.set_ylabel(precip_lbl_unit)
        ax2b.set_ylabel(cloud_lbl_unit)
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
        sp_label = self.get_label_value("surface_pressure")
        sp_lbl_unit = sp_label + f" ({self.units_used["surface_pressure"]})"
        # 3.2 Optional marker only for 5hr and 24hr plotting
        marker_sign = "o" if self.duration in ("5hr","24hr") else None
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
        ax3.set_ylabel(sp_lbl_unit)
        # 3.5 Set sub plot title
        ax3.set_title(sp_label, fontsize = SP_FS)
        # 3.6 Customize the legend
        ax3.legend(loc="upper left", fontsize = LGND_FS)

        # Panel 4: Wind direction and Wind speed ----------------
        # type: Rose

        # 4.1 Hide the x and y ticks of the sub plot
        ax4.set_xticks([])
        ax4.set_yticks([])

        # 4.2 Get labels
        ws_label = self.get_label_value("wind_speed_10m")
        ws_lbl_unit = ws_label + f"\n({self.units_used["wind_speed_10m"]})"

        # 4.3 Getting stats for Wind speed
        stats_text_ws = (f"{ws_lbl_unit}\n"
                f"Min: {min_max_mean["wind_speed_10m"]["min"]:.1f}\n"
                f"Max: {min_max_mean["wind_speed_10m"]["max"]:.1f}\n"
                f"Avg: {min_max_mean["wind_speed_10m"]["avg"]:.1f}")
        
        # 4.4 Add text to show min, max and avg values
        ax4.text(0.05, 0.85, stats_text_ws, 
            transform=ax4.transAxes, 
            fontsize=10, 
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.5))
        
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

        # 4.12 Hide x axis label and add customized labels for 5 hour plot
        if self.duration == "5hr":
            labels = ["5hr ago", "4hr ago", "3hr ago", "2hr ago", "1hr ago", "Now"]
            for ax in [ax1, ax2, ax3]:
                ax.set_xticks([])
                ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6)) 
                ax.set_xticklabels(labels)

        plt.grid(True)#to check
        plt.tight_layout()
        plt.show()
    
    def visuals_plotter_daily(self)-> None:
        """
        Creats plot for Daily data
        1. Panel 1: Temperature: temperature_2m_max, temperature_2m_min, apparent_temperature_mean
        2. Panel 2: Precipitation: precipitation
        3. Panel 3: Sunshine duration: sunshine_duration
        4. Panel 4. Wind speed and Wind direction: wind_speed_10m_max, wind_direction_10m_dominant
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

        plot_title = f"Daily Weather data ({self.unit_sys})"
        plt_all_df, min_max_mean = self.anlyzd

        if self.duration == "1m":
            data_to_plot = plt_all_df.iloc[50:89]
            plot_title += " over last 1 month"
        elif self.duration == "2m":
            data_to_plot = plt_all_df.iloc[30:89]
            plot_title += " over last 2 months"
        elif self.duration == "3m":
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
        temp_label_unit = f"Temperature({self.units_used["temperature_2m_max"]})"
        # temp_postfix = " (\u00b0F)" if unit_sys == "Imperial" else " (\u2103)"
        ax1.set_ylabel(temp_label_unit)
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
        precip_label = "Precipitation sum"
        precip_lbl_unit = precip_label + "("+self.units_used["precipitation_sum"]+ ")"
        # ax2.set_xlabel("Days")
        ax2.set_ylabel(precip_lbl_unit)
        # 2.3 Set sub plot title
        ax2.set_title(precip_label, fontsize = SP_FS)
        # 2.4 Customize legend
        ax2.legend(loc = "upper left", frameon = True, fontsize = LGND_FS)

        #Panel 3: sunshine_duration
        # type: bar
        # 3.1 Get title value
        ss_label = self.get_label_value("sunshine_duration")
        ss_lbl_unit = ss_label + "(" + self.units_used["sunshine_duration"] + ")"
        # 3.2 Plot sunshine_duration
        ax3.plot(
            data_to_plot["time"],
            data_to_plot["sunshine_duration"],
            color = "#DBDB07",
            label = ss_label
        )
        # 3.3 Set labels
        # ax3.set_xlabel("Days")
        ax3.set_ylabel(ss_lbl_unit)
        # 3.4 Get title value
        ax3.set_title(ss_label, fontsize = SP_FS)

        #Panel 4:  wind_speed_10m_max,  wind_direction_10m_dominant
        # type: Rose

        # 4.1 Hide the x and y ticks of the sub plot
        ax4.set_xticks([])
        ax4.set_yticks([])

        # 4.2 Get labels
        # wd_label = get_label_value("wind_direction_10m_dominant")
        # ws_label = get_label_value("wind_speed_10m_max")

        # 4.3 Getting stats for Wind speed
        ws_label = self.get_label_value("wind_speed_10m_max")
        ws_lbl_unit = ws_label + f"\n({self.units_used["wind_speed_10m_max"]})"
        stats_text_ws = (f"{ws_lbl_unit}\n"
                f"Min: {min_max_mean["wind_speed_10m_max"]["min"]:.1f}\n"
                f"Max: {min_max_mean["wind_speed_10m_max"]["max"]:.1f}\n"
                f"Avg: {min_max_mean["wind_speed_10m_max"]["avg"]:.1f}")
        
        # 4.4 Add text to show min, max and avg values
        ax4.text(.01, 0.85, stats_text_ws, 
            transform=ax4.transAxes, 
            fontsize=10, 
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.5),
            horizontalalignment="left"
            )
        
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
    
    def get_label_value(self, key: str)-> str:
        """
        Docstring for get_label_value
        
        :param key: Dataframe label (str)
        :return: Label on basis of the key
        :rtype: str
        """
        values = {
            "temperature_2m": "Temperature",
            "relative_humidity_2m": "Relative humidity",#"Relative humidity (2 meters)",
            "precipitation": "Precipitation",
            "wind_speed_10m": "Wind speed",#"Wind speed (10 meters/second)",
            "cloud_cover": "Cloud cover",
            "surface_pressure": "Surface Pressure",
            "wind_direction_10m": "Wind direction",# (10 meters)",
            "temperature_2m_min": "Minimum temperature",# (2 meters)",
            "temperature_2m_max": "Maximum temperature",# (2 meters)",
            "apparent_temperature_mean": "Mean apparent temperature",
            "precipitation_sum": "Precipitation sum",
            "sunshine_duration": "Sunshine duration",
            "wind_speed_10m_max": "Highest wind speed",# (10 meters/second)",
            "wind_direction_10m_dominant": "Dominant wind direction",# (10 meters)"
        }
        return values[key]
    
    def get_plot_title_hourly(self)->tuple:
        """
        returns a tuple of:
        1. hourly data as per the selected duration to plot
        2. plot title
        3. dataframe state: min, max, mean for the duration
        """
        if self.duration == "5hr":
            data_to_plot = self.anlyzd[1]
            min_max_mean = self.anlyzd[6]
            plot_title = "Weather over 5 hours"
        
        elif self.duration == "24hr":
            data_to_plot = self.anlyzd[2]
            min_max_mean = self.anlyzd[7]
            plot_title = "Weather whole day"

        elif self.duration == "pst_4d":
            data_to_plot = self.anlyzd[3]
            min_max_mean = self.anlyzd[8]
            plot_title = "Weather over past 4 days"

        elif self.duration == "nxt_3d":
            data_to_plot = self.anlyzd[4]
            min_max_mean = self.anlyzd[9]
            plot_title = "Weather forcast for next 3 days"
        return (data_to_plot, plot_title, min_max_mean)
    
    def visuals_plotter_single(self, label: str) -> None:
        """
        function to plot using anlyzed data
        
        :param adf: Description
        :type adf: pd.DataFrame
        """
        label_val = self.get_label_value(label)
        if self.duration == "5hr":#--------
            data_to_plot = self.anlyzd[1]
            plot_title = f"{label_val} over 5 hours"
        
        elif self.duration == "24hr":
            data_to_plot = self.anlyzd[2]
            plot_title = f"{label_val} whole day"

        elif self.duration == "pst_4d":
            data_to_plot = self.anlyzd[3]
            plot_title = f"{label_val} over past 4 days"

        elif self.duration == "nxt_3d":
            data_to_plot = self.anlyzd[4]
            plot_title = f"{label_val} forcast for next 3 days"

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