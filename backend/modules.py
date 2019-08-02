from flask_mail import Mail
from flask_redis import FlaskRedis

from flask_postgres import Postgres
from serializer import MySerializer

db = Postgres()
redis_client = FlaskRedis()
mail = Mail()
serializer = MySerializer()
