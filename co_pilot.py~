import cv2
import numpy as np


class CoPilot:
	def correct(frame):
		l = frame[:,0:int(frame.shape[1]*0.33):]
		r = frame[:,-int(frame.shape[1]*0.33):-1:]

		l_avg = np.average(l)
		r_avg = np.average(r)

		print(l_avg, r_avg)

CoPilot.correct(np.hstack((np.ones((500, 500)), np.zeros((500, 500)))))

