import http
import json
from http.cookies import SimpleCookie
from typing import Optional

import requests
import toredis
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.log import app_log as log

REDIS_HOST = "redis"
API_URL = "http://backend:5000"
SERVER_PORT = 8888


"""
2 types -> notification and chat
notifications are subscribed automatically when socket is opened
to subscribe to a chat -> send {"action": "open_chat", "companion_id": USER_ID}
to unsubscribe from chat -> send {"action": "close_chat"}
subscribing to new chat will unsubscribe from previous
On event sends payload like {"type": "message/notification", "channel": "channel_name", "data": ...}
"""


def get_me(cookies: SimpleCookie):
	request_cookies = {c.key: c.value for c in cookies.values()}
	resp = requests.get(API_URL + "/users/me", cookies=request_cookies)
	if not resp.ok:
		if resp.status_code == http.HTTPStatus.UNAUTHORIZED:
			raise tornado.web.HTTPError(http.HTTPStatus.UNAUTHORIZED)
		raise tornado.web.HTTPError()
	resp.raise_for_status()
	user = resp.json().get('user')
	return user


class WSHandler(tornado.websocket.WebSocketHandler):
	def __init__(self, *args, **kwargs):
		super(WSHandler, self).__init__(*args, **kwargs)
		self.user_id = None
		self.notifications_channel = None
		self.chat_channel = None
		self.client = None

	def prepare_redis(self):
		self.client = toredis.Client()
		self.client.connect(host=REDIS_HOST, callback=lambda: log.debug(f"Connected to Redis"))

	def prepare(self):
		user = get_me(self.cookies)
		if not user:
			raise tornado.web.HTTPError(http.HTTPStatus.BAD_REQUEST)
		self.user_id = user['id']
		self.prepare_redis()

	def open(self, *args, **kwargs):
		self.open_notification()

	def handler(self, msg):
		if msg[0] == b'subscribe':
			log.debug(f"subscribed to {msg[1]}")
		elif msg[0] == b'unsubscribe':
			log.debug(f"unsubscribed from {msg[1]}")
		elif msg[0] == b'message':
			log.debug(f"received {msg[2]} from {msg[1]}")
			try:
				incoming_payload = json.loads(msg[2])
				channel = msg[1].decode('utf-8')
				event_type = 'unknown'
				if 'chat' in channel:
					event_type = 'message'
				elif 'notification' in channel:
					event_type = 'notification'
				response_payload = {
					"type": event_type,
					"channel": channel,
					"data": incoming_payload
				}
				self.send_json(response_payload)
			except json.JSONDecodeError:
				pass
		else:
			log.debug(f"got unknown event: {msg}")

	def on_close(self):
		log.debug(f"Closing connection {self}")
		try:
			if self.notifications_channel:
				self.client.unsubscribe(self.notifications_channel)
			self.close_chat()
		except AttributeError:
			pass

	def data_received(self, chunk):
		pass

	def check_origin(self, origin):  # @TODO?
		return True

	def on_message(self, message):
		try:
			request = json.loads(message)
			action = request.get('action')
			if action == 'open_chat':
				try:
					companion_id = int(request.get('companion_id'))
					self.open_chat(companion_id)
				except ValueError:
					self.send_not_ok("can't get companion id")
			elif action == "close_chat":
				self.close_chat()
			elif action == "ping":
				self.send_json({"answer": "pong"})
			self.send_ok()
		except json.JSONDecodeError:
			self.send_not_ok("can't parse json")

	def send_json(self, data: dict):
		self.write_message(json.dumps(data))

	def send_ok(self):
		self.send_json({'status': 'ok'})

	def send_not_ok(self, err: Optional[str] = None):
		if err:
			self.send_json({'status': 'not_ok', 'err': err})
		else:
			self.send_json({'status': 'not_ok'})

	def open_notification(self):
		self.notifications_channel = f"notifications_{self.user_id}"
		# self.client.subscribe(self.notifications_channel, callback=self.handler('notification'))
		self.client.subscribe(self.notifications_channel, callback=self.handler)

	def open_chat(self, companion_id: int):
		if companion_id == self.user_id:
			# Return err
			pass
		ordered_users = sorted((companion_id, self.user_id))
		self.close_chat()
		self.chat_channel = f"chat_{ordered_users[0]}_{ordered_users[1]}_messages"
		# self.client.subscribe(self.chat_channel, callback=self.handler('message'))
		self.client.subscribe(self.chat_channel, callback=self.handler)

	def close_chat(self):
		if self.chat_channel:
			self.client.unsubscribe(self.chat_channel)
			self.chat_channel = None


def main():
	application = tornado.web.Application([
		(r'/', WSHandler),
	])
	tornado.options.parse_command_line()
	log.info("Starting WS server")
	application.listen(SERVER_PORT)
	tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
	main()
