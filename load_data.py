import cv2
import os
import numpy as np

KEYS = ["LEFT", "RIGHT", "UP", "DOWN"]
def keys2bitmap(keys):
    return np.float32([k in keys for k in KEYS])

def load_data(filename, folder):
    with open(filename, "rt") as file:
        csv_data = [set(line.strip().split(",")) for line in file]

    csv_data = csv_data[0:-1]
    count = len(csv_data)
    X = np.stack([cv2.imread("%s/image%05d.png" % (folder, i),
                       cv2.IMREAD_GRAYSCALE) for i in range(count)])
    
    Y = np.stack([keys2bitmap(line) for line in csv_data])
    return X, Y

if __name__ == '__main__':
    X, Y = load_data("test_images/classes.csv", "test_images")
    print(X, Y.shape)
