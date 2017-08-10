import cv2
import numpy as np
import pipe

class PiPipe(pipe.Pipe):
	def pipe(self, data):
		gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
		gray = cv2.resize(gray, (100, 100))

		return gray

	def __enter__(self):
		pass

	def __exit__(self):
		pass
