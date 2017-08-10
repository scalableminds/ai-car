import cv2
from threading import Thread
from time import sleep

from sensors.sensor import Sensor


class Webcam(Sensor):
    def __enter__(self):
        self.cam = cv2.VideoCapture(0)
        self.ready = self.cam.isOpened()
        return self

    def __exit__(self, exit_type, value, traceback):
        self.ready = False
        self.cam.release()

    def read(self):
        if self.ready:
            self.ready, frame = self.cam.read()
            return frame
        else:
            return None
