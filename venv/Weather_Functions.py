import pyowm                        #Package for weather forecasts via the OpenWeather API
    # On raspberry pi: use sudo pip install pyowm
from datetime import datetime

def current_weather(timestamp):
    # Inputs
    OWM_key = '4486f60ddf98ce6ed3b4e248703e1d1b'                # Key for free API requests from OpenWeather API
    house_lat = 50.996880                                       # House lat
    house_lon = 3.641542                                        # House lon

    owm = pyowm.OWM(OWM_key)                                    # Create owm object
    observation = owm.weather_at_coords(house_lat, house_lon)   # Observe weather
    w = observation.get_weather()                               # Get weather
    uvi = owm.uvindex_around_coords(house_lat, house_lon)

    # Current weather from Open Weather Map
    new_entry = (timestamp, w.get_reference_time(timeformat='date').timestamp(), w.get_clouds(), str(w.get_rain()), str(w.get_wind()),
                 w.get_humidity(), w.get_pressure()['press'], w.get_temperature(unit='celsius')['temp'], uvi.get_value(),
                 w.get_status(), w.get_detailed_status(), w.get_weather_code())
    return new_entry