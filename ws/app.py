#!/usr/bin/env python
from typing import Optional, Awaitable

import toredis
import tornado.web
import tornado.websocket
import tornado.ioloop

REDIS_HOST = "redis"


class MessagesHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(MessagesHandler, self).__init__(*args, **kwargs)
        self.user_id = 12
        self.sender_name = "Q"  # @TODO
        self.companion_id = None
        self.channel = None
        self.client = toredis.Client()
        self.client.connect(host=REDIS_HOST, callback=lambda: print(f"Connected to Redis"))  # @TODO

    def check_origin(self, origin):
        return True

    @property
    def ordered_users(self) -> (Optional[int], Optional[int]):
        if not self.user_id or not self.companion_id:
            return None, None
        if self.user_id < self.companion_id:
            return self.user_id, self.companion_id
        return self.companion_id, self.user_id

    def open(self, companion_id=None):
        self.companion_id = companion_id
        self.channel = f"chat_{self.ordered_users[0]}_{self.ordered_users[1]}_messages"
        self.client.subscribe(self.channel, callback=self.show_new_message)

    def handle_request(self, response):
        pass

    def on_message(self, message):
        if not message:
            return
        if len(message) > 10000:
            return
        print(message)

    def show_new_message(self, msg):
        if msg == 1:
            return
        print(msg)
        self.write_message(str(msg[2]))

    def on_close(self):
        try:
            self.client.unsubscribe(self.channel)
        except AttributeError:
            pass

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass


application = tornado.web.Application([
    (r'/(?P<thread_id>\d+)/', MessagesHandler),
    (r'/websocket/?', MessagesHandler)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
