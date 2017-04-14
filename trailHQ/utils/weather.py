# coding: interpy

import requests
from pprint import pprint

endpoint = "https://api.weather.gov"

# this method will make the request to the NWS API
def GetWeather(lat, long):
    forecastZip = "/points/#{lat},#{long}/forecast"

    r = requests.get(endpoint+forecastZip)
    weather = decodeResults(r)
    return weather


# parse results
def decodeResults(response):
    json_content = response.json()
    weatherInfo = json_content["properties"]["periods"]

    # the info we only care about right now is today and then the weekend

    weatherDict = dict()
    weatherDict['today'] = [weatherInfo[0]["shortForecast"], weatherInfo[0]["temperature"], weatherInfo[0]["icon"]]
    friday = ""
    saturday = ""
    for day in weatherInfo:
        if day["name"] == "Friday":
            weatherDict["friday"] = [day["shortForecast"], day["temperature"], day["icon"]]
        if day["name"] == "Saturday":
            weatherDict["saturday"] = [day["shortForecast"], day["temperature"], day["icon"]]
            break

    return weatherDict


