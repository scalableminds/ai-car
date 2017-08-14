from aiohttp import web, WSMsgType
import asyncio

from handlers.handler import Handler

class FileHandler(Handler):
    def __init__(self, file):
        self.file = file

    @asyncio.coroutine
    def handle(self, request):
    	return web.FileRespone(file)

    def __enter__(self):
        pass

    def __exit__(self, exit_type, value, traceback):
        pass
