from flask import Flask


def build_app():
    app = Flask(__name__)
    return app


flask_app = build_app()


if __name__ == '__main__':
    flask_app.run()