import http

from flask import blueprints, jsonify, abort, g

from models.like import Like
from models.notification import Notification
from models.user import User
from utils.security import authorised_only

likes = blueprints.Blueprint("likes", __name__)


@likes.route('/<int:user_id>', methods=['POST'])
@authorised_only
def create_like(user_id):
	liked_user = User.get_by_id(user_id)  # Check if user exists
	has_photo = Like.able_to_like(g.current_user.id)  # Check if user has profile image
	is_blocked = User.user_is_blocked(g.current_user.id, user_id)  # Check if user was blocked

	if is_blocked:
		abort(http.HTTPStatus.FORBIDDEN)

	if not has_photo:
		abort(http.HTTPStatus.UNAUTHORIZED)

	if liked_user and has_photo:
		Like.like(g.current_user.id, user_id)

		# If user is not blocked [blocked, blocker]
		# Notification
		if not is_blocked:
			text = Notification.notification_text('like', g.current_user.id)
			notification = Notification.from_dict({"user_id": user_id, "text": text, "type": "like"})
			notification.create()

		return jsonify(ok=True)
	abort(http.HTTPStatus.BAD_REQUEST)


@likes.route('/<int:user_id>', methods=['DELETE'])
@authorised_only
def remove_like(user_id):
	liked_user = User.get_by_id(user_id)  # Check if user exists
	if liked_user:
		Like.unlike(g.current_user.id, user_id)

		# If user is not blocked [blocked, blocker]
		# Notification
		if not User.user_is_blocked(g.current_user.id, user_id):
			text = Notification.notification_text('unlike', g.current_user.id)
			notification = Notification.from_dict({"user_id": user_id, "text": text, "type": "like"})
			notification.create()

		return jsonify(ok=True)
	abort(http.HTTPStatus.BAD_REQUEST)
