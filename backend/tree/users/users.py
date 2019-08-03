import http
import math

from flask import blueprints, jsonify, abort, current_app, session, request, g, redirect, url_for

from models.history import History
from models.image import Image
from models.like import Like
from models.notification import Notification
from models.user import User
from modules import serializer
from utils.emails import send_token_email
from utils.form_validator import check_fields
from utils.security import authorised_only

users = blueprints.Blueprint("users", __name__)


@users.route('/<int:user_id>', methods=['GET'])
@authorised_only
def get_user_by_id(user_id):
	user = User.get_by_id(user_id)
	if user:
		payload = user.get_view("public")
		if request.args.get('with_images'):
			user_images = Image.get_user_images(user.id)
			payload['images'] = []
			if user_images:
				payload['images'] = [{"src": i.image_src, "id": i.id} for i in user_images]
		if request.args.get('with_like'):
			has_like = Like.is_liked(g.current_user.id, user_id)
			likes_me = Like.is_liked(user_id, g.current_user.id)
			payload['has_like'] = has_like
			payload['likes_me'] = likes_me

		# If I blocked this user [blocked, blocker]
		if User.user_is_blocked(user_id, g.current_user.id):
			u_is_blocked = True
		else:
			u_is_blocked = False
		if request.args.get('with_block'):
			payload['is_blocked'] = u_is_blocked

		# If user didn't block me [blocked, blocker]
		# Send notification
		if not User.user_is_blocked(g.current_user.id, user_id):
			if g.current_user.id != user_id:
				text = Notification.notification_text('view', g.current_user.id)
				notification = Notification.from_dict({"user_id": user_id, "text": text, "type": "view"})
				notification.create()

		# View history
		if g.current_user.id != user_id:
			History.add_to_history(g.current_user.id, user_id)

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
	per_page = 5
	count_users = 0
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
	req_data["filter"].setdefault("tags", [])
	# Age
	filter_validation["max"]["default"] = 99
	check_fields(req_data["filter"]["age"], filter_validation)
	# Rating
	filter_validation["max"]["default"] = 10
	check_fields(req_data["filter"]["rating"], filter_validation)
	# Distance
	filter_validation["max"]["default"] = 10000
	check_fields(req_data["filter"]["distance"], filter_validation)

	# Sort
	req_data.setdefault("sort", {})
	req_data["sort"].setdefault("order_by", "desc")
	req_data["sort"].setdefault("sort_by", "my_tags")
	req_data["sort"]["order_by"] = req_data["sort"]["order_by"].upper()
	if req_data["sort"]["order_by"] not in ("ASC", "DESC"):
		abort(http.HTTPStatus.BAD_REQUEST)
	if req_data["sort"]["sort_by"] not in ("id", "age", "distance", "rating", "tags", "my_tags"):
		abort(http.HTTPStatus.BAD_REQUEST)
	# Here we are with all data valid

	search_users: [User] = []
	payload = {
		'age_min': int(req_data['filter']['age']['min']),
		'age_max': int(req_data['filter']['age']['max']),
		'rating_min': int(req_data['filter']['rating']['min']),
		'rating_max': int(req_data['filter']['rating']['max']),
		'dist_min': int(req_data['filter']['distance']['min']),
		'dist_max': int(req_data['filter']['distance']['max']),
		'selected_tags': req_data['filter']['tags'],
		'my_tags': g.current_user.tags,
		'order_by_field': req_data['sort']['sort_by'],
		'order_by': req_data['sort']['order_by'],
		'limit': per_page,
		'offset': per_page * page_number
	}

	if g.current_user.sex_pref == 'bi':
		payload['gender'] = (g.current_user.gender,)
		payload['sex_pref'] = ('homo', 'bi')

		result = g.current_user.get_filtered(**payload)
		if result:
			search_users = result
			count_users = g.current_user.count_filtered(**payload)
		payload['gender'] = (g.current_user.opposite_gender,)
		payload['sex_pref'] = ('hetero', 'bi')

		result = g.current_user.get_filtered(**payload)
		if result:
			search_users += result
			count_users += g.current_user.count_filtered(**payload)

		def get_sort_key(u: User):
			if req_data["sort"]["sort_by"] == 'tags':
				return len(getattr(u, req_data["sort"]["sort_by"]))
			elif req_data["sort"]["sort_by"] == 'my_tags':
				return -len(set(u.tags) & set(g.current_user.tags))
			value = getattr(u, req_data["sort"]["sort_by"])
			if value is None:
				if req_data["sort"]["sort_by"] == 'distance':
					return (math.inf, -math.inf)[req_data["sort"]["order_by"] == 'DESC']
				return 0
			return value

		search_users.sort(
			key=get_sort_key,
			reverse=req_data["sort"]["order_by"] == 'DESC'
		)

	elif g.current_user.sex_pref == 'homo':
		payload['gender'] = (g.current_user.gender,)
		payload['sex_pref'] = ('homo', 'bi')

		result = g.current_user.get_filtered(**payload)
		if result:
			search_users = result
			count_users = g.current_user.count_filtered(**payload)
	else:
		payload['gender'] = (g.current_user.opposite_gender,)
		payload['sex_pref'] = ('hetero', 'bi')

		result = g.current_user.get_filtered(**payload)
		if result:
			search_users = result
			count_users = g.current_user.count_filtered(**payload)
	search_users = [u.get_view(with_attr={"distance"}) for u in search_users]
	return jsonify(users=search_users, total_users=count_users, per_page=per_page)


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

	if User.get_by_email(req_data['email']):
		abort(http.HTTPStatus.CONFLICT)  # If another user has this email
	if User.get_by_username(req_data['username']):
		abort(http.HTTPStatus.CONFLICT)  # If another user has this username

	new_user = User.from_dict(req_data)
	new_user.set_password(req_data["password"])
	new_user.create()

	# Send activation email
	token = serializer.create_token(req_data['email'], 'activate_user')
	send_token_email('activate_user', new_user.email, token)

	return jsonify({"ok": True, "user": new_user.get_view("personal")})


@users.route('/block/<int:blocked_id>', methods=['POST'])
def block_user(blocked_id):
	current_user = User.get_by_id(session['user_id'])
	if not current_user:
		abort(http.HTTPStatus.UNAUTHORIZED)
	blocker_id = current_user.id
	User.block_user(blocked_id, blocker_id)
	return jsonify({"ok": True})


@users.route('/block/<int:blocked_id>', methods=['DELETE'])
def unblock_user(blocked_id):
	current_user = User.get_by_id(session['user_id'])
	if not current_user:
		abort(http.HTTPStatus.UNAUTHORIZED)
	blocker_id = current_user.id
	User.unblock_user(blocked_id, blocker_id)
	return jsonify({"ok": True})
