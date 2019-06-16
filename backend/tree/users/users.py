import datetime
import http

from flask import blueprints, jsonify, abort, current_app, session, request, g, redirect, url_for

from models.user import User
from models.image import Image
from utils.form_validator import check_fields
from utils.security import authorised_only

users = blueprints.Blueprint("users", __name__)


@users.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    current_app.logger.info(f"Getting user #{user_id}")
    user = User.get_by_id(user_id)
    if user:
        payload = user.get_view("public")
        if request.args.get('with_images'):
            user_images = Image.get_user_images(user.id)
            payload['images'] = []
            if user_images:
                payload['images'] = [i.image_src for i in user_images]
        return jsonify(user=payload)
    abort(404)


@users.route('/filter', methods=['POST'])
@users.route('/filter/page', methods=['POST'])
def user_filter_default():
    return redirect(url_for('users.users_filter', page_number=0, _method='POST'))


@users.route('/filter/page/<int:page_number>', methods=['POST'])
@authorised_only
def users_filter(page_number):
    """
    :param page_number: page number
    :request -> {
        "filter": {
            "age": {"min": 0, "max": 99},
            "rating": {"min": 0, "max": 10},
            "distance": {"min": 0, "max": 100}
        },
        "sort": {
            "order_by": "asc" (def) | "desc",
            "sort_by": "id" (def) | "age", "rating", "distance"
        }
    }
    :return:
    """
    PER_PAGE = 20
    if page_number < 0:
        page_number = 0
    req_data: dict = request.get_json()
    if not req_data:
        abort(http.HTTPStatus.BAD_REQUEST)
    # Filter
    filter_validation = {
        "min": {
            'required': False,
            'default': 0,
            'type': int,
            'validator': None
        },
        "max": {
            'required': False,
            'default': 0,
            'type': int,
            'validator': None
        },
    }
    req_data.setdefault("filter", {})
    req_data["filter"].setdefault("age", {})
    req_data["filter"].setdefault("rating", {})
    req_data["filter"].setdefault("distance", {})
    # Age
    filter_validation["max"]["default"] = 99
    check_fields(req_data["filter"]["age"], filter_validation)
    # Rating
    filter_validation["max"]["default"] = 10
    check_fields(req_data["filter"]["rating"], filter_validation)
    # Distance
    filter_validation["max"]["default"] = 100
    check_fields(req_data["filter"]["distance"], filter_validation)

    # Sort
    req_data.setdefault("sort", {})
    req_data["sort"].setdefault("order_by", "asc")
    req_data["sort"].setdefault("sort_by", "id")
    if req_data["sort"]["order_by"] not in ("asc", "desc"):
        abort(http.HTTPStatus.BAD_REQUEST)
    if req_data["sort"]["sort_by"] not in ("id", "age", "distance", "rating"):
        abort(http.HTTPStatus.BAD_REQUEST)
    # Here we are with all data valid

    search_users = []
    payload = {
        'age_min': req_data['filter']['age']['min'],
        'age_max': req_data['filter']['age']['max'],
        'rating_min': req_data['filter']['rating']['min'],
        'rating_max': req_data['filter']['rating']['max'],
        'order_by_field': req_data['sort']['sort_by'].upper(),
        'order_by': req_data['sort']['order_by'].upper(),
        'limit': PER_PAGE,
        'offset': PER_PAGE * page_number
    }
    if g.current_user.sex_pref == 'bi':
        payload['gender'] = (g.current_user.gender,)
        payload['sex_pref'] = ('homo', 'bi')

        result = User.get_filtered(**payload)
        if result:
            search_users = result
        payload['gender'] = (g.current_user.opposite_gender,)
        payload['sex_pref'] = ('hetero', 'bi')
        result = User.get_filtered(**payload)
        if result:
            search_users += result
        search_users.sort(
            key=lambda u: getattr(u, req_data["sort"]["sort_by"]),
            reverse=req_data["sort"]["order_by"] == 'desc'
        )

    elif g.current_user.sex_pref == 'homo':
        payload['gender'] = (g.current_user.gender,)
        payload['sex_pref'] = ('homo', 'bi')
        result = User.get_filtered(**payload)
        if result:
            search_users = result
    else:
        payload['gender'] = (g.current_user.opposite_gender,)
        payload['sex_pref'] = ('hetero', 'bi')
        result = User.get_filtered(**payload)
        if result:
            search_users = result
    return jsonify(users=search_users)


