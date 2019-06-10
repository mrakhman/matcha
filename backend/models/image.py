from .model import Model, Queries


class ImageQueries(Queries):
    def __init__(self):
        self.update_profile_image = self.query("INSERT INTO users (profile_image) VALUES ($1)")
        self.update_user_images = self.query("INSERT INTO images (image_src) VALUES ($1)")
        self.get_profile_image = self.query("SELECT profile_image FROM users WHERE id = $1", one=True)
        self.get_user_images = self.query("SELECT * FROM images WHERE user_id = $1")


class Images(Model):
    _fields = {
        'first_name': {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        }
    }

    _views = {
        'personal': {
            'fields': [
                'id',
                'first_name',
                'last_name',
                'dob',
                'bio_text',
                'gender',
                'sex_pref',
                'tags',
                'profile_image',
                'username'
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
                'username'
            ]
        }
    }

    def get_profile_image(self, user_id):
        self.queries.get_profile_image(user_id)
