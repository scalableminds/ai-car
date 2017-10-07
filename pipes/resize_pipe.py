from pipes.pipe import Pipe
import numpy as np
import cv2

class ResizePipe(Pipe):
    def __init__(self, size, grayscale=True):
        self.size = size
        self.grayscale = grayscale

    def pipe(self, frame):
        if grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, self.size)
        return frame

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        pass
