from pipes.pipe import Pipe
import numpy as np
import cv2

class Shrinking(Pipe):
    def pipe(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        r = 100.0 / frame.shape[1]
        dim = (100, int(frame.shape[0] * r))
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        return frame

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        pass