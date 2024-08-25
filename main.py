import DisplayDriver
import WeatherDataTools
import json

with open('/home/effex/inky-temp/config.json') as config_file:
    init_values = json.load(config_file)

wdt = WeatherDataTools.WeatherDataTools(city_id=init_values['city_id'],
                                        api_key=init_values['api_key'],
                                        db_name=init_values['db_name'],
                                        collection_name=init_values['collection_name'])
dd = DisplayDriver.DisplayDriver()

def weather_display_system():

    input = []

    #try:
    wdt.weather_data_process()
    #except:
    #    print("Data update failed. Defaulting to stored data.")

    try:
        useful_info = wdt.return_weather_Data()
    except:
        useful_info = {"condition":"ERROR","current_temp":00,"min_temp":00,
                          "max_temp":00,"rain_chance":False, "wind_speed":00,
                             "wind_direction":"XX"}

    print(useful_info)

    message = useful_info['condition']

    # The following is because Open Weather Map can give some oddly specific weather data. Like "Very heavy rain".
    # The length causes display issues, so it is split and only the actual description is used. Assuming one is not
    # in a bunker, one should notice the difference between "Rain" and "Really fucking heavy rain."
    if len(message) > 12:
        first, *middle, message = message.split()

    temp = str(useful_info['current_temp']) + "°"
    min = str(useful_info['min_temp']) + "°"
    max = str(useful_info['max_temp']) + "°"
    wind_speed = str(useful_info['wind_speed']) + "M/s"
    wind_dir = str(useful_info['wind_direction'])

    rain_check = useful_info['rain_chance']

    if not rain_check:
        rain_chance = "0%"
    else:
        rain_chance = useful_info['rain_chance']

    first_display = temp + " - " + message

    second_display = "Risk of Rain: " + str(rain_chance)

    third_display = " Wind: " + wind_speed + " " + wind_dir

    fourth_display = "min: " + min + " - max: " + max

    input.append(first_display)
    input.append(second_display)
    input.append(third_display)
    input.append(fourth_display)

    dd.display_notification_message(data=input)

weather_display_system()
