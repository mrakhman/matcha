from flask import blueprints, jsonify, abort, current_app, session, request

from models.user import User
from utils.form_validator import check_fields

users = blueprints.Blueprint("users", __name__)


@users.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    current_app.logger.info(f"Getting user #{user_id}")
    user = User.get_by_id(user_id)
    if user:
        return jsonify(user.get_view("public"))

    abort(404)


@users.route('/page/<int:page_number>', methods=['GET'])
def get_users_page(page_number):
    if page_number < 0:
        page_number = 0

    users = [User.get_by_id(i).get_view("public") for i in range(1 + 10 * page_number, 11 + 10 * page_number)]
    return jsonify({"users": users})


@users.route('/me', methods=['GET'])
def get_me():
    current_user_id = session.get('user_id')
    if current_user_id:
        current_user = User.get_by_id(int(current_user_id))
        if current_user:
            return jsonify({"user": current_user.get_view('personal')})
    abort(401)


@users.route('/register', methods=['POST'])
def create_user():
    # first_name = request.json.get("first_name")
    # last_name = request.json.get("last_name")
    # email = request.json.get("email")
    # username = request.json.get("username")
    # password = request.json.get("password")
    req_data = request.get_json()
    form_values = {
        "first_name": {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        },
        "last_name": {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        },
        "email": {
            'required': True,
            'default': None,
            'type': str,
            'validator': lambda x: '@' in x[1:-1]
        },
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
    new_user = User.from_dict(req_data)
    new_user.set_password(req_data["password"])
    # new_user.set_password('test')  # @TODO: rm
    new_user.create()
    return jsonify({"ok": True, "user": new_user.get_view("public")})


@users.route('/all', methods=['GET'])
def get_all2():
    user_rows = User.queries.get_all()
    result = User.from_db_row(user_rows)
    return jsonify(result)


@users.route('/create', methods=['GET'])
def create_many():
    u = User.from_db(1)
    u.create()
    return jsonify({"ok": True})


@users.route('/edit_profile', methods=['POST'])
def add_personal_details():
    req_data = request.get_json()
    form_values = {
        "gender": {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        "sex_pref": {
            'required': False,
            'default': 'bi',
            'type': str,
            'validator': None
        },
        "bio_text": {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        "profile_image": {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        "photos": {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        "tags": {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        "dob": {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        }
    }
    current_app.logger.info(f"Here we are, the request is: {req_data}")
    check_fields(req_data, form_values)
    current_user = User.get_by_username(session['user_id'])

    if current_user:
        for field, val in req_data.items():
            User.update_field(field, val)

        return jsonify({"ok": True})


    # new_user = User.from_dict(req_data)
    # new_user.set_password(req_data["password"])
    # new_user.create()
    # return jsonify({"ok": True, "user": new_user.get_view("public")})
