from datetime import datetime

from flask import json

from modules import redis_client
from .model import Model, Queries


# SELECT messages.id, messages.sender_id, users.username, messages.created_at, messages.text
# FROM messages INNER JOIN users
# ON messages.sender_id = users.id
# WHERE messages.sender_id IN(12, 16) AND messages.receiver_id IN(12, 16)
# ORDER BY created_at DESC

class MessageQueries(Queries):
	def __init__(self):
		self.create = self.query("INSERT INTO messages (sender_id, receiver_id, text) VALUES ($1, $2, $3) RETURNING id")
		self.get_user_chats = self.query(
			"SELECT users.id, users.profile_image, users.username "
			"FROM users WHERE users.id IN ("
			"(SELECT messages.sender_id AS chat_users FROM messages "
			"WHERE messages.sender_id = $1 OR messages.receiver_id = $1) "
			"UNION "
			"(SELECT messages.receiver_id AS chat_users FROM messages "
			"WHERE messages.sender_id = $1 OR messages.receiver_id = $1)"
			") "
			"AND users.id != $1")

		self.get_chat_messages = self.query(
			"SELECT messages.id, messages.sender_id, messages.created_at, messages.text "
			"FROM messages "
			"WHERE messages.sender_id IN($1, $2) AND messages.receiver_id IN($1, $2)"
			"ORDER BY created_at ASC")


class Message(Model):
	_fields = {
		'id': {
			'required': False,
			'default': None,
			'type': int,
			'validator': None
		},
		'sender_id': {
			'required': False,
			'default': None,
			'type': int,
			'validator': None
		},
		'receiver_id': {
			'required': False,
			'default': False,
			'type': int,
			'validator': None
		},
		'text': {
			'required': False,
			'default': None,
			'type': str,
			'validator': None
		},
		'created_at': {
			'required': False,
			'default': None,
			'type': datetime,
			'validator': None
		},
		'username': {
			'required': False,
			'default': None,
			'type': str,
			'validator': None
		},
		'profile_image': {
			'required': False,
			'default': None,
			'type': str,
			'validator': None
		},
	}

	_views = {
		'personal': {
			'fields': {
				'id',
				'sender_id',
				'receiver_id',
				'text',
				'created_at',
				'username',
				'profile_image'
			}
		},
		'public': {
			'fields': {
				'id',
				'sender_id',
				'receiver_id',
				'text',
				'created_at',
				'username',
				'profile_image'
			}
		},
		'chat': {
			'fields': {
				'id',
				'sender_id',
				'receiver_id',
				'text',
				'created_at'
			}
		}
	}

	_update_watch_fields = ()

	queries = MessageQueries()

	@classmethod
	def get_user_chats(cls, user_id):
		result = cls.queries.get_user_chats(user_id)
		if not result:
			return None
		obj = cls.from_db_row(result)
		return obj

	@classmethod
	def get_chat_messages(cls, sender_id, receiver_id):
		result = cls.queries.get_chat_messages(sender_id, receiver_id)
		if not result:
			return []
		obj = cls.from_db_row(result)
		return obj

	def create(self):
		result = self.queries.create(self.sender_id, self.receiver_id, self.text)
		self.id = result[0][0]

		users = [self.sender_id, self.receiver_id]
		users.sort()
		redis_payload = self.get_view('chat')
		redis_payload['created_at'] = datetime.utcnow()
		redis_client.publish(f"chat_{users[0]}_{users[1]}_messages", json.dumps(redis_payload))
