from sensors.sensor import Sensor
from time import time
import keras
#from keras import backend as K
import load_data
import cv2

verbose = False

class NNSensor(Sensor):
    
    def __init__(self):
        print("loading model")
        t = time()
        self.model = keras.models.load_model('./model.h5')
        print("time was: "+str(time()-t))
        print("model loaded")

    def read(self, frame):
        if frame is None:
            return set()
        reshaped = frame.reshape((1,) + frame.shape + (1,))

        t = time()
        results = self.model.predict(reshaped)
        print("Predicted in: "+str(time() - t))

        s = set()
        for i in range(len(load_data.KEYS)):
            if results[0][i]>0.5:
                s.add(load_data.KEYS[i])
        print("predicting" + str(s))
        if verbose:
            print("in shape:  {}".format(reshaped.shape))
            print("out shape: {}".format(results.shape))
            print("out vals:  {}".format(results))
            print("out set:   {}".format(s))
        return s

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

if __name__ == '__main__':
    verbose = True
    sensor = NNSensor()
    while True:
        print("test image index:")
        i = input()
        img = cv2.imread('./testdata/collected_data/lower/image{}.png'.format(i), cv2.IMREAD_GRAYSCALE)
        print(sensor.read(img))
