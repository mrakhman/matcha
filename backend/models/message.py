from datetime import datetime, date, timedelta


from .model import Model, Queries
from .user import User


# SELECT messages.id, messages.sender_id, users.username, messages.created_at, messages.text
# FROM messages INNER JOIN users
# ON messages.sender_id = users.id
# WHERE messages.sender_id IN(12, 16) AND messages.receiver_id IN(12, 16)
# ORDER BY created_at DESC

class MessageQueries(Queries):
	def __init__(self):
		self.create = self.query("INSERT INTO messages (sender_id, receiver_id, text) VALUES ($1, $2, $3) RETURNING id")
		self.get_user_chats = self.query("SELECT users.id, users.profile_image, users.username "
											"FROM users WHERE users.id IN ("
											"(SELECT messages.sender_id AS chat_users FROM messages "
											"WHERE messages.sender_id = $1 OR messages.receiver_id = $1) "
											"UNION "
											"(SELECT messages.receiver_id AS chat_users FROM messages "
											"WHERE messages.sender_id = $1 OR messages.receiver_id = $1)"
											") "
											"AND users.id != $1")

		self.get_chat_messages = self.query("SELECT messages.id, messages.sender_id, users.username, messages.created_at, messages.text "
											"FROM messages INNER JOIN users "
											"ON messages.sender_id = users.id "
											"WHERE messages.sender_id IN($1, $2) AND messages.receiver_id IN($1, $2)"
											"ORDER BY created_at DESC")
		# self.get_by_id = self.query("SELECT * FROM notifications WHERE id = $1", one=True)
		# self.update_field = lambda field: self.query(f"UPDATE notifications SET {field} = $1 WHERE id = $2")
		# self.mark_all_read = self.query("UPDATE notifications SET is_read = true WHERE user_id = $1")


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
		}
	}

	_update_watch_fields = ()

	queries = MessageQueries()

	# @property
	# def created_at(self):
	#     if not getattr(self, 'created_at'):
	#         return None
	#     created_at = datetime.fromtimestamp(self.created_at)
	#     return created_at

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
			return None
		obj = cls.from_db_row(result)
		return obj

	def create(self):
		self.queries.create(self.sender_id, self.receiver_id, self.text)
		# self.queries.create(getattr(self, 'user_id'), getattr(self, 'text'))

	# def _update_field(self, field, value):
	#     self.queries.update_field(field)(value, self.id)

