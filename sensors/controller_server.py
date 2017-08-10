import asyncio
from aiohttp import web, WSMsgType
import json
from threading import Thread

from sensors.sensor import Sensor


class ControllerServer(Sensor):
    def __init__(self, port):
        self.port = port
        self.current_keys = set()
        self.is_connected = False
        self.running = False

    def __enter__(self):
        self.running = True
        Thread(target=self.run_thread).start()
        return self

    def __exit__(self, exit_type, value, traceback):
        self.loop.stop()
        self.running = False
        self.current_keys = set()

    def read(self):
        return self.current_keys

    def run_thread(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        app = web.Application(loop=self.loop)
        app.router.add_get("/", self.controller_handler)
        app.router.add_get("/socket", self.websocket_handler)
        web.run_app(app, port=self.port, handle_signals=False)

    @asyncio.coroutine
    def controller_handler(self, request):
        with open("sensors/controller.html", "rt") as file:
            return web.Response(text=file.read(), content_type="text/html")

    @asyncio.coroutine
    def websocket_handler(self, request):
        if self.is_connected:
            raise web.HTTPConflict()

        try:
            ws = web.WebSocketResponse()
            self.is_connected = True
            yield from ws.prepare(request)

            while self.running:
                msg = yield from ws.receive()
                if msg.type == WSMsgType.TEXT:
                    self.current_keys = set(json.loads(msg.data))

                elif msg.type == WSMsgType.CLOSE:
                    break
                elif msg.type == WSMsgType.ERROR:
                    print("ws connection closed with exception %s" %
                          ws.exception())
                    break
            return ws
        finally:
            self.current_keys = set()
            self.is_connected = False
