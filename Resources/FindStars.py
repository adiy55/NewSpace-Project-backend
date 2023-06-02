from flask_restful import Resource
from flask import request, abort
from stellarium_client import get_screenshot
import base64


class FindStars(Resource):

    def get(self):
        return {'response': 'Hello world'}

    def post(self):
        """
        {'fov': 60, 'latitude': 41.28, 'longitude': 13.24, 'datetime_str': "2023:01:10 20:00:37"}
        :return:
        """
        try:
            received_data = request.json
            fov = received_data.get('fov')
            latitude = received_data.get('latitude')
            longitude = received_data.get('longitude')
            datetime_str = received_data.get('datetime_str')
            screenshot_path = get_screenshot(fov, latitude, longitude, datetime_str)
            with open(screenshot_path, 'rb') as f:
                encoded_image = base64.b64encode(f.read()).decode()
            return {'status': "accepted", 'encBase64': encoded_image}
        except Exception as e:
            abort(400, str(e))
