import numpy as np
from picamera import PiCamera
from threading import Thread

from sensors.sensor import Sensor


class PiCameraSensor(Sensor):
    def __init__(self, resolution=(640, 480), internal_framerate=10):
        self.exited = False
        self.resolution = resolution
        self.internal_framerate = internal_framerate
        output_dimensions = (resolution[1], resolution[0], 3)
        self._last_frame = np.empty(output_dimensions, dtype=np.uint8)

    def _read_camera(self):
        current_frame = np.zeros_like(self._last_frame)
        camera = PiCamera(resolution=self.resolution, framerate=self.internal_framerate)
        for _ in camera.capture_continuous(current_frame, format='rgb', use_video_port=True):
            self._last_frame = current_frame.copy()
            if self.exited:
                break

    def __enter__(self):
        self.exited = False
        Thread(target=self._read_camera).start()
        return self

    def __exit__(self, type, value, traceback):
        self.exited = True

    def read(self):
        return self._last_frame
