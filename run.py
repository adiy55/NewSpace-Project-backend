from Resources.Example import Example
from Resources.ImageHandler import ImageHandler
from Resources.FindStars import FindStars
from server import api, app

api.add_resource(Example, '/example')
api.add_resource(ImageHandler, '/image')
api.add_resource(FindStars, '/stars')

if __name__ == '__main__':
    app.run(debug=True)
