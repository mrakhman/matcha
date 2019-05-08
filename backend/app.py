import logging

from flask import Flask, jsonify
from flask import request
from flask.logging import default_handler
from werkzeug.exceptions import HTTPException

from tree.users import users

APP_NAME = "matcha"


# Logging
class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)


def app_factory(name):
    flask_app = Flask(name)
    flask_app.config.from_object('config.DevelopmentConfig')

    flask_app.register_blueprint(users, url_prefix="/users")
    return flask_app


app = app_factory(APP_NAME)


@app.errorhandler(HTTPException)
def not_found(error):
    return jsonify({
        "code": error.code,
        "error": error.name,
        "description": error.description
    }), error.code


if __name__ == '__main__':
    app.run()
