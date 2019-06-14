import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    PSQL_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    PSQL_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "HelloWorld!"
    PSQL_DATABASE_URI = os.getenv('DB_URI')
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")


class TestingConfig(Config):
    TESTING = True
