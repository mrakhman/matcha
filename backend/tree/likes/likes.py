import os
import uuid
import http

from flask import blueprints, jsonify, abort, current_app, session, request, g, redirect, url_for

from models.like import Like
from models.user import User
from models.notification import Notification
from utils.form_validator import check_fields
from utils.security import authorised_only

likes = blueprints.Blueprint("likes", __name__)


@likes.route('/<int:user_id>', methods=['POST'])
@authorised_only
def create_like(user_id):
	# current_app.logger.info(f"Here we are, the request is: {user_id}")
	liked_user = User.get_by_id(user_id)  # Check if user exists
	if liked_user:
		Like.like(g.current_user.id, user_id)

		# Notification
		text = Notification.notification_text('like', g.current_user.id)
		notification = Notification.from_dict({"user_id": user_id, "text": text, "type": "like"})
		notification.create()
		# TODO: add like notification on front

		return jsonify(ok=True)
	abort(http.HTTPStatus.BAD_REQUEST)


@likes.route('/<int:user_id>', methods=['DELETE'])
@authorised_only
def remove_like(user_id):
	liked_user = User.get_by_id(user_id)  # Check if user exists
	if liked_user:
		Like.unlike(g.current_user.id, user_id)

		# Notification
		text = Notification.notification_text('unlike', g.current_user.id)
		notification = Notification.from_dict({"user_id": user_id, "text": text, "type": "unlike"})
		notification.create()
		# TODO: add unlike notification on front

		return jsonify(ok=True)
	abort(http.HTTPStatus.BAD_REQUEST)
