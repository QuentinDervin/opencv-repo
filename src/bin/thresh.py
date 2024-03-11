import cv2 as cv
import numpy as np

img = cv.imread('/home/quentin/opencv-repo/src/Photos/cats.jpg')
cv.imshow('Cats', img)

#blank image
blank = np.zeros(img.shape[:2], dtype='uint8')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#SIMPLE Thresholding
#if its above 150, sets color to 255, otherwise set to 0
#downside is we have to specify a value manually
threshold, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)
cv.imshow('Simple Thresholded', thresh)

#inverse threshold
threshold, thresh_inv = cv.threshold(gray, 150, 255, cv.THRESH_BINARY_INV)
cv.imshow('Simple Thresholded Inverse', thresh_inv)


#ADAPTIVE Thresholding
#this allows the computer to determine a thresholding value itself
#image, max value color, adaptive method, threshold type, blocksize, C value
adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 3)
#creates an 11 by 11 window, determines a mean, and finds an optimal threshold value
#the higher the C, the more precise the image
cv.imshow("Adaptive Thresholding", adaptive_thresh)


cv.waitKey(0)