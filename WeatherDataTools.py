import requests
import json
import datetime
import pymongo

class WeatherDataTools:

    def __init__(self, api_key, city_id, db_name, collection_name):

        self.api_key = api_key
        self.city_id = city_id
        self.db_name = db_name
        self.collection_name = collection_name

    def get_weather_data(self):
        baseurl = "http://api.openweathermap.org/data/2.5/weather?id={}".format(self.city_id)

        access_token = "&APPID=" + self.api_key

        full_request_url = baseurl + access_token

        print("Making request at: " + full_request_url)

        try:
            weather_info = requests.get(full_request_url)
        except:
            print("No weather data collected")
            return False

        print(weather_info)

        weather_json = weather_info.json()

        #print(weather_json)

        current_temp = int(int(weather_json['main']['temp']) - 273.15)
        min_temp = int(int(weather_json['main']['temp_min']) - 273.15)
        max_temp = int(int(weather_json['main']['temp_max']) - 273.15)
        condition = weather_json['weather'][0]['description']

        return_data = {"current_temp":current_temp,
                       "min_temp": min_temp,
                       "max_temp": max_temp,
                       "condition":condition}

        return return_data

    def get_rain_data(self):
        baseurl = "http://api.openweathermap.org/data/2.5/forecast?id={}".format(self.city_id)

        access_token = "&APPID=" + self.api_key

        full_request_url = baseurl + access_token

        print("Making request at: " + full_request_url)

        try:
            weather_info = requests.get(full_request_url)
        except:
            print("No weather data collected")
            return ""

        print(weather_info)

        weather_json = weather_info.json()

        #print(weather_json)

        today = datetime.datetime.now().strftime("%Y-%m-%d")

        rain_chance = False

        for item in weather_json['list'][:8]:

            match = item['dt_txt'][:10]  # Gets the item's date for comparison

            if match == today:
                rain_check = item['weather'][0]['main']

                if rain_check == "Rain":
                    rain_chance = True

        return rain_chance


    def weather_data_to_mongo(self, weather_data):

        client = pymongo.MongoClient()
        database = client[self.db_name]

        collection = database[self.collection_name]

        cursor = collection.find({'date': weather_data['date']})

        min_list = []
        max_list = []

        min_list.append(int(weather_data['min_temp']))
        max_list.append(int(weather_data['max_temp']))

        for record in cursor:
            min_list.append(int(record['min_temp']))
            max_list.append(int(record['max_temp']))

        weather_data['min_temp'] = min(min_list)
        weather_data['max_temp'] = max(max_list)

        collection.insert_one(weather_data)

        return "OK"

    def weather_data_process(self):

        weather_data = self.get_weather_data()
        if weather_data:
            weather_data['rain_chance'] = self.get_rain_data()
            weather_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d")
            weather_data['time'] = datetime.datetime.now().strftime("%H:%M:%S")
            weather_data['timestamp'] = datetime.datetime.now().timestamp()
            response = self.weather_data_to_mongo(weather_data)
            print("Weather to database: {}".format(response))

    def return_weather_Data(self):
        client = pymongo.MongoClient()
        database = client[self.db_name]
        collection = database[self.collection_name]
        cursor = collection.find().skip(collection.count() - 1)
        response_data = {}

        for record in cursor:
            latest_data = record
            response_data['min_temp'] = record['min_temp']
            response_data['max_temp'] = record['max_temp']
            response_data['date'] = record['date']
            response_data['time'] = record['time']
            response_data['rain_chance'] = record['rain_chance']
            response_data['timestamp'] = record['timestamp']
            response_data['condition'] = record['condition']
            response_data['current_temp'] = record['current_temp']

        return response_data

