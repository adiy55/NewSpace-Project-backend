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


def get_screenshot(latitude, longitude, datetime_str, img_direction, altitude, fov=60):
    if latitude and longitude and datetime_str and img_direction and altitude:
        __set_view(compass_direction=img_direction)
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


def __set_view(compass_direction):
    try:
        url_view = "main/view"
        if 90 < compass_direction < 270:
            south_value = -((compass_direction % 180) / 180 - 1)
            east_value = -(((compass_direction - 90) % 180 - 90) / 90)
        else:
            south_value = (compass_direction % 180) / 180 - 1
            east_value = ((compass_direction - 90) % 180 - 90) / 90
        params = {'altAz': f'[{south_value}, {east_value}, 0.25]'}
        resp = requests.post(url_main + url_view, data=params)
        print(resp)
    except Exception as e:
        print("__set_fov", e)


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


def query_objects(name):
    try:
        # find_path = f'simbad/lookup'
        find_path = f'objects/info'
        params = {
            'name': name,
            'format': 'json'
        }
        resp = requests.get(url_main + find_path, data=params)
        return resp.status_code, resp.json()
    except Exception as e:
        print("query_objects", e)
        return 400, 'bad request'


if __name__ == '__main__':
    name = 'Moon'
    query_objects(name)
    # The Simbad querying object
    # simbad = Simbad()
    # simbad.ROW_LIMIT = 20
    # simbad.TIMEOUT = 500
    # result = simbad.query_objects(object_names=name)
    # print(result)
