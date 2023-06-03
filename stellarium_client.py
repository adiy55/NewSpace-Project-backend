import time
from PIL import Image
import requests
import datetime
import math
import julian
import json
import os
import glob

url_main = "http://localhost:8090/api/"


def get_screenshot(latitude, longitude, datetime_str, fov=60):
    if fov and latitude and longitude and datetime_str:
        __set_fov(fov=fov)
        __set_location(latitude=latitude, longitude=longitude)
        __set_datetime(datetime_str)
    try:
        # Create a screenshot of the current view
        url_screenshot = 'stelaction/do'
        screenshot = requests.post(url_main + url_screenshot, data={'id': 'actionSave_Screenshot_Global'})
        print("Screenshot: ", screenshot.status_code, screenshot.content, screenshot.text)
        return __get_most_recent_screenshot()
    except Exception as e:
        print("get_screenshot", e)


def __set_fov(fov):
    try:
        param_fov = {'fov': fov}
        url_fov = "main/fov"
        resp = requests.post(url_main + url_fov, data=param_fov)
        if resp.status_code == 200:
            print("FOV set successfully.")
        else:
            print("Failed to set the FOV.")
    except Exception as e:
        print("__set_fov", e)


def __set_datetime(datetime_str):
    try:
        # Define the format of the datetime string
        datetime_format = "%Y:%m:%d %H:%M:%S"
        # Parse the datetime string into a datetime object
        parsed_datetime = datetime.datetime.strptime(datetime_str, datetime_format)
        payload = {'time': str(julian.to_jd(parsed_datetime, fmt='jd'))}
        url_datetime = "main/time"
        resp = requests.post(url_main + url_datetime, data=payload)
        if resp.status_code == 200:
            print("Date and time set successfully.")
        else:
            print("Failed to set the date and time.")
    except Exception as e:
        print("__set_datetime", e)


def __set_location(latitude, longitude):
    try:
        url_location = 'location/setlocationfields'
        params = {
            'longitude': longitude,
            'latitude': latitude,
        }
        resp = requests.post(url_main + url_location, data=params)
        if resp.status_code == 200:
            print('Location service request successful')
        else:
            print('Location service request failed:', resp.text)
    except Exception as e:
        print("__set_location", e)


def __get_most_recent_screenshot():
    try:
        directory = "C:/Users/adiya/Pictures/Stellarium"  # Default directory where Stellarium saves screenshots
        list_of_files = glob.glob(directory + '/*')
        if not list_of_files:
            return None
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)
        return latest_file
    except Exception as e:
        print("__get_most_recent_screenshot", e)
