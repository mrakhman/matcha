import random

from utils.images import get_dog_image
from .model import Model
from datetime import date, timedelta

from werkzeug.security import generate_password_hash, \
     check_password_hash

temp_users = {}


class User(Model):
    _fields = {
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
        'birthday': {
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
        'pw_hash': {
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
                'birthday',
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

    @property
    def age(self):
        if not getattr(self, 'birthday'):
            return None
        today = date.today()
        age = today.year - getattr(self, 'birthday').year
        if today.month < getattr(self, 'birthday').month \
                or (today.month == getattr(self, 'birthday').month and today.day < getattr(self, 'birthday').day):
            age -= 1
        return age

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    @classmethod
    def from_db(cls, obj_id: int):
        # TODO
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
        obj.birthday = date.today() - timedelta(random.randint(365 * 20, 365 * 30))
        obj.sex_pref = random.choice(['homo', 'hetero', 'bi'])
        obj.profile_image = get_dog_image()
        password = f"_{obj.id}"
        obj.set_password(password)
        temp_users[obj_id] = obj
        return obj

    def create(self):
        self.id = 1
        while self.id in temp_users:
            self.id += 1

        temp_users[self.id] = self
