import http

from flask import blueprints, jsonify, abort, request, g

from models.like import Like
from models.message import Message
from models.user import User
from utils.form_validator import check_fields
from utils.security import authorised_only
from redis import redis_client

messages = blueprints.Blueprint("messages", __name__)


@messages.route("/allowed/<int:user_id>", methods=['GET'])
@authorised_only
def users_can_chat(user_id):
	sender_id = g.current_user.id
	receiver_id = user_id
	if (Like.is_liked(sender_id, receiver_id) and Like.is_liked(receiver_id, sender_id)) \
		and not (User.user_is_blocked(sender_id, receiver_id) or User.user_is_blocked(receiver_id, sender_id)):
		return jsonify(ok=True)
	return jsonify(ok=False)


@messages.route("/new", methods=['POST'])
@authorised_only
def create_message():
	req_data = request.get_json()
	print(req_data)
	form_values = {
		"text": {
			'required': False,
			'default': None,
			'type': str,
			'validator': None
		},
		"receiver_id": {
			'required': False,
			'default': None,
			'type': int,
			'validator': None
		}
	}
	check_fields(req_data, form_values)
	sender_id = g.current_user.id
	receiver_id = int(req_data["receiver_id"])
	if (Like.is_liked(sender_id, receiver_id) and Like.is_liked(receiver_id, sender_id)) \
			and (not User.user_is_blocked(sender_id, receiver_id) and not User.user_is_blocked(receiver_id, sender_id)):
		message = Message.from_dict({"sender_id": sender_id, "receiver_id": receiver_id, "text": req_data["text"]})
		message.create()

		# Redis here
		red = redis_client.StrictRedis(host='redis', port=8888, db=0)
		red.publish('messages' + '_' + str(sender_id) + '_' + str(receiver_id), req_data["text"])

		return jsonify(ok=True)
	abort(http.HTTPStatus.UNAUTHORIZED)


@messages.route("/chats", methods=['GET'])
@authorised_only
def get_my_chats():
	my_chats = Message.get_user_chats(g.current_user.id)
	return jsonify(chats=my_chats)


@messages.route('/<int:user_id>', methods=['GET'])
@authorised_only
def get_chat_messages(user_id):
	chat_messages = Message.get_chat_messages(g.current_user.id, user_id)
	msgs = list(map(lambda msg: msg.get_view('chat'), chat_messages))
	return jsonify(messages=msgs)
