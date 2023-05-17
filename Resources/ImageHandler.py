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
            path = os.path.join(self.image_dir, args_filename)
            with open(path, 'rb') as f:
                encoded_image = base64.b64encode(f.read()).decode()
            return {'image': encoded_image}
        except Exception as e:
            abort(400, str(e))

    def post(self):
        filenames = []
        try:
            data = request.json
            image_array = data.get('images', None)
            if image_array is None:
                raise Exception("Missing images key in request!")
            for encoded_image in image_array:
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
                filenames.append(unique_filename)

            return {'filenames': filenames}

        except Exception as e:
            for fn in filenames:
                os.remove(os.path.join(self.image_dir, fn))
            abort(400, str(e))
