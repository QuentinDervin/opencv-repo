import cv2 as cv
import numpy as np
#NOTE: Gradients are like edges in computer science

img = cv.imread('/home/quentin/opencv-repo/src/Photos/park.jpg')
cv.imshow('Park', img)

#blank image
blank = np.zeros(img.shape[:2], dtype='uint8')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


#Laplacian
#smudged pencil looking thing
#computes the gradients, uses the absolute value due to neessity of non-negative pixel values, as gray is a gradient of positive and negative
#image, depth
lap = cv.Laplacian(gray, cv.CV_64F)
lap = np.uint8(np.absolute(lap))
cv.imshow('Laplacian', lap)

#SOBEL
sobelx = cv.Sobel(gray, cv.CV_64F, 1, 0)
sobely = cv.Sobel(gray, cv.CV_64F, 0, 1)
combined_sobel = cv.bitwise_or(sobelx, sobely)

cv.imshow('Sobel X', sobelx)
cv.imshow('Sobel Y', sobely)
cv.imshow('Sobel X+Y', combined_sobel)


#CANNY
#canny multistage process uses sobel at a point
#Canny is a much cleaner version of the edges, and is why its usually used
canny = cv.Canny(gray, 150, 175)
cv.imshow('Canny', canny)


cv.waitKey(0)
