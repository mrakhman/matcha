import http
from functools import wraps

from flask import session, g, abort, jsonify


def authorised_only(f):
    @wraps(f)
    def internal(*args, **kwargs):
        # current_user_id = session.get('user_id')
        # if current_user_id and type(current_user_id) == int:
        #     current_user = User.get_by_id(current_user_id)
        #     if current_user:
        #         g.current_user = current_user
        if getattr(g, 'current_user'):
            return f(*args, **kwargs)
        abort(http.HTTPStatus.UNAUTHORIZED)
    return internal
