import cv2 as cv
import numpy as np
path = "Users/anton/ai-car/collected_data_4/image*.png"
img = cv.imread(path)
normalizedImg = np.zeros((800, 800))
normalizedImg = cv.normalize(img,  normalizedImg, 0, 255, cv.NORM_MINMAX)
cv.imwrite(normalizedImg, Users/ai-car/collected_data/x_test)
cv.waitKey(0)
cv.destroyAllWindows()