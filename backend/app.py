import logging

from flask import Flask, jsonify
from flask import request
from flask.logging import default_handler
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, abort

from db import db
from tree import auth, images, notifications, users, tags, likes
from utils.json_encoder import CustomJSONEncoder
from mail import mail
# from signature import signature

APP_NAME = "matcha"


# Logging
class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)


formatter = RequestFormatter(
    '|||[ART]||| [%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)


def app_factory(name):
    flask_app = Flask(name)
    flask_app.config.from_object('config.DevelopmentConfig')
    flask_app.json_encoder = CustomJSONEncoder
    db.init_app(flask_app)

    # # Mail here
    flask_app.config.update(dict(
        DEBUG=True,
        MAIL_SERVER='smtp.yandex.ru',
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='matcha@coffeebreak42.cf',
        MAIL_PASSWORD='matcha',
        SECRET_KEY='kukushka',
        SECURITY_SALT='what_is_salt'
    ))
    mail.init_app(flask_app)
    # signature.init_app(flask_app)  # TODO: Artem, do I need this line and this import?

    flask_app.register_blueprint(auth, url_prefix="/auth")
    flask_app.register_blueprint(images, url_prefix="/images")
    flask_app.register_blueprint(notifications, url_prefix="/notifications")
    flask_app.register_blueprint(users, url_prefix="/users")
    flask_app.register_blueprint(tags, url_prefix="/tags")
    flask_app.register_blueprint(likes, url_prefix="/likes")

    CORS(flask_app, supports_credentials=True)
    return flask_app


app = app_factory(APP_NAME)


@app.errorhandler(HTTPException)
def not_found(error):
    return jsonify({
        "code": error.code,
        "error": error.name,
        "description": error.description
    }), error.code


@app.route('/')
def root_handler():
    return "Hello World!"


@app.route('/teapot')
def teapot():
    abort(418)


if __name__ == '__main__':
    app.run()
