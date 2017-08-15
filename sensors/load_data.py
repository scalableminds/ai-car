import cv2
import os
import numpy as np

KEYS = ["LEFT", "RIGHT", "UP", "DOWN"]
def keys2bitmap(keys):
    return np.float32([k in keys for k in KEYS])

def load_data(filename, folder):
    with open(filename, "rt") as file:
        csv_data = [set(line.strip().split(",")) for line in file]
    #csv_data = csv_data[0:-1]
    count = len(csv_data)
    X, Y = ([], [])
    #X = np.stack([cv2.imread(folder + f, cv2.IMREAD_GRAYSCALE) for f in os.listdir(folder)])
    #Y = np.stack([keys2bitmap(line) for line in csv_data])
    for f in os.listdir(folder):
        img = cv2.imread(folder + f, cv2.IMREAD_GRAYSCALE)
        X.append(img)
        ind = int(f[5:10]) # the index
        assert ind <= len(csv_data) 
        print("Index: "+str(ind)+"  keys:"+(','.join(csv_data[ind])))
        Y.append(keys2bitmap(csv_data[ind]))
    return np.array(X), np.array(Y)

if __name__ == '__main__':
    X, Y = load_data("classes.csv", "trainingsdata/collected_data/lower/")