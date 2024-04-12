import cv2 as cv
import numpy as np

img = cv.imread('/home/quentin/opencv-repo/src/Photos/park.jpg')
cv.imshow('Park', img)

blank = np.zeros(img.shape[:2], dtype='uint8')

#This splits the images colors into BGR
b,g,r = cv.split(img)

#The darker it is, the less intensity the color, the lighter, the more of that color
#for blue, the sky will be very light, but the green trees will be very dark (cus very little blue)
cv.imshow('Blue', b)
cv.imshow('Red', r)
cv.imshow('Green', g)

#Notice the shape is 1 for the tuples, becase they are displayed as greyscale
print(img.shape)
print(b.shape)
print(r.shape)
print(g.shape)

#this colors the brightness/darkness distribution
blue = cv.merge([b,blank,blank])
red = cv.merge([blank,blank,r])
green = cv.merge([blank,g,blank])
cv.imshow('BlueB', blue)
cv.imshow('RedR', red)
cv.imshow('GreenR', green)

merged = cv.merge([b,g,r])
cv.imshow('Merged', merged)

cv.waitKey(0)