import base64
import uuid
import imghdr
import os
from io import BytesIO
from PIL import Image
from flask_restful import Resource, reqparse
from flask import request, abort


class ImageHandler(Resource):
    def __init__(self):
        self.image_dir = r'Images'

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('filename', location='args')
            args = parser.parse_args()
            args_filename = args.get('filename', None)
            with open(args_filename, 'rb') as f:
                encoded_image = base64.b64encode(f.read())
            return {'image': encoded_image}
        except Exception as e:
            abort(400, str(e))

    def post(self):
        try:
            data = request.json
            encoded_image = data.get('image', None)
            if encoded_image is None:
                abort(400, "Bad image file")

            decoded_image = base64.b64decode(encoded_image)
            # Determine the file type dynamically using imghdr
            image_extension = imghdr.what(None, h=decoded_image)
            if image_extension is None:
                raise ValueError("Unknown image format")

            if not os.path.exists(self.image_dir):
                os.makedirs(self.image_dir)
            unique_filename = f"{uuid.uuid4().hex}.{image_extension}"
            image = Image.open(BytesIO(decoded_image))
            image.save(os.path.join(self.image_dir, unique_filename), image_extension)
            return {'filename': unique_filename}

        except Exception as e:
            abort(400, str(e))
