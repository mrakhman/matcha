from datetime import datetime, date, timedelta


from .model import Model, Queries
from .user import User


class HistoryQueries(Queries):
    def __init__(self):
        self.add_to_history = self.query("INSERT INTO history (user_id, profile_id) "
                                         "VALUES ($1, $2) RETURNING id")

        # Insert username as foreign value by profile_id; assign use_id and profile_id to foreign key

        self.get_user_history = self.query("SELECT * FROM history WHERE user_id = $1 ORDER BY created_at DESC")
        self.delete_history = self.query("DELETE FROM history WHERE user_id = $1")


class History(Model):
    _fields = {
        'id': {
            'required': False,
            'default': None,
            'type': int,
            'validator': None
        },
        'user_id': {
            'required': True,
            'default': None,
            'type': int,
            'validator': None
        },
        'profile_id': {
            'required': True,
            'default': None,
            'type': int,
            'validator': None
        },
        'created_at': {
            'required': False,
            'default': None,
            'type': datetime,
            'validator': None
        }
    }

    _views = {
        'public': {
            'fields': [
                'id',
                'user_id',
                'profile_id',
                'created_at'
            ]
        }
    }

    _update_watch_fields = ()

    queries = HistoryQueries()

    @classmethod
    def add_to_history(cls, user_id, profile_id):
        cls.queries.add_to_history(user_id, profile_id)

    @classmethod
    def get_user_history(cls, user_id):
        result = cls.queries.get_user_history(user_id)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    @classmethod
    def delete_history(cls, user_id):
        cls.queries.delete_history(user_id)
        return True
