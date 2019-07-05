from datetime import datetime
from .model import Model, Queries


class LikeQueries(Queries):
    def __init__(self):
        self.create = self.query("INSERT INTO likes (f_party, s_party, f2s, s2f) VALUES ($1, $2, $3, $4)")
        self.update = lambda field: \
            self.query(f"UPDATE likes SET {field} = $3 WHERE f_party = $1 AND s_party = $2") if field in ('f2s', 's2f') else None
        self.get = self.query("SELECT * FROM likes WHERE f_party = $1 AND s_party = $2", one=True)
        self.able_to_like = self.query("SELECT profile_image FROM users WHERE profile_image IS NOT NULL AND id = $1")
        # self.get_user_likes = self.query("SELECT * FROM likes WHERE user_id = $1")
        # self.delete = self.query("DELETE FROM tags_array WHERE user_id = $1")


class Like(Model):
    _fields = {
        'f_party': {
            'required': True,
            'default': None,
            'type': int,
            'validator': None
        },
        's_party': {
            'required': True,
            'default': None,
            'type': int,
            'validator': None
        },
        'f2s': {
            'required': True,
            'default': False,
            'type': bool,
            'validator': None
        },
        's2f': {
            'required': True,
            'default': False,
            'type': bool,
            'validator': None
        }
    }

    _views = {
        'public': {
            'fields': [
                'f_party',
                's_party',
                'f2s',
                's2f'
            ]
        }
    }

    _update_watch_fields = ()

    queries = LikeQueries()


    @classmethod
    def _create(cls, user1: int, user2: int, f2s: bool, s2f: bool):
        if user1 == user2:
            return
        if user1 > user2:
            return cls._create(user2, user1, s2f, f2s)
        cls.queries.create(user1, user2, f2s, s2f)

    @classmethod
    def _set_state(cls, liker: int, likee: int, value: bool):
        if liker > likee:
            cls.queries.update('s2f')(likee, liker, value)
        elif liker < likee:
            cls.queries.update('f2s')(liker, likee, value)

    def _self_update(self, field: str, value: bool):
        self.queries.update(field)(self.f_party, self.s_party, value)

    @classmethod
    def get(cls, user1, user2):
        f_party, s_party = sorted((user1, user2))
        result = cls.queries.get(f_party, s_party)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    @classmethod
    def like(cls, liker, likee):
        if liker == likee:
            return
        like_entry = cls.get(liker, likee)
        if like_entry:
            cls._set_state(liker, likee, True)
        else:
            cls._create(liker, likee, True, False)

    @classmethod
    def unlike(cls, liker, likee):
        if liker == likee:
            return
        like_entry = cls.get(liker, likee)
        if like_entry:
            cls._set_state(liker, likee, False)
        else:
            cls._create(liker, likee, False, False)

    @classmethod
    def is_liked(cls, liker, likee):
        like = cls.get(liker, likee)
        if not like:
            return False
        if liker < likee:
            return like.f2s
        return like.s2f

    @classmethod
    def able_to_like(cls, user_id):
        result = cls.queries.able_to_like(user_id)
        if not result:
            return False
        return True


