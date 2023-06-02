from flask import Flask  # This is a package which creates the framework for our web application (HTTP server)
from flask_restful import Api  # This is an extension to Flask which adds REST API + object abstraction
from flask_cors import CORS

# https://flask-restful.readthedocs.io/en/latest/quickstart.html
app = Flask(__name__)
CORS(app)  # A security feature that blocks web pages from making requests to a different domains
api = Api(app)  # Adds flask_restful