@users.route('/page/<int:page_number>', methods=['GET'])
def get_users_page(page_number):
    if page_number < 0:
        page_number = 0

    # users = [User.get_by_id(i).get_view("public") for i in range(1 + 10 * page_number, 11 + 10 * page_number)]
    # return jsonify({"users": users})
    return get_all()


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
    return jsonify({"ok": True, "user": new_user.get_view("personal")})


@users.route('/all', methods=['GET'])
def get_all():
    user_rows = User.queries.get_all()
    result = User.from_db_row(user_rows)
    return jsonify(users=result)


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
        "images": {
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
    current_user = User.get_by_id(session['user_id'])

    if current_user:
        #     current_user.update_field('gender', req_data['gender'])
        if getattr(current_user, 'gender') != req_data['gender']:
            current_user.gender = req_data['gender']
        if getattr(current_user, 'sex_pref') != req_data['sex_pref']:
            current_user.sex_pref = req_data['sex_pref']
        try:
            dob = datetime.datetime.strptime(req_data['dob'][:10], '%Y-%m-%d')
        except ValueError:
            abort(http.HTTPStatus.BAD_REQUEST)

        current_user.dob = dob

        if getattr(current_user, 'bio_text') != req_data['bio_text']:
            current_user.bio_text = req_data['bio_text']

        if getattr(current_user, 'profile_image') != req_data['profile_image']:
            
            current_user.profile_image = req_data['profile_image']

        current_user.update()

        return jsonify({"ok": True})
    return jsonify({"ok": False})  # @TODO: think about error handling


@users.route('/edit_names', methods=['POST'])
def edit_names():
    req_data = request.get_json()
    form_values = {
        "first_name": {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        "last_name": {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        },
        "username": {
            'required': False,
            'default': None,
            'type': str,
            'validator': None
        }
    }
    current_app.logger.info(f"Here we are, the request is: {req_data}")
    check_fields(req_data, form_values)
    current_user = User.get_by_id(session['user_id'])

    if current_user:
        if getattr(current_user, 'first_name') != req_data['first_name'] and len(req_data['first_name']) > 0:
            current_user.first_name = req_data['first_name']
        if getattr(current_user, 'last_name') != req_data['last_name'] and len(req_data['last_name']) > 0:
            current_user.last_name = req_data['last_name']
        if getattr(current_user, 'username') != req_data['username'] and len(req_data['username']) > 0:
            if User.get_by_username(req_data['username']):
                abort(http.HTTPStatus.CONFLICT)  # If another user has this username
            current_user.username = req_data['username']
        current_user.update()

        return jsonify({"ok": True})
    return jsonify({"ok": False})  # @TODO: think about error handling


@users.route('/edit_email', methods=['POST'])
def edit_email():
    req_data = request.get_json()
    form_values = {
        "email": {
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
    current_user = User.get_by_id(session['user_id'])

    if current_user and current_user.check_password(req_data["password"]):
        if getattr(current_user, 'email') != req_data['email']:
            if User.get_by_email(req_data['email']):
                abort(http.HTTPStatus.CONFLICT)  # If another user has this email
            current_user.email = req_data['email']
        current_user.update()

        return jsonify({"ok": True})
    abort(http.HTTPStatus.UNAUTHORIZED)
    # return jsonify({"ok": False})  # @TODO: think about error handling


@users.route('/edit_password', methods=['POST'])
def edit_password():
    req_data = request.get_json()
    form_values = {
        "old_password": {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        },
        "new_password": {
            'required': True,
            'default': None,
            'type': str,
            'validator': None
        }
    }
    current_app.logger.info(f"Here we are, the request is: {req_data}")
    check_fields(req_data, form_values)
    current_user = User.get_by_id(session['user_id'])

    if current_user and current_user.check_password(req_data["old_password"]):
        # @TODO: old and new passwords are the same - do we make it an error?
        if getattr(current_user, 'password'):  # != hash_from_this ->req_data['new_password']:
            current_user.set_password(req_data["new_password"])
        current_user.update()

        return jsonify({"ok": True})
    abort(http.HTTPStatus.UNAUTHORIZED)
    # return jsonify({"ok": False})  # @TODO: think about error handling
