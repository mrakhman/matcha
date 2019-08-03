from typing import Optional

from flask import Flask
from itsdangerous import URLSafeTimedSerializer


class MySerializerException(Exception):
	pass


class MySerializer:
	def __init__(self, *args, **kwargs):
		self._init_args = args
		self._init_kwargs = kwargs
		self._instance: Optional[URLSafeTimedSerializer] = None
		self.expiration = 3600 * 2  # 2h

	def __getattr__(self, item):
		if item in [
			'_init_args', '_init_kwargs', '_instance', 'expiration', 'init_app',
			'create_token', 'verify_token'
		]:
			return getattr(self, item)
		if self._instance:
			return getattr(self._instance, item)
		raise MySerializerException("Instance not initialized")

	def init_app(self, app: Flask):
		secret_key = app.secret_key
		salt = app.config.get('SECURITY_SALT')
		if not secret_key:
			raise MySerializerException("Secret key should be defined")
		self._instance = URLSafeTimedSerializer(secret_key, *self._init_args, **self._init_kwargs)
		if salt:
			self._instance.salt = salt

	def create_token(self, email, token_type) -> str:
		assert token_type is not None
		return self.dumps({'email': email, 'type': token_type})

	def verify_token(self, token, token_type, expiration=None) -> {}:
		assert token_type is not None
		if expiration is None:
			expiration = self.expiration
		payload = self.loads(token, max_age=expiration)
		assert payload.get('token_type') == token_type
		return payload
