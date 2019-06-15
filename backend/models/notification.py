from datetime import datetime

from .model import Model, Queries


class NotificationQueries(Queries):
    def __init__(self):
        self.create = self.query("INSERT INTO notifications (user_id, text) VALUES ($1, $2) RETURNING id")
        self.get_user_notifications = self.query("SELECT * FROM notifications WHERE user_id = $1")
        self.get_by_id = self.query("SELECT * FROM notifications WHERE id = $1", one=True)
        self.update_field = lambda field: self.query(f"UPDATE notifications SET {field} = $1 WHERE id = $2")


class Notification(Model):
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
        'read': {
            'required': False,
            'default': False,
            'type': bool,
            'validator': None
        },
        'text': {
            'required': True,
            'default': None,
            'type': str,
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
                'read',
                'text',
                'created_at'
            ]
        }
    }

    _update_watch_fields = ('read',)

    queries = NotificationQueries()

    @classmethod
    def get_by_id(cls, notification_id):
        result = cls.queries.get_by_id(notification_id)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    @classmethod
    def get_user_notifications(cls, user_id):
        result = cls.queries.get_user_notifications(user_id)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    def create(self):
        self.queries.create(self.user_id, self.text)

    def _update_field(self, field, value):
        self.queries.update_field(field)(value, self.id)

