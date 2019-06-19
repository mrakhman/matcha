from datetime import datetime
from .model import Model, Queries


class TagQueries(Queries):
    def __init__(self):
        self.create = self.query("INSERT INTO tags_array (user_id, tags) VALUES ($1, $2)")
        self.get_user_tags = self.query("SELECT * FROM user_tags WHERE user_id = $1")
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

    _update_watch_fields = ()

    queries = TagQueries()

    @classmethod
    def get_user_tags(cls, user_id):
        result = cls.queries.get_user_tags(user_id)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    def create(self):
        self.queries.create(self.user_id, self.tags)

    def delete(self):
        self.queries.delete(self.id)
