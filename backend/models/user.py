import random

from .model import Model
from datetime import date, timedelta

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
        }
    }

    _views = {
        'personal': {
            'fields': [
                'first_name',
                'last_name',
                'birthday',
                'bio_text',
                'gender',
                'sex_pref',
                'tags'
            ]
        },
        'public': {
            'fields': [
                'first_name',
                'last_name',
                'age',
                'bio_text',
                'gender',
                'sex_pref',
                'tags'
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

    @classmethod
    def from_db(cls, obj_id):
        # TODO
        import names
        if obj_id > 100:
            return None

        if obj_id in temp_users:
            return temp_users[obj_id]

        obj = cls()
        obj.id = obj_id
        obj.gender = random.choice(['female', 'male'])
        obj.first_name = names.get_first_name(obj.gender)
        obj.last_name = names.get_last_name()
        obj.birthday = date.today() - timedelta(random.randint(365 * 20, 365 * 30))
        obj.sex_pref = random.choice(['homo', 'hetero', 'bi'])
        temp_users[obj_id] = obj
        return obj
