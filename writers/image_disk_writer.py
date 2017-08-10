import cv2

from writers.writer import Writer


class ImageDiskWriter(Writer):
    def __init__(self, folder):
        self.folder = folder
        self.counter = 0

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        pass

    def write(self, data):
        cv2.imwrite("%s/image%03d.png" % (self.folder, self.counter), data)
        self.counter += 1
