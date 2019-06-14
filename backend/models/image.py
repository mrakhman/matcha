from .model import Model, Queries

UPLOAD_FOLDER = 'img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

class ImageQueries(Queries):
    def __init__(self):
        self.update_profile_image = self.query("INSERT INTO users (profile_image) VALUES ($1)")
        self.update_user_images = self.query("INSERT INTO images (image_src) VALUES ($1, $2)")
        self.get_profile_image = self.query("SELECT profile_image FROM users WHERE id = $1", one=True)
        self.get_user_images = self.query("SELECT * FROM images WHERE user_id = $1")


class Image(Model):
    _fields = {
        'id': {
            'required': False,
            'default': None,
            'type': int,
            'validator': None
        },
        'user_id': {
            'required': False,
            'default': None,
            'type': int,
            'validator': None
        },
        'image_src': {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        'profile_image': {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        'form_data': {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        'filename': {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        }
    }

    _views = {
        'user_images': {
            'fields': [
                'id',
                'user_id',
                'image_src'
            ]
        },
        'profile_image': {
            'fields': [
                'id',
                'profile_image'
            ]
        }
    }

    queries = ImageQueries()

    

    # @classmethod
    # def get_profile_image(cls, user_id):
    #     result = cls.queries.get_profile_image(user_id)
    #     if not result:
    #         return None
    #     obj = cls.from_db_row(result)
    #     return obj

    @classmethod
    def get_user_images(cls, user_id):
        result = cls.queries.get_user_images(user_id)
        if not result:
            return None
        obj = cls.from_db_row(result)
        return obj

    def add_user_image(self, user_id, image_src):
        self.queries.update_user_images(user_id, image_src)

