import logging

import click
from flask import Flask, g, jsonify, session
from flask import request
from flask.cli import AppGroup, with_appcontext
from flask.logging import default_handler
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, abort

from models.user import User
from modules import db, mail, redis_client, serializer, storage
from tree import auth, history, images, likes, messages, notifications, recovery, settings, users
from utils.json_encoder import CustomJSONEncoder

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
    flask_app.config.from_pyfile('configs.cfg')

    flask_app.json_encoder = CustomJSONEncoder

    db.init_app(flask_app)
    mail.init_app(flask_app)
    redis_client.init_app(flask_app)
    serializer.init_app(flask_app)
    storage.init_app(flask_app)

    # Create a bucket if not already created
    with flask_app.app_context():
        if not storage.connection.bucket_exists(flask_app.config['IMAGES_BUCKET_NAME']):
            flask_app.logger.info(f"Creating images bucket: {flask_app.config['IMAGES_BUCKET_NAME']}")
            storage.connection.make_bucket(flask_app.config['IMAGES_BUCKET_NAME'])

    flask_app.register_blueprint(auth, url_prefix="/auth")
    flask_app.register_blueprint(history, url_prefix="/history")
    flask_app.register_blueprint(images, url_prefix="/images")
    flask_app.register_blueprint(likes, url_prefix="/likes")
    flask_app.register_blueprint(messages, url_prefix="/messages")
    flask_app.register_blueprint(notifications, url_prefix="/notifications")
    flask_app.register_blueprint(recovery, url_prefix="/recovery")
    flask_app.register_blueprint(settings, url_prefix="/settings")
    flask_app.register_blueprint(users, url_prefix="/users")

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


@app.before_request
def track_last_connection():
    g.current_user = None
    current_user_id = session.get('user_id')
    if current_user_id and type(current_user_id) == int:
        current_user = User.get_by_id(current_user_id)
        if current_user:
            g.current_user = current_user
            g.current_user.made_request()


@app.route('/')
def root_handler():
    return "Hello World!"


@app.route('/teapot')
def teapot():
    abort(418)


@app.route('/health')
def health():
    return "OK"


db_cli = AppGroup('db')


@db_cli.command('init')
@with_appcontext
def init_db():
	db.init_db(app)


@db_cli.command('populate')
@click.argument('amount', type=click.INT)
@with_appcontext
def populate(amount):
	from populate import RandomUser
	params = {
		'results': amount,
		'nat': 'fr',
	}
	RandomUser().create_users(**params)


app.cli.add_command(db_cli)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
else:
    # We are probably inside gunicorn
    import logging
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
