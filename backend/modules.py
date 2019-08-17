from flask_mail import Mail
from flask_minio import Minio
from flask_redis import FlaskRedis

from flask_postgres import Postgres
from utils.token_serializer import MySerializer

db = Postgres()
mail = Mail()
redis_client = FlaskRedis()
serializer = MySerializer()
storage = Minio()
