import http

from flask import blueprints, jsonify, session, request, abort, current_app

from models.user import User
from utils.form_validator import check_fields

auth = blueprints.Blueprint("auth", __name__)


@auth.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    form_values = {
        "username": {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        },
        "password": {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        }
    }
    current_app.logger.info(f"Here we are, the request is: {req_data}")
    check_fields(req_data, form_values)

    current_user = User.get_by_username(req_data["username"])

    if current_user.activated is not True:
        abort(http.HTTPStatus.FORBIDDEN)

    if current_user and current_user.check_password(req_data["password"]):
        session['user_id'] = current_user.id
        return jsonify({'status': 'ok'})
    abort(http.HTTPStatus.UNAUTHORIZED)


@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'user_id' in session:
        del session['user_id']
    return jsonify({'status': 'ok'})
