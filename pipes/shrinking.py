from pipes.pipe import Pipe
import numpy as np
import cv2

class Shrinking(Pipe):
    def pipe(self, data):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        r = 100.0 / gray.shape[1]
        dim = (100, int(gray.shape[0] * r))
        gray = cv2.resize(gray, dim, interpolation = cv2.INTER_AREA)
        return gray

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        pass