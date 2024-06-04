import requests
from tkinter import *
import math
from datetime import datetime
import pytz
from PIL import Image, ImageTk

api_key = "997f9e08a086a6bec3facde688bfbb35"
TIMEZONEDB_API_KEY = "YOUR_TIMEZONEDB_API_KEY"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x500")
        self.root.title("Weather and Time Information")
        self.weather_icons = {
            "Clear": "icons/sunny.png",
            "Clouds": "icons/cloudy.png",
            "Rain": "icons/rainy.png",
            "Snow": "icons/snowy.png",
            "Thunderstorm": "icons/stormy.png"
        }
        self.current_city = StringVar()
        self.current_city.set("Mumbai")

        self.create_widgets()
        self.update_weather_info()

    def create_widgets(self):
        # Weather Display
        self.weather_frame = Frame(self.root)
        self.weather_frame.pack(pady=10)

        self.weather_icon_label = Label(self.weather_frame)
        self.weather_icon_label.pack()

        self.weather_info_label = Label(self.weather_frame, text="", font=("Helvetica", 14))
        self.weather_info_label.pack()

        # Temperature Unit Selection
        self.temp_unit_frame = Frame(self.root)
        self.temp_unit_frame.pack()

        self.temp_unit = StringVar()
        self.temp_unit.set("Fahrenheit")

        self.temp_unit_label = Label(self.temp_unit_frame, text="Temperature Unit:")
        self.temp_unit_label.grid(row=0, column=0)

        self.temp_unit_menu = OptionMenu(self.temp_unit_frame, self.temp_unit, "Celsius", "Fahrenheit")
        self.temp_unit_menu.grid(row=0, column=1)

        # City Selection and Update Button
        self.city_frame = Frame(self.root)
        self.city_frame.pack(pady=10)

        self.city_label = Label(self.city_frame, text="Enter city name:")
        self.city_label.grid(row=0, column=0)

        self.city_entry = Entry(self.city_frame, textvariable=self.current_city)
        self.city_entry.grid(row=0, column=1)

        self.update_button = Button(self.city_frame, text="Search Weather", command=self.update_weather_info)
        self.update_button.grid(row=0, column=2)

        # Time Display
        self.time_label = Label(self.root, text="", font=("Helvetica", 14))
        self.time_label.pack(pady=10)

        # Update time every second
        self.update_time()

    def update_weather_info(self):
        city = self.current_city.get()
        weather_data = self.get_weather(api_key, city)
        if weather_data:
            self.display_weather_info(weather_data)
        else:
            self.weather_info_label.config(text="Error: Weather information not available.")

    def get_weather(self, api_key, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url).json()

        if 'main' in response and 'weather' in response:
            temp = response['main']['temp']
            feels_like = response['main']['feels_like']
            humidity = response['main']['humidity']
            weather_main = response['weather'][0]['main']
            return {
                'temp': temp,
                'feels_like': feels_like,
                'humidity': humidity,
                'weather_main': weather_main
            }
        else:
            return None

    def display_weather_info(self, weather):
        temp_unit = self.temp_unit.get()
        temp = self.convert_temperature(weather['temp'], temp_unit)
        feels_like = self.convert_temperature(weather['feels_like'], temp_unit)
        humidity = weather['humidity']
        weather_main = weather['weather_main']
        self.weather_info_label.config(text=f"Temperature: {temp}°{temp_unit}\nFeels Like: {feels_like}°{temp_unit}\nHumidity: {humidity}%\nWeather: {weather_main}")
        self.display_weather_icon(weather_main)

    def convert_temperature(self, temperature, to_unit):
        if to_unit == "Celsius":
            return round(temperature - 273.15, 2)
        elif to_unit == "Fahrenheit":
            return round((temperature - 273.15) * 9/5 + 32, 2)
        else:
            return temperature

    def display_weather_icon(self, weather_main):
        if weather_main in self.weather_icons:
            icon_path = self.weather_icons[weather_main]
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((50, 50), Image.ANTIALIAS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            self.weather_icon_label.config(image=icon_photo)
            self.weather_icon_label.image = icon_photo

    def update_time(self):
        city = self.current_city.get()
        city_timezone = self.get_timezone(city)
        if city_timezone:
            city_time = datetime.now(city_timezone)
            formatted_time = city_time.strftime('%Y-%m-%d %H:%M:%S %Z')
            self.time_label.config(text=f"Time ({city}): {formatted_time}")
        else:
            self.time_label.config(text="Timezone information not found for the specified city.")
        self.root.after(1000, self.update_time)

    def get_timezone(self, city):
        try:
            geonames_url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={TIMEZONEDB_API_KEY}&format=json&by=position&lat=YOUR_LATITUDE&lng=YOUR_LONGITUDE"
            response = requests.get(geonames_url).json()
            if 'status' in response and response['status'] == 'OK':
                return pytz.timezone(response['zoneName'])
            else:
                return pytz.timezone('Asia/Kolkata')  # Default to Kolkata timezone
        except Exception as e:
            print(f"Error getting timezone information: {e}")
            return None

if __name__ == "__main__":
    root = Tk()
    app = WeatherApp(root)
    root.mainloop()
