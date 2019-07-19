import datetime
import http

from flask import blueprints, jsonify, abort, current_app, session, request, g, redirect, url_for

from models.user import User
from models.notification import Notification
from models.message import Message

from utils.form_validator import check_fields
from utils.security import authorised_only

messages = blueprints.Blueprint("messages", __name__)


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
	message = Message.from_dict({"sender_id": sender_id, "receiver_id": int(req_data["receiver_id"]), "text": req_data["text"]})
	message.create()
	return jsonify(ok=True)


@messages.route("/chats", methods=['GET'])
@authorised_only
def get_my_chats():
	my_chats = Message.get_user_chats(g.current_user.id)
	return jsonify(chats=my_chats)


@messages.route('/<int:user_id>', methods=['GET'])
@authorised_only
def get_chat_messages(user_id):
	chat_messages = Message.get_chat_messages(g.current_user.id, user_id)
	return jsonify(messages=chat_messages)

