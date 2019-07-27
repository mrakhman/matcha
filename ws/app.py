import http
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


class RedisChannelHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(RedisChannelHandler, self).__init__(*args, **kwargs)
        self.channel = None
        self.client = None

    def prepare_redis(self):
        self.client = toredis.Client()
        self.client.connect(host=REDIS_HOST, callback=lambda: log.debug(f"Connected to Redis"))

    def handler(self, msg):
        if msg[0] == b'subscribe':
            log.debug(f"subscribed to {msg[1]}")
        elif msg[0] == b'unsubscribe':
            log.debug(f"unsubscribed from {msg[1]}")
        elif msg[0] == b'message':
            self.write_message(msg[2].decode('utf-8'))
            log.debug(f"received {msg[2]} from {msg[1]}")
        else:
            log.debug(f"Got unknown event: {msg}")

    def on_close(self):
        log.debug(f"Closing connection {self}")
        try:
            self.client.unsubscribe(self.channel)
        except AttributeError:
            pass

    def data_received(self, chunk):
        pass

    def on_message(self, message):
        pass


class ChatHandler(RedisChannelHandler):
    def __init__(self, *args, **kwargs):
        super(ChatHandler, self).__init__(*args, **kwargs)
        self.user_id = None
        self.companion_id = None

    @property
    def ordered_users(self) -> (Optional[int], Optional[int]):
        if not self.user_id or not self.companion_id:
            return None, None
        if self.user_id < self.companion_id:
            return self.user_id, self.companion_id
        return self.companion_id, self.user_id

    def check_origin(self, origin):
        return True

    def prepare(self):
        user = get_me(self.cookies)
        if not user:
            raise tornado.web.HTTPError(http.HTTPStatus.BAD_REQUEST)
        self.user_id = user['id']
        self.prepare_redis()

    def open(self, companion_id=None):
        self.companion_id = int(companion_id)
        if self.companion_id == self.user_id:
            raise tornado.web.HTTPError(http.HTTPStatus.BAD_REQUEST)
        self.channel = f"chat_{self.ordered_users[0]}_{self.ordered_users[1]}_messages"
        self.client.subscribe(self.channel, callback=self.handler)


class NotificationsHandler(RedisChannelHandler):
    def __init__(self, *args, **kwargs):
        super(NotificationsHandler, self).__init__(*args, **kwargs)
        self.user_id = None
        self.channel = None

    def check_origin(self, origin):
        return True

    def prepare(self):
        user = get_me(self.cookies)
        if not user:
            raise tornado.web.HTTPError(http.HTTPStatus.BAD_REQUEST)
        self.user_id = user['id']
        self.prepare_redis()

    def open(self, companion_id=None):
        self.channel = f"notifications_{self.user_id}"
        self.client.subscribe(self.channel, callback=self.handler)


def main():
    application = tornado.web.Application([
        (r'/chat/(?P<companion_id>\d+)/', ChatHandler),
        (r'/notifications/', NotificationsHandler)
    ])
    tornado.options.parse_command_line()
    log.info("Starting WS server")
    application.listen(SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()
    log.info("Ready")


if __name__ == "__main__":
    main()
