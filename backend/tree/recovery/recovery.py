import http

import itsdangerous
from flask import blueprints, request, abort, jsonify

from models.user import User
from modules import serializer
from utils.emails import send_token_email
from utils.form_validator import check_fields

recovery = blueprints.Blueprint("recovery", __name__)


def send_token(token_type):
	req_data = request.get_json()
	form_values = {
		"email": {
			'required': True,
			'default': None,
			'type': str,
			'validator': lambda x: '@' in x[1:-1]
		}
	}
	check_fields(req_data, form_values)

	current_user = User.get_by_email(req_data['email'])
	if not current_user:
		abort(http.HTTPStatus.NOT_FOUND)  # If user with this email doesn't exist

	# Send activation email
	token = serializer.create_token(req_data['email'], token_type)
	send_token_email(token_type, req_data['email'], token)
	return jsonify({"ok": True})


@recovery.route('/resend_activation', methods=['POST'])
def resend_activation():
	return send_token('activate_user')


@recovery.route('/password', methods=['POST'])
def password_recovery():
	return send_token('reset_pwd')


@recovery.route('/reset_password/<token>', methods=['GET'])
def check_password_reset_token(token):
	try:
		email = serializer.verify_token(token, 'reset_pwd').get('email')
		current_user = User.get_by_email(email)
		if not current_user:
			abort(http.HTTPStatus.UNAUTHORIZED)
		return jsonify({"ok": True})
	except (itsdangerous.BadData, AssertionError):
		abort(http.HTTPStatus.UNAUTHORIZED)


@recovery.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
	req_data = request.get_json()
	form_values = {
		"password": {
			'required': True,
			'default': None,
			'type': str,
			'validator': None
		}
	}
	check_fields(req_data, form_values)

	try:
		email = serializer.verify_token(token, 'reset_pwd').get('email')
		current_user = User.get_by_email(email)
		if not current_user:
			abort(http.HTTPStatus.UNAUTHORIZED)
		current_user.set_password(req_data["password"])
		current_user.update()
		return jsonify({"ok": True})
	except (itsdangerous.BadData, AssertionError):
		abort(http.HTTPStatus.UNAUTHORIZED)
