import re
from datetime import date, datetime, timedelta
from typing import Optional

import postgresql
import postgresql.exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from .model import Model, Queries


class UserQueries(Queries):
	def __init__(self):
		self.get_all = self.query(
			"SELECT * FROM users")
		self.create = self.query(
			"INSERT INTO users (username, email, first_name, last_name, password) "
			"VALUES ($1, $2, $3, $4, $5) RETURNING id")
		self.get_by_unique_field = lambda field: self.query(
			f"SELECT * FROM users WHERE {field} = $1", one=True)
		self.update_field = lambda field: self.query(
			f"UPDATE users SET {field} = $1 WHERE id = $2")
		self.filter = lambda order_by, order_by_field, nulls_behavior="": self.query(f"""
			SELECT 
				users.id,
				users.first_name,
				users.last_name,
				users.email,
				users.bio_text,
				users.gender,
				users.sex_pref,
				users.tags,
				users.profile_image,
				users.username,
				users.rating,
				users.last_connection,
				users.dob,
				dist.distance
			FROM users
			LEFT JOIN (
				SELECT calculate_distance(u1.latitude, u1.longitude, u2.latitude, u2.longitude, 'K') as distance,
					u1.id as user1_id,
					u2.id as user2_id
				FROM users u1
				CROSS JOIN users u2
			) dist on user1_id = $10 AND user2_id = users.id
			WHERE date_part('year', age(dob)) BETWEEN $1 AND $2 
			AND rating BETWEEN $3 AND $4
			AND gender = ANY($5)
			AND sex_pref = ANY($6) 
			AND users.id NOT IN (
						SELECT blocked_users.blocked_id 
						FROM blocked_users 
						WHERE blocked_users.blocker_id = $10
						)
			AND tags @> $7
			AND dist.distance BETWEEN $11 AND $12
			AND users.id != $10
			ORDER BY {order_by_field} {order_by}, users.rating, dist.distance, users.id {nulls_behavior}
			LIMIT $8 OFFSET $9
			""")

		self.count = self.query("""
			SELECT COUNT(*) FROM users
			LEFT JOIN (
				SELECT calculate_distance(u1.latitude, u1.longitude, u2.latitude, u2.longitude, 'K') as distance,
					u1.id as user1_id,
					u2.id as user2_id
				FROM users u1
				CROSS JOIN users u2
			) dist on user1_id = $8 AND user2_id = users.id
			WHERE date_part('year', age(dob)) BETWEEN $1 AND $2
			AND rating BETWEEN $3 AND $4
			AND gender = ANY($5)
			AND sex_pref = ANY($6)
			AND users.id NOT IN (
						SELECT blocked_users.blocked_id 
						FROM blocked_users 
						WHERE blocked_users.blocker_id = $8
						) 
			AND users.id != $8
			AND tags @> $7
			AND dist.distance BETWEEN $9 AND $10
			""")

		self.block_user = self.query(
			"INSERT INTO blocked_users (blocked_id, blocker_id) VALUES ($1, $2)")
		self.unblock_user = self.query(
			"DELETE FROM blocked_users WHERE blocked_id = $1 AND blocker_id = $2")
		self.user_is_blocked = self.query(
			"SELECT * FROM blocked_users WHERE blocked_id = $1 AND blocker_id = $2")
		self.update_last_connection = self.query(
			"UPDATE users SET last_connection = NOW() WHERE id = $1")


