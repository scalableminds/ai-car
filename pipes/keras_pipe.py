from pipes.pipe import Pipe
import keras
from load_data import KEYS

class KerasPipe(Pipe):

    def __init__(self, filename, threshold=0.5, verbose=False):
        self.model = keras.models.load_model(filename)
        self.threshold = threshold
        self.verbose = False

    def pipe(self, frame):
        if frame is None:
            return set()

        reshaped = frame.reshape((1,) + frame.shape + (1,))
        results = self.model.predict(reshaped)

        keys = set()
        for i in range(len(KEYS)):
            if results[0][i] > self.threshold:
                keys.add(KEYS[i])

        if self.verbose:
            print("in shape: {}".format(reshaped.shape))
            print("out shape: {}".format(results.shape))
            print("out vals: {}".format(results))
            print("out set: {}".format(keys))
        return keys


    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        pass