from datetime import datetime
from .model import Model, Queries


class LikeQueries(Queries):
    def __init__(self):
        self.get_user_tags = self.query("SELECT * FROM tags_array WHERE user_id = $1")
        self.create = self.query("INSERT INTO tags_array (user_id, tags) VALUES ($1, $2)")
        self.update = self.query("UPDATE tags_array SET tags = $2 WHERE user_id = $1")
        # self.delete = self.query("DELETE FROM tags_array WHERE user_id = $1")


class Like(Model):
    _fields = {
        'user_id': {
            'required': False,
            'default': None,
            'type': int,
            'validator': None
        },
        'tags': {
            'required': False,
            'default': None,
            'type': [],
            'validator': None
        }
    }

    _views = {
        'public': {
            'fields': [
                'user_id',
                'tags'
            ]
        }
    }

    _update_watch_fields = ()

    queries = LikeQueries()

    @classmethod
    def get_user_tags(cls, user_id):
        result = cls.queries.get_user_tags(user_id)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    def create(self, user_id):
        self.queries.create(user_id, getattr(self, 'tags'))

    def update(self, user_id):
        self.queries.update(user_id, getattr(self, 'tags'))

    # def delete(self, user_id):
    #     self.queries.delete(user_id)
