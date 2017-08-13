from aiohttp import web, WSMsgType
import asyncio 
import cv2

from handlers.handler import Handler
from writers.writer import Writer

class VideoHandler(Handler, Writer):
    def __init__(self):
        self.frame = None

    @asyncio.coroutine
    def handle(self, request):
        resp = web.StreamResponse(status=200, 
                                  reason='OK', 
                                  headers={'Content-Type': 'multipart/x-mixed-replace; boundary=frame'})
        
        # The StreamResponse is a FSM. Enter it with a call to prepare.
        yield from resp.prepare(request)
        
        while self.running:
            try:
                if self.frame is not None:
                    img = cv2.imencode('.jpg', self.frame)[1].tostring()
                else:
                    img = b""
                img_len = str.encode(str(len(img)))
                resp.write(b"--frame\r\n")
                resp.write(b"Content-Type: image/jpeg\r\n")
                resp.write(b"Content-length: " + img_len + b"\r\n\r\n")
                resp.write(img)
                
                # Yield to the scheduler so other processes do stuff.
                yield from resp.drain()
                 
                # Sleep for a bit..
                yield from asyncio.sleep(0.07)
            except Exception as e:
                # So you can observe on disconnects and such.
                print(repr(e))
                raise
        return resp

    def __enter__(self):
        self.running = True

    def __exit__(self, exit_type, value, traceback):
        self.running = False

    def write(self, data):
        self.frame = data
