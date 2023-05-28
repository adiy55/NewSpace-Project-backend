import time
from PIL import Image
import requests
import datetime
import math
import julian

url_main = "http://localhost:8090/api/"


def __set_fov(fov):
    pass


def __set_datetime(datetime_str="2023:01:10 20:00:37"):
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


def __set_location(latitude=41.28, longitude=13.24):
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


def set_params_for_screenshot(fov=190):
    param_fov = {'fov': fov}
    url_fov = "main/fov"
    fov = requests.post(url_main + url_fov, data=param_fov)
    print("FOV: ", fov)

    # Set the view to face upward, but slightly South so that is North is up
    param_view = {'altAz': '[0.0001,0,1]'}
    url_view = "main/view"
    view = requests.post(url_main + url_view, data=param_view)
    print("View: ", view)

    __set_location()
    __set_datetime()

    # Create a screenshot of the current view
    url_screenshot = 'stelaction/do'
    screenshot = requests.post(url_main + url_screenshot, data={'id': 'actionSave_Screenshot_Global'})
    print("Screenshot: ", screenshot)


if __name__ == "__main__":
    set_params_for_screenshot(60)

    url_status = "main/status"
    response = requests.get(url_main + url_status)
    print("Status: ", response.status_code)
    if response.status_code == 200:
        print("Time: ", response.json().get('time'))
        print("Location: ", response.json().get('location'))
        print("View: ", response.json().get('view'))
