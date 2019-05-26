from .model import Model


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
