import time

from handlers.video_handler import VideoHandler
from handlers.key_handler import KeyHandler
from handlers.file_handler import FileHandler
from server import Server
from sensors.pi_camera_sensor import PiCameraSensor
from writers.motor_writer import MotorWriter
from pipes.resize_pipe import ResizePipe

def transform(keys):
    x = 0
    if 'LEFT' in keys:
        x = 1
    elif 'RIGHT' in keys:
        x = -1

    y = 0
    if 'UP' in keys:
        y = 1
    elif 'DOWN' in keys:
        y = -1

    return x, y

def main():
    vid_handler = VideoHandler()
    key_handler = KeyHandler()
    file_handler = FileHandler("index.html")

    with PiCameraSensor(resolution=(64, 48)) as cam, \
        Server(handlers={
            "/": file_handler,
            "/video": vid_handler,
            "/socket": key_handler 
        }, port=8080) as server, \
        MotorWriter(frequency=100, speed=0.6) as motor_writer, \
        ResizePipe(size=(64, 48), grayscale=True) as resize_pipe:
            while True:
                try:
                    frame = cam.read()
                    frame = resize_pipe.pipe(frame)
                    keys = transform(key_handler.read())
                    motor_writer.write_num(keys[0], keys[1])               
                    vid_handler.write(frame)
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    break

if __name__ == '__main__':
    main()
