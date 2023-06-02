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


def __set_fov(fov):
    try:
        param_fov = {'fov': fov}
        url_fov = "main/fov"
        fov = requests.post(url_main + url_fov, data=param_fov)
        print("FOV: ", fov)
    except Exception as e:
        print(e, "4")
    # # Set the view to face upward, but slightly South so that is North is up
    # param_view = {'altAz': '[0.0001,0,1]'}
    # url_view = "main/view"
    # view = requests.post(url_main + url_view, data=param_view)
    # print("View: ", view)


def __set_datetime(datetime_str):
    try:
        # Define the format of the datetime string
        datetime_format = "%Y:%m:%d %H:%M:%S"
        # Parse the datetime string into a datetime object
        parsed_datetime = datetime.datetime.strptime(datetime_str, datetime_format)
        # print(parsed_datetime)
        # print(julian.to_jd(parsed_datetime, fmt='jd'))
        payload = {'time': str(julian.to_jd(parsed_datetime, fmt='jd'))}
        url_datetime = "main/time"
        resp = requests.post(url_main + url_datetime, data=payload)
        if resp.status_code == 200:
            print("Date and time set successfully.")
        else:
            print("Failed to set the date and time.")
    except Exception as e:
        print(e, "2")


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
        print(e, "1")


def get_screenshot(fov, latitude, longitude, datetime_str):
    if fov and latitude and longitude and datetime_str:
        __set_fov(fov=fov)
        __set_location(latitude=latitude, longitude=longitude)
        __set_datetime(datetime_str)
    try:
        # Create a screenshot of the current view
        url_screenshot = 'stelaction/do'
        screenshot = requests.post(url_main + url_screenshot, data={'id': 'actionSave_Screenshot_Global'})
        print("Screenshot: ", screenshot.status_code, screenshot.content, screenshot.text)
        return get_most_recent_screenshot()
    except Exception as e:
        print(e, "0")


def get_most_recent_screenshot():
    print("1")
    directory = "StellariumScreenshots"
    list_of_files = glob.glob(directory + '/*')
    if not list_of_files:
        return None
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    return latest_file


# if __name__ == "__main__":
    # get_screenshot(60, 41.28, 13.24, "2023:01:10 20:00:37")

    # url_status = "main/status"
    # response = requests.get(url_main + url_status)
    # print("Status: ", response.status_code)
    # if response.status_code == 200:
    #     print("Time: ", response.json().get('time'))
    #     print("Location: ", response.json().get('location'))
    #     print("View: ", response.json().get('view'))
