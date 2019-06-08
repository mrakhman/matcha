import http

from flask import blueprints, jsonify, session, request, abort, current_app

from models.user import User
from utils.form_validator import check_fields

auth = blueprints.Blueprint("auth", __name__)


# @auth.route('/login', methods=['POST'])
# def pseudo_login():
#     # TODO: if not json -> fail silently
#     login = request.json.get('username')
#     pw = request.json.get('password')
#     if not (login and pw and login.isdigit()):
#         abort(http.HTTPStatus.BAD_REQUEST)
#
#     # TODO: For now login = user_id. To be changed later
#     login = int(login)
#     current_user = User.from_db(login)
#     if current_user and current_user.check_password(pw):
#         session['user_id'] = current_user.id
#         return jsonify({'status': 'ok'})
#     abort(http.HTTPStatus.UNAUTHORIZED)


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

    if current_user and current_user.check_password(req_data["password"]):
        session['user_id'] = current_user.id
        return jsonify({'status': 'ok'})
    abort(http.HTTPStatus.UNAUTHORIZED)


@auth.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'user_id' in session:
        del session['user_id']
    return jsonify({'status': 'ok'})


# @auth.route('/whoami', methods=['GET'])
# def whoami():
#     context = {}
#     current_user_id = session.get('user_id')
#     if current_user_id:
#         current_user = User.from_db(int(current_user_id))
#         if current_user:
#             context = {
#                 'first_name': current_user.first_name,
#                 'last_name': current_user.last_name,
#                 'username': current_user.username
#             }
#     return jsonify({
#         'user_id': session.get('user_id'),
#         'context': context
#     })
