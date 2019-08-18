import datetime
import http

import itsdangerous
from flask import abort, blueprints, current_app, g, jsonify, request

from models.user import User
from modules import serializer
from utils.emails import send_token_email
from utils.form_validator import check_fields
from utils.security import authorised_only

settings = blueprints.Blueprint("settings", __name__)


@settings.route('/profile', methods=['POST'])
@authorised_only
def update_personal_details():
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
		"tags": {
			'required': False,
			'default': None,
			'type': [],
			'validator': None
		},
		"dob": {
			'required': False,
			'default': None,
			'type': str,
			'validator': None
		}
	}
	current_app.logger.debug(f"[update profile] the request is: {req_data}")
	check_fields(req_data, form_values)
	current_user = g.current_user

	if getattr(current_user, 'gender') != req_data['gender']:
		current_user.gender = req_data['gender']
	if getattr(current_user, 'sex_pref') != req_data['sex_pref']:
		current_user.sex_pref = req_data['sex_pref']
	if req_data.get('dob') and type(req_data['dob']) == str:
		try:
			dob = datetime.datetime.strptime(req_data['dob'][:10], '%Y-%m-%d')
			if not (datetime.date.today() - datetime.timedelta(365 * 99) < dob < datetime.date.today()):
				abort(http.HTTPStatus.BAD_REQUEST)
			current_user.dob = dob
		except ValueError:
			abort(http.HTTPStatus.BAD_REQUEST)

	if getattr(current_user, 'bio_text') != req_data['bio_text']:
		current_user.bio_text = req_data['bio_text']

	allowed_tags = {'42', 'eco', 'geek', 'veggie', 'music', 'travel'}
	for tag in req_data['tags']:
		if tag not in allowed_tags:
			abort(http.HTTPStatus.BAD_REQUEST)

	current_user.tags = req_data['tags']

	current_user.update()

	return jsonify({"ok": True})


@settings.route('/name', methods=['POST'])
@authorised_only
def update_name():
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
	current_app.logger.debug(f"[update name], the request is: {req_data}")
	check_fields(req_data, form_values)
	current_user = g.current_user

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


@settings.route('/location', methods=['POST'])
@authorised_only
def update_location():
	req_data = request.get_json()
	form_values = {
		"latitude": {
			'required': False,
			'default': None,
			'type': float,
			'validator': None
		},
		"longitude": {
			'required': False,
			'default': None,
			'type': float,
			'validator': None
		}
	}
	current_app.logger.debug(f"[update location], the request is: {req_data}")
	check_fields(req_data, form_values)
	current_user = g.current_user

	if getattr(current_user, 'latitude') != req_data['latitude']:
		current_user.latitude = str(req_data['latitude'])
	if getattr(current_user, 'longitude') != req_data['longitude']:
		current_user.longitude = str(req_data['longitude'])

	current_user.update()
	return jsonify({"ok": True})


@settings.route('/password', methods=['POST'])
@authorised_only
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
	current_app.logger.debug(f"[update pwd] the request is: {req_data}")
	check_fields(req_data, form_values)
	current_user = g.current_user

	if current_user.check_password(req_data["old_password"]):
		if not current_user.check_password_strength(req_data["password"]):
			abort(http.HTTPStatus.BAD_REQUEST)
		current_user.set_password(req_data["new_password"])
		current_user.update()

		return jsonify({"ok": True})
	abort(http.HTTPStatus.UNAUTHORIZED)


@settings.route('/email', methods=['POST'])
@authorised_only
def update_email():
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
	current_app.logger.debug(f"[update email] the request is: {req_data}")
	check_fields(req_data, form_values)
	current_user = g.current_user

	if current_user.check_password(req_data["password"]):
		if getattr(current_user, 'email') != req_data['email']:
			if User.get_by_email(req_data['email']):
				abort(http.HTTPStatus.CONFLICT)  # If another user has this email

			# Send activation email
			token = serializer.create_token(req_data['email'], 'update_email')
			send_token_email(current_app.config.get('FRONTEND_URL'), 'update_email', req_data['email'], token)

		return jsonify({"ok": True})
	abort(http.HTTPStatus.UNAUTHORIZED)


@settings.route('/activate_email/<token>', methods=['GET'])
@authorised_only
def activate_email(token):
	try:
		email = serializer.verify_token(token, 'update_email').get('email')
		g.current_user.email = email
		g.current_user.update()
		return jsonify({"ok": True})
	except (itsdangerous.BadData, AssertionError):
		abort(http.HTTPStatus.UNAUTHORIZED)


@settings.route('/activate_user/<token>', methods=['GET'])
def activate_user(token):
	try:
		token_content = serializer.verify_token(token, 'activate_user')
		email = token_content.get('email')
		if not email:
			abort(http.HTTPStatus.UNAUTHORIZED)  # The confirmation link is invalid or has expired

		current_user = User.get_by_email(email)

		if not current_user:
			abort(http.HTTPStatus.NOT_FOUND)

		if current_user.activated:
			return jsonify(msg="Account already activated, you can login", ok=True)
		else:
			current_user.activated = True
			current_user.update()
			return jsonify(ok=True)
	except (itsdangerous.BadData, AssertionError):
		abort(http.HTTPStatus.UNAUTHORIZED)
