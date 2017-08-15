import cv2
import os
import numpy as np

KEYS = ["LEFT", "RIGHT", "UP", "DOWN"]
def keys2bitmap(keys):
    return np.float32([k in keys for k in KEYS])

def load_data(filename, folder):
    with open(filename, "rt") as file:
        csv_data = [set((x for x in line.strip().split(",") if x.strip()!='')) for line in file]
    #csv_data = csv_data[0:-1]
    count = len(csv_data)
    X, Y = ([], [])
    #X = np.stack([cv2.imread(folder + f, cv2.IMREAD_GRAYSCALE) for f in os.listdir(folder)])
    #Y = np.stack([keys2bitmap(line) for line in csv_data])
    
    for f in os.listdir(folder):
        ind = int(f[5:10]) # the index
        if len(csv_data[ind])==0 or "DOWN" in csv_data[ind]:
            continue

        img = cv2.imread(folder + f, cv2.IMREAD_GRAYSCALE)
        X.append(img)
        X.append(np.fliplr(img))
        
        assert ind <= len(csv_data)

        bitmap = keys2bitmap(csv_data[ind])

        print("Index: {} keys: {} {}"
              .format(f[5:10], bitmap, ','.join(csv_data[ind])))
        Y.append(bitmap)
        flipped_bitmap = np.array(bitmap)
        if flipped_bitmap[0] == 1:
            flipped_bitmap[0] = 0
            flipped_bitmap[1] = 1
        elif flipped_bitmap[1] == 1:
            flipped_bitmap[1] = 0
            flipped_bitmap[0] = 1

        Y.append(flipped_bitmap)
        
    return np.array(X), np.array(Y)

if __name__ == '__main__':
    X, Y = load_data("classes.csv", "trainingsdata/collected_data/lower/")
