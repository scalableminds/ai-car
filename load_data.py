import cv2
import os
import numpy as np


def load_data(filename, folder):
    with open(filename, "rt") as file:
        csv_data = [set(line.strip().split(","))
                    for line in file if line.strip() != ""]

    count = len(csv_data)
    images = np.stack([cv2.imread("%s/image%03d.png" % (folder, i),
                       cv2.IMREAD_GRAYSCALE) for i in range(count)])

    return csv_data, images

if __name__ == '__main__':
    X, Y = load_data("test_images/classes.csv", "test_images")
    print(X, Y.shape)
