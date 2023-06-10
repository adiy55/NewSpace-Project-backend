from flask_restful import Resource, reqparse
from flask import request, abort

from stellarium_client import get_screenshot, query_objects
import base64


class FindStars(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', location='args')
            args = parser.parse_args()
            star_name = args.get('name', None)
            print(star_name)
            if star_name is not None:
                status, content = query_objects(name=star_name)
                if status == 200:
                    return {'content': content}
                else:
                    return {'content': 'bad request'}, status
        except Exception as e:
            abort(400, str(e))

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
            gps_img_direction = received_data.get('gps_img_direction')
            altitude = received_data.get('altitude')
            print(received_data)
            screenshot_path = get_screenshot(latitude, longitude, datetime_str, gps_img_direction, altitude)
            with open(screenshot_path, 'rb') as f:
                encoded_image = base64.b64encode(f.read()).decode()
            return {'status': "accepted", 'encBase64': encoded_image}
        except Exception as e:
            abort(400, str(e))