class User(Model):
	_fields = {
		'id': {
			'required': False,
			'default': None,
			'type': int,
			'validator': None
		},
		'first_name': {
			'required': True,
			'default': None,
			'type': str,
			'validator': None
		},
		'last_name': {
			'required': True,
			'default': None,
			'type': str,
			'validator': None
		},
		'username': {
			'required': True,
			'default': None,
			'type': str,
			'validator': None
		},
		'email': {
			'required': True,
			'default': None,
			'type': str,
			'validator': None
		},
		'dob': {
			'required': False,
			'default': None,
			'type': date,
			'validator': lambda _: _ and date.today() - timedelta(365 * 99) < _ < date.today()
			# Age between ~ 99y and 0
		},
		'bio_text': {
			'required': False,
			'default': None,
			'type': str,
			'validator': None
		},
		'gender': {
			'required': False,
			'default': None,
			'type': str,
			'validator': lambda _: _ in ['female', 'male']
		},
		'sex_pref': {
			'required': False,
			'default': 'bi',
			'type': str,
			'validator': lambda _: _ in ['homo', 'hetero', 'bi']
		},
		'tags': {
			'required': False,
			'default': None,
			'type': [],
			'validator': None
		},
		'profile_image': {
			'required': False,
			'default': "",
			'type': str,
			'validator': None
		},
		'password': {
			'required': False,
			'default': None,
			'type': str,
			'validator': None
		},
		'rating': {
			'required': False,
			'default': None,
			'type': int,
			'validator': None
		},
		'activated': {
			'required': False,
			'default': None,
			'type': bool,
			'validator': None
		},
		'last_connection': {
			'required': False,
			'default': None,
			'type': datetime,
			'validator': None
		},
		'latitude': {
			'required': False,
			'default': None,
			'type': float,
			'validator': None
		},
		'longitude': {
			'required': False,
			'default': None,
			'type': float,
			'validator': None
		},
		'distance': {
			'required': False,
			'default': None,
			'type': float,
			'validator': None
		},
	}

	_views = {
		'personal': {
			'fields': {
				'id',
				'first_name',
				'last_name',
				'email',
				'dob',
				'bio_text',
				'gender',
				'sex_pref',
				'tags',
				'profile_image',
				'username',
				'rating',
				'activated',
				'last_connection',
				'online',
				'latitude',
				'longitude'
			}
		},
		'public': {
			'fields': {
				'id',
				'first_name',
				'last_name',
				'age',
				'bio_text',
				'gender',
				'sex_pref',
				'tags',
				'profile_image',
				'username',
				'rating',
				'last_connection',
				'online'
			}
		}
	}

	_update_watch_fields = (
		'gender', 'sex_pref', 'dob', 'bio_text',
		'first_name', 'last_name', 'username',
		'email', 'profile_image', 'tags', 'password', 'activated', 'latitude', 'longitude'
	)

	queries = UserQueries()

	@property
	def age(self):
		if not getattr(self, 'dob'):
			return None
		today = date.today()
		age = today.year - self.dob.year
		if today.month < self.dob.month \
				or (today.month == self.dob.month and today.day < self.dob.day):
			age -= 1
		return age

	@property
	def online(self) -> bool:
		if not getattr(self, 'last_connection'):
			return False
		now = datetime.utcnow()
		if (now - self.last_connection) < timedelta(minutes=15):
			return True
		return False

	@property
	def opposite_gender(self):
		if not getattr(self, 'gender'):
			return None
		return {'male': 'female', 'female': 'male'}[self.gender]

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def set_password(self, password):
		self.password = generate_password_hash(password)

	@staticmethod
	def check_password_strength(password):
		exp = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$'
		return re.match(exp, password) is not None

	@classmethod
	def _get_by_unique_field(cls, column: str, value) -> Optional['User']:
		result = cls.queries.get_by_unique_field(column)(value)
		if not result:
			return None
		obj = cls.from_db_row(result)
		return obj

	@classmethod
	def get_by_username(cls, username: str):
		return cls._get_by_unique_field('username', username)

	@classmethod
	def get_by_email(cls, email: str):
		return cls._get_by_unique_field('email', email)

	@classmethod
	def get_by_id(cls, user_id: int):
		return cls._get_by_unique_field('id', user_id)

	def get_filtered(
			self, *,
			age_min, age_max, rating_min, rating_max,
			gender, sex_pref, my_tags, selected_tags, order_by_field, order_by,
			limit, offset, dist_min, dist_max):
		nulls_behavior = ""
		reversed_order = {'ASC': 'DESC', 'DESC': 'ASC'}
		args = [age_min, age_max, rating_min, rating_max, gender, sex_pref, selected_tags, limit, offset, self.id,
		        dist_min, dist_max]
		if order_by_field == 'my_tags':
			order_by_field = 'count_intersect($13, tags)'
			# order_by = reversed_order[order_by]
			args.append(my_tags)
		elif order_by_field == 'tags':
			order_by_field = 'COALESCE(array_length(tags, 1), 0)'
		elif order_by_field == 'age':
			order_by_field = 'dob'
			order_by = reversed_order[order_by]
		elif order_by_field == 'distance':
			order_by_field = "13"
			nulls_behavior = "NULLS LAST"
		print(f"order_by: {order_by}, order_by_field: {order_by_field}")
		result = self.queries.filter(order_by, order_by_field, nulls_behavior)(
			*args
		)
		if not result:
			return None
		obj = self.from_db_row(result)
		return obj

	def count_filtered(self, *, age_min, age_max, rating_min, rating_max, gender, sex_pref,
	                   selected_tags, dist_min, dist_max, **_):
		result = self.queries.count(age_min, age_max, rating_min, rating_max, gender, sex_pref,
		                            selected_tags, self.id, dist_min, dist_max)
		if not result:
			return 0
		return result[0][0]

	def create(self):
		result = self.queries.create(
			getattr(self, 'username'), getattr(self, 'email'), getattr(self, 'first_name'),
			getattr(self, 'last_name'), getattr(self, 'password')
		)
		self.id = result[0][0]

	def _update_field(self, field, value):
		self.queries.update_field(field)(value, self.id)

	@classmethod
	def block_user(cls, blocked_id, blocker_id):
		try:
			cls.queries.block_user(blocked_id, blocker_id)
		except postgresql.exceptions.UniqueError as error:
			return error

	@classmethod
	def unblock_user(cls, blocked_id, blocker_id):
		cls.queries.unblock_user(blocked_id, blocker_id)

	@classmethod
	def user_is_blocked(cls, blocked_id, blocker_id):
		result = cls.queries.user_is_blocked(blocked_id, blocker_id)
		if not result:
			return False
		return True

	def made_request(self):
		self.queries.update_last_connection(self.id)
