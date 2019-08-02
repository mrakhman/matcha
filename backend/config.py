import os

from flask_dotenv import DotEnv


class Config(object):
    DEBUG = False
    TESTING = False

    @classmethod
    def init_app(cls, app):
        env = DotEnv()
        env.init_app(app)

        env.eval(keys={
            'DEBUG': bool,
            'MAIL_PORT': int,
            'MAIL_USE_TLS': bool,
            'MAIL_USE_SSL': bool,
        })


class DevelopmentConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")


class TestingConfig(Config):
    TESTING = True
