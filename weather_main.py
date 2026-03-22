from visuals import Visuals
import pandas as pd

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

class UserInputs:
    """
    Clss for UserInputs
    """
    def __init__(self):
        self.city_coords, self.duration, self.unit_sys = self.user_inputs()
    
    def user_inputs(self):
        """
        Get user input
        """
        city_coords = None
        while not city_coords:
            city_coords = self.get_user_city_coords()

        user_duration = ""
        while not user_duration:
            user_duration = self.get_user_duration()

        user_unit = ""
        while not user_unit:
            user_unit = self.get_user_unit()

        return (city_coords, user_duration, user_unit)
    
    def get_user_city_coords(self):
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
    

    #-------- Functions for configured values : Start--------
    def get_configured_durations(self)-> dict:
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
    
    def get_configured_units(self)-> dict:
        """
        Returns the configured units
        """
        units = {
            "1": "Metric",
            "2": "Imperial"
        }
        return units
    #-------- Functions for configured values : End--------
    
    def get_user_unit(self)->str:
        """
        Gets unit from user
        """
        options = self.get_configured_units()
        print()
        print("-"*10)
        print("Select unit:")
        print("1: Metric (SI) || 2: Imperial")
        user_unit = input("Enter 1/2:")
        if not user_unit.isdigit() or user_unit == "" or (user_unit.isdigit() and len(user_unit)>1):
            print("Enter only single digits")
            user_unit = self.get_user_unit()
        
        if not user_unit in options:
            print("Not a valid option")
            user_unit = self.get_user_unit()
        return options[user_unit]
    
    def get_user_duration(self)-> str:
        """
        Gets duration from user
        """
        options = self.get_configured_durations()
        print()
        print("-"*10)
        print("Select durations:")
        print("1: Last 5 hours || 2: Today || 3: Past 4 days || 4: Next 3 days")
        print("Or")
        print("5: Past 1 month || 6: Past 2 month || 7: Past 3 month")
        user_duration = input("Enter 1/2/3/4/5/6/7:")
        if not user_duration.isdigit() or user_duration == "" or (user_duration.isdigit() and len(user_duration)>1):
            print("Enter only single digits")
            user_duration = self.get_user_duration()
        
        if not user_duration in options:
            print("Not a valid option")
            user_duration = self.get_user_duration()
        return options[user_duration]

def main():
    user_data = UserInputs()
    Visuals(user_data.city_coords, user_data.duration, user_data.unit_sys)
    
if __name__ == "__main__":
    main()