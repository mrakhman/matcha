from .model import Model, Queries


class ImageQueries(Queries):
    def __init__(self):
        self.update_profile_image = self.query("INSERT INTO users (profile_image) VALUES ($1)")
        self.create = self.query("INSERT INTO images (user_id, image_src) VALUES ($1, $2)")
        self.get_profile_image = self.query("SELECT profile_image FROM users WHERE id = $1", one=True)
        self.get_user_images = self.query("SELECT * FROM images WHERE user_id = $1")
        self.delete = self.query("DELETE FROM images WHERE user_id = $1 AND id = $2")


class Image(Model):
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
        'image_src': {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        }
    }

    _views = {
        'public': {
            'fields': [
                'id',
                'user_id',
                'image_src'
            ]
        }
    }

    _update_watch_fields = ()

    queries = ImageQueries()

    @classmethod
    def get_user_images(cls, user_id):
        result = cls.queries.get_user_images(user_id)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    def create(self):
        self.queries.create(self.user_id, self.image_src)

    @classmethod
    def delete(cls, user_id, del_img_id):
        cls.queries.delete(user_id, del_img_id)

    # def delete(self):
    #     self.queries.delete(self.user_id, getattr(self, 'image_src'))
