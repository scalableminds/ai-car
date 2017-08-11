import cv2
import numpy as np
from pipes.pipe import *

class CoPilot(Pipe):
    def pipe(self, frame, threshold = 10):
        frame = cv2.blur(frame, (5, 5))
        frame = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                      cv2.THRESH_BINARY,5, 0)

        #_, frame = cv2.threshold(frame, 160, 255, cv2.THRESH_BINARY)
        frame = cv2.medianBlur(frame, 5)
        #cv2.imshow("to", frame)
        thirds = (int(frame.shape[0] * 0.33), int(frame.shape[1] * 0.33))

        l = frame[thirds[0]:-thirds[0], 0:thirds[1]]
        r = frame[thirds[0]:-thirds[0], -thirds[1]:-1]

        l_avg = np.average(l)
        r_avg = np.average(r)

        #print(l_avg, r_avg)

        l = cv2.resize(l, None, None, 5, 5)
        r = cv2.resize(r, None, None, 5, 5)

        #cv2.imshow("l", l)
        #cv2.imshow("r", r)
        #cv2.waitKey(10)

        if l_avg > r_avg + threshold:
            return "RIGHT"
        elif r_avg > l_avg + threshold:
            return "LEFT"


    def __init__(self):
        pass

    def __enter__(self):
        return self


    def __exit__(self, exit_type, value, traceback):
        pass


#CoPilot.correct(np.hstack((np.ones((500, 500)), np.zeros((500, 500)))))

