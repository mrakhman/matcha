from datetime import date, timedelta
from typing import Optional

from werkzeug.security import generate_password_hash, check_password_hash

from .model import Model, Queries


class UserQueries(Queries):
    def __init__(self):
        self.get_all = self.query("SELECT * FROM users")
        self.create = self.query("INSERT INTO users (username, email, first_name, last_name, password) "
                                 "VALUES ($1, $2, $3, $4, $5) RETURNING id")
        self.get_by_unique_field = lambda field: self.query(f"SELECT * FROM users WHERE {field} = $1", one=True)
        self.update_field = lambda field: self.query(f"UPDATE users SET {field} = $1 WHERE id = $2")

        self.filter = lambda order_by, order_by_field: self.query(f"""
            SELECT * FROM users 
            WHERE date_part('year', age(dob)) BETWEEN $1 AND $2 
            AND rating BETWEEN $3 AND $4
            AND gender = ANY($5)
            AND sex_pref = ANY($6)
            AND tags @> $7
            ORDER BY {order_by_field} {order_by}
            LIMIT $8 OFFSET $9
            """)
        self.count = self.query("""
            SELECT COUNT(*) FROM users 
            WHERE date_part('year', age(dob)) BETWEEN $1 AND $2
            AND rating BETWEEN $3 AND $4
            AND gender = ANY($5)
            AND sex_pref = ANY($6)
            AND tags @> $7
            """)


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
            'validator': lambda _: _ and date.today() - timedelta(365 * 99) < _ < date.today()
            # Age between ~ 99y and 0
        },
        'bio_text': {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        'gender': {
            'required': False,
            'default': None,
            'type': str,
            'validator': lambda _: _ in ['female', 'male']
        },
        'sex_pref': {
            'required': False,
            'default': 'bi',
            'type': str,
            'validator': lambda _: _ in ['homo', 'hetero', 'bi']
        },
        'tags': {
            'required': False,
            'default': None,
            'type': [],
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
        },
        'rating': {
            'required': False,
            'default': None,
            'type': int,
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
                'username',
                'rating'
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
                'username',
                'rating'
            ]
        }
    }

    _update_watch_fields = (
        'gender', 'sex_pref', 'dob', 'bio_text',
        'first_name', 'last_name', 'username',
        'email', 'profile_image', 'tags', 'password'
    )

    queries = UserQueries()

    @property
    def age(self):
        if not getattr(self, 'dob'):
            return None
        today = date.today()
        age = today.year - self.dob.year
        if today.month < self.dob.month \
                or (today.month == self.dob.month and today.day < self.dob.day):
            age -= 1
        return age

    @property
    def opposite_gender(self):
        if not getattr(self, 'gender'):
            return None
        return {'male': 'female', 'female': 'male'}[self.gender]

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

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

    @classmethod
    def get_filtered(
            cls, *,
            age_min, age_max, rating_min, rating_max,
            gender, sex_pref, my_tags, selected_tags, order_by_field, order_by,
            limit, offset):
        reversed_order = {'ASC': 'DESC', 'DESC': 'ASC'}
        args = [age_min, age_max, rating_min, rating_max, gender, sex_pref, selected_tags, limit, offset]
        if order_by_field == 'my_tags':
            order_by_field = 'count_intersect($10, tags)'
            order_by = reversed_order[order_by]
            args.append(my_tags)
        elif order_by_field == 'tags':
            order_by_field = 'count_intersect($7, tags)'
        elif order_by_field == 'age':
            order_by_field = 'dob'
            order_by = reversed_order[order_by]
        print(f"order_by: {order_by}, order_by_field: {order_by_field}")
        result = cls.queries.filter(order_by, order_by_field)(
            *args
        )
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    @classmethod
    def count_filtered(cls, *, age_min, age_max, rating_min, rating_max, gender, sex_pref, selected_tags, **kwargs):
        result = cls.queries.count(age_min, age_max, rating_min, rating_max, gender, sex_pref, selected_tags)
        if not result:
            return 0
        return result[0][0]

    def create(self):
        # @TODO: Check smth?
        self.queries.create(getattr(self, 'username'), getattr(self, 'email'), getattr(self, 'first_name'),
                            getattr(self, 'last_name'), getattr(self, 'password'))
        # @TODO: get id from request, set it to the model attribute

    def _update_field(self, field, value):
        self.queries.update_field(field)(value, self.id)
