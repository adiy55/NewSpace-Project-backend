from flask import Flask  # This is a package which creates the framework for our web application (HTTP server)
from flask_restful import Api  # This is an extension to Flask which adds REST API + object abstraction
from flask_cors import CORS
from Resources.Example import Example
from Resources.ImageHandler import ImageHandler

# https://flask-restful.readthedocs.io/en/latest/quickstart.html
app = Flask(__name__)
CORS(app)  # A security feature that blocks web pages from making requests to a different domains
api = Api(app)  # Adds flask_restful

api.add_resource(Example, '/example')
api.add_resource(ImageHandler, '/image')

if __name__ == '__main__':
    app.run(debug=True)
