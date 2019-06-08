import random
from datetime import date, timedelta
from typing import Optional

from werkzeug.security import generate_password_hash, \
    check_password_hash

from utils.images import get_dog_image
from .model import Model, Queries

temp_users = {}  # @TODO: rm


class UserQueries(Queries):
    def __init__(self):
        self.get_all = self.query("SELECT * FROM users")
        self.create = self.query("INSERT INTO users(username, email, first_name, last_name, password) "
                                 "VALUES ($1, $2, $3, $4, $5) RETURNING id")
        # self.get_by_username = self.query("SELECT * FROM users WHERE username = $1", one=True)
        self.get_by_unique_field = lambda column: self.query(f"SELECT * FROM users WHERE {column} = $1", one=True)


class User(Model):
    _fields = {
        'id': {
            'required': False,
            'default': None,
            'type': int,
            'validator': None
        },
        'first_name': {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        },
        'last_name': {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        },
        'username': {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        },
        'email': {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        },
        'dob': {
            'required': False,
            'default': None,
            'type': date,
            'validator': lambda _: _ and date.today() - timedelta(365 * 120) < _ < date.today()
            # Age between ~ 120y and 0
        },
        'bio_text': {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        'gender': {
            'required': False,
            'default': 'not mention',
            'type': str,
            'validator': lambda _: _ in ['female', 'male', 'not mention']
        },
        'sex_pref': {
            'required': False,
            'default': 'bi',
            'type': str,
            'validator': lambda _: _ in ['homo', 'hetero', 'bi']
        },
        'tags': {
            'required': False,
            'default': [],
            'type': dict,
            'validator': None
        },
        'profile_image': {
            'required': False,
            'default': "",
            'type': str,
            'validator': None
        },
        'password': {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        }
    }

    _views = {
        'personal': {
            'fields': [
                'id',
                'first_name',
                'last_name',
                'email',
                'dob',
                'bio_text',
                'gender',
                'sex_pref',
                'tags',
                'profile_image',
                'username'
            ]
        },
        'public': {
            'fields': [
                'id',
                'first_name',
                'last_name',
                'age',
                'bio_text',
                'gender',
                'sex_pref',
                'tags',
                'profile_image',
                'username'
            ]
        }
    }

    queries = UserQueries()

    @property
    def age(self):
        if not getattr(self, 'dob'):
            return None
        today = date.today()
        age = today.year - getattr(self, 'dob').year
        if today.month < getattr(self, 'dob').month \
                or (today.month == getattr(self, 'dob').month and today.day < getattr(self, 'dob').day):
            age -= 1
        return age

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @classmethod
    def from_db(cls, obj_id: int):
        # TODO: remove nahui
        import names
        if obj_id > 1000:
            return None

        if obj_id in temp_users:
            return temp_users[obj_id]

        obj = cls()
        obj.id = obj_id
        obj.gender = random.choice(['female', 'male'])
        obj.first_name = names.get_first_name(obj.gender)
        obj.last_name = names.get_last_name()
        obj.username = obj.first_name[0] + obj.last_name
        obj.username = obj.username.lower()
        obj.email = obj.username + '@example.com'
        obj.dob = date.today() - timedelta(random.randint(365 * 20, 365 * 30))
        obj.sex_pref = random.choice(['homo', 'hetero', 'bi'])
        obj.profile_image = get_dog_image()
        password = f"_{obj.id}"
        obj.set_password(password)
        temp_users[obj_id] = obj
        return obj

    @classmethod
    def _get_by_unique_field(cls, column: str, value) -> Optional['User']:
        result = cls.queries.get_by_unique_field(column)(value)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    @classmethod
    def get_by_username(cls, username: str):
        return cls._get_by_unique_field('username', username)

    @classmethod
    def get_by_email(cls, email: str):
        return cls._get_by_unique_field('email', email)

    @classmethod
    def get_by_id(cls, user_id: int):
        return cls._get_by_unique_field('id', user_id)

    def create(self):
        # @TODO: Check smth?
        self.queries.create(getattr(self, 'username'), getattr(self, 'email'), getattr(self, 'first_name'), getattr(self, 'last_name'), getattr(self, 'password'))
