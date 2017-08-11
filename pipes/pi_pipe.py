import cv2
import numpy as np
from pipes.pipe import Pipe

class PiPipe(Pipe):
	def pipe(self, data):
		gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
		gray = cv2.resize(gray, (50, 50))

		return gray

	def __enter__(self):
		return self

	def __exit__(self, exit_type, value, traceback):
		pass
