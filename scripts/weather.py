from pyowm.owm import OWM
import datetime

# TODO: Fix api key exposure
owm = OWM('e9dd1343ae35d3b8db26656b78b75c45')
mgr = owm.weather_manager()


def get_current_weather(lat, lon):
    one_call = mgr.one_call(lat=lat, lon=lon)
    weather_data = one_call.current

    return _get_weather_statements(one_call.timezone.split("/")[1],
                                   weather_data)


def _get_weather_statements(city, data):
    time = datetime.datetime.fromtimestamp(data.ref_time).date().strftime(
        'Today is %B %d of %Y')

    temperature = f"The current temperature here in {city} is " \
                  f"{data.temperature('celsius')['temp']}, and it feels like " \
                  f"{data.temperature('celsius')['feels_like']}"
    humidity = f"The humidity is {data.humidity} percent. " + \
               ("Not too humid today!" if data.humidity <= 50
                else "It's humid today!")
    rain = "It doesn't seem like it will rain today!" if data.rain == {} \
        else "There is a chance of rain today."
    overview = f"In general, today there will be {data.detailed_status}."
    return [time, temperature, humidity, rain, overview]
