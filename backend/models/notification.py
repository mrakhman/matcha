from datetime import datetime

from flask import json

from my_redis import redis_client
from .model import Model, Queries
from .user import User


class NotificationQueries(Queries):
    def __init__(self):
        self.create = self.query("INSERT INTO notifications (user_id, text, type) VALUES ($1, $2, $3) RETURNING id")
        self.get_user_notifications = self.query("SELECT * FROM notifications WHERE user_id = $1 AND is_read = FALSE "
                                                 "ORDER BY created_at DESC LIMIT 50")
        self.get_by_id = self.query("SELECT * FROM notifications WHERE id = $1", one=True)
        self.update_field = lambda field: self.query(f"UPDATE notifications SET {field} = $1 WHERE id = $2")
        self.mark_all_read = self.query("UPDATE notifications SET is_read = true WHERE user_id = $1")


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
        'is_read': {
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
        },
        'type': {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        }
    }

    _views = {
        'public': {
            'fields': {
                'id',
                'user_id',
                'is_read',
                'text',
                'created_at',
                'type'
            }
        }
    }

    _update_watch_fields = ('is_read',)

    queries = NotificationQueries()

    # @property
    # def created_at(self):
    #     if not getattr(self, 'created_at'):
    #         return None
    #     created_at = datetime.fromtimestamp(self.created_at)
    #     return created_at

    @classmethod
    def get_user_notifications(cls, user_id):
        result = cls.queries.get_user_notifications(user_id)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    def create(self):
        result = self.queries.create(self.user_id, self.text, self.type)
        self.id = result[0][0]
        redis_payload = self.get_view()
        redis_client.publish(f"notifications_{self.user_id}", json.dumps(redis_payload))

        # self.queries.create(getattr(self, 'user_id'), getattr(self, 'text'))

    def _update_field(self, field, value):
        self.queries.update_field(field)(value, self.id)

    @staticmethod
    def notification_text(notif_type, sender_id):
        sender_user = User.get_by_id(sender_id)
        sender_username = sender_user.username
        if notif_type == 'like':
            text = sender_username + " liked your profile"
            return text
        if notif_type == 'unlike':
            text = sender_username + " unliked your profile"
            return text
        if notif_type == 'view':
            text = sender_username + " viewed your profile"
            return text
        if notif_type == 'message':
            text = sender_username + " sent you a message"
            return text

    @classmethod
    def mark_all_read(cls, user_id):
        cls.queries.mark_all_read(user_id)
        return True


