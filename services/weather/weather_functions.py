import pandas as pd
import requests
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

import urllib.request
import sys
import pprint
from pandas import json_normalize
import json


def get_berlin():
    """
    This function returns a csv that contains
    """
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 52.5244,
        "longitude": 13.4105,
        "daily": ["sunrise", "rain_sum", "showers_sum"],
        "hourly": [
            "temperature_2m",
            "precipitation",
            "rain",
            "snowfall",
            "relative_humidity_2m",
            "wind_speed_10m",
            "wind_speed_120m",
        ],
        "past_days": 92,
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
    hourly_rain = hourly.Variables(2).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(3).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_speed_120m = hourly.Variables(6).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["rain"] = hourly_rain
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_speed_120m"] = hourly_wind_speed_120m

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print(hourly_dataframe)

    daily = response.Daily()
    daily_sunrise = daily.Variables(0).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(1).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(2).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        )
    }

    daily_data["sunrise"] = daily_sunrise
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum

    daily_dataframe = pd.DataFrame(data=daily_data)
    return daily_dataframe


def get_amsterdam():
    # this function returns a pandas dataframe that contains data pertaining to amsterdam's weather
    api_key = "3PKVXWUQ7Q3ZAR7M37LDNQ2D2"
    try:
        ResultBytes = urllib.request.urlopen(
            f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Amsterdam%2C%20Noord-Holland%2C%20Nederland/2025-02-1/2025-03-13?unitGroup=us&key={api_key}&contentType=json"
        )

        jsonData = json.load(ResultBytes)

    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print("Error code: ", e.code, ErrorInfo)
        sys.exit()
    except urllib.error.URLError as e:
        ErrorInfo = e.read().decode()
        print("Error code: ", e.code, ErrorInfo)
        sys.exit()

    if jsonData:
        a = json_normalize(jsonData)
        file = pd.DataFrame(a)
        return file
