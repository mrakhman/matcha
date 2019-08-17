import http
from functools import wraps

from flask import g, abort


def authorised_only(f):
    @wraps(f)
    def internal(*args, **kwargs):
        if getattr(g, 'current_user'):
            return f(*args, **kwargs)
        abort(http.HTTPStatus.UNAUTHORIZED)
    return internal
