import cv2 as cv
import numpy as np

img = cv.imread('/home/quentin/opencv-repo/src/Photos/cats 2.jpg')
cv.imshow('Cats', img)

#blank image - note the images have to be the same size to mask (thus img.shape)
blank = np.zeros(img.shape[:2], dtype='uint8')

#Masking - focusing on certain parts of an image (image with people, focus on faces)
circle = cv.circle(blank.copy(), (img.shape[1]//2,img.shape[0]//2), 100, 255, -1)
cv.imshow('Mask', circle)

rectangle = cv.rectangle(blank.copy(), (30,30), (370,370), 255, -1)

weird_shape = cv.bitwise_xor(circle, rectangle)


masked = cv.bitwise_and(img,img,mask=weird_shape)
cv.imshow('Weird Shaped Masked Image', masked)

cv.waitKey(0)
