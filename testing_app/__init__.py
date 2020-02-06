from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hey, we have Flask in a Docker container!'

    return app
