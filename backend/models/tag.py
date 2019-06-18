from datetime import datetime
from .model import Model, Queries


class TagQueries(Queries):
    def __init__(self):
        self.create = self.query("INSERT INTO user_tags (user_id, tag_id) VALUES ($1, $2)")
        self.get_user_tags = self.query("SELECT * FROM user_tags WHERE user_id = $1 AND $tag_id = $2")
        # self.get_by_id = self.query("SELECT * FROM notifications WHERE id = $1", one=True)
        self.delete = self.query("DELETE FROM user_tags WHERE user_id = $1 AND $tag_id = $2")


class Tag(Model):
    _fields = {
        'user_id': {
            'required': False,
            'default': None,
            'type': int,
            'validator': None
        },
        'tag_id': {
            'required': True,
            'default': None,
            'type': int,
            'validator': None
        }
    }

    _views = {
        'public': {
            'fields': [
                'user_id',
                'tag_id',
            ]
        }
    }

