import cv2 as cv
import numpy as np

img = cv.imread('/home/quentin/opencv-repo/src/Photos/park.jpg')
cv.imshow('Park', img)

#blank image
blank = np.zeros(img.shape[:2], dtype='uint8')

cv.waitKey(0)
