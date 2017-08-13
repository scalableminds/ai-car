from aiohttp import web, WSMsgType, Timeout
import asyncio 
import json

from handlers.handler import Handler
from sensors.sensor import Sensor

class KeyHandler(Handler, Sensor):
    def __init__(self):
        self.frame = None
        self.current_keys = set()
        self.is_connected = False

    @asyncio.coroutine
    def handle(self, request):
        if self.is_connected:
            raise web.HTTPConflict()
        try:
            self.ws = web.WebSocketResponse()
            self.is_connected = True
            yield from self.ws.prepare(request)

            while self.running:
                try:
                    msg = yield from self.ws.receive(timeout=1)
                    if msg is not None:
                        if msg.type == WSMsgType.TEXT:
                            self.current_keys = set(json.loads(msg.data))
                        elif msg.type == WSMsgType.CLOSE:
                            break
                        elif msg.type == WSMsgType.ERROR:
                            print("ws connection closed with exception %s" %
                                  self.ws.exception())
                            break
                except Exception as e:
                    pass
            return self.ws
        finally:
            self.current_keys = set()
            if not self.ws.closed:
                yield from self.ws.close()
            self.is_connected = False

    def __enter__(self):
        self.running = True

    def __exit__(self, exit_type, value, traceback):
        self.running = False
        self.current_keys = set()

    def write(self, data):
        self.frame = data

    def read(self):
        return self.current_keys
