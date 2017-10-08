import time
import cv2

from handlers import *
from server import Server
from sensors import *
from writers import *
from pipes.resize_pipe import ResizePipe
from datetime import datetime
import os

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
        MotorWriter() as motor_writer, \
        ResizePipe(size=(64, 48), grayscale=True) as resize_pipe:
            drive_pwm_count = 4
            drive_pwm_high = 2
            drive_pwm = 0
            while True:
                try:
                    frame = cam.read()
                    frame = resize_pipe.pipe(frame)
                    _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
                    left = np.count_nonzero(frame[:, :32])
                    right = np.count_nonzero(frame[:, 32:])
                    direction = (right - left) / 1536.0

                    keys = set() # keys = key_handler.read()
                    if drive_pwm < drive_pwm_high:
                      keys.add('UP')
                    drive_pwm = (drive_pwm + 1) % drive_pwm_count

                    if abs(direction) > 0.15:
                      if direction < 0:
                        keys.add('RIGHT')
                      else:
                        keys.add('LEFT')

                    print(keys)
                    motor_writer.write(keys)
                    vid_handler.write(frame)
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    break

if __name__ == '__main__':
    main()
