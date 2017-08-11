import cv2
import numpy as np
from pipes.pipe import *

class CoPilot(Pipe):
	def pipe(self, frame):
		l = frame[:,0:int(frame.shape[1]*0.33):]
		r = frame[:,-int(frame.shape[1]*0.33):-1:]

		l_avg = np.average(l)
		r_avg = np.average(r)

		print(l_avg, r_avg)

    def __init__(self):
        pass

    def __enter__(self):
        return self


    def __exit__(self, exit_type, value, traceback):
        pass
CoPilot.correct(np.hstack((np.ones((500, 500)), np.zeros((500, 500)))))

