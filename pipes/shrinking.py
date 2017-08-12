from pipes.pipe import Pipe
import numpy as np
import cv2

class Shrinking(Pipe):
    def pipe(self, data):
        data = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        r = 100.0 / data.shape[1]
        dim = (100, int(data.shape[0] * r))
        data = cv2.resize(data, dim, interpolation = cv2.INTER_AREA)
        return data

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        pass