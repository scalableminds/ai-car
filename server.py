import asyncio
from aiohttp import web, WSMsgType
import json
from threading import Thread
from handlers import handler

from sensors.sensor import Sensor

class Server():
    def __init__(self, handlers=dict(), port=8080):
        self.port = port
        self.handlers = handlers
        self.running = False

    def __enter__(self):
        self.running = True
        self.thread = Thread(target=self.run_thread)
        self.thread.start()
        for url, handler in self.handlers.items():
            handler.__enter__()
        return self

    def __exit__(self, exit_type, value, traceback):
        for url, handler in self.handlers.items():
            handler.__exit__(exit_type, value, traceback)
        self.running = False
        self.loop.stop()

    def run_thread(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.app = web.Application(loop=self.loop)
        for url, handler in self.handlers.items():
            self.app.router.add_get(url, handler.handle)
        web.run_app(self.app, port=self.port, handle_signals=False)

    def add_handler(url, handler):
        handlers[url] = handler
        handler.__enter__()
        self.app.router.add_get(url, handler.handle)
