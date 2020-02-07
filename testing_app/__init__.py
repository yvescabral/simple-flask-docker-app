from flask import Flask, request, jsonify


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hey, we have Python in a Docker container!'

    @app.route('/webhook/github', methods=['POST'])
    def github_webhook():
        if request.headers.get('X-GitHub-Event') == 'delete':
            pass
        return jsonify({})

    @app.route('/webhook/docker_hub', methods=['POST'])
    def docker_hub_webhook():
        print(request.data.decode('utf8'))
        return jsonify({})

    return app
