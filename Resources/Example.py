from flask_restful import Resource
from flask import request, abort


class Example(Resource):

    def get(self):
        return {'response': 'Hello world'}

    def post(self):
        try:
            received_data = request.json
            body = received_data.get('data')
            print(body)
            return {'status': "accepted"}
        except Exception as e:
            abort(400, str(e))
