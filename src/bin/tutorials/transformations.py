import cv2 as cv
import numpy as np

img = cv.imread('/home/quentin/opencv-repo/src/Photos/park.jpg')

cv.imshow('Boston', img)

#TRANSLATION
def translate(img, x, y):
    #a matrix that defines the translation. Changing the x and y values below affects the translation
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, transMat, dimensions)

#-x values --> left
#-y values --> up
#x --> right
#y --> down

translated = translate(img, -100, 100)
cv.imshow('Translated', translated)

#ROTATION
def rotate(img, angle, rotPoint=None):
    (height,width) = img.shape[:2]

    if rotPoint is None:
        rotPoint = (width//2,height//2)

    #The 1.0 is a scale factor, bigger number means bigger
    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width,height)

    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img, 45)
cv.imshow('Rotated', rotated)
#notice that rotating rotated images no longer keep the data off the page, so the black triangle edges will carry over
#rotated_rotated = rotate(rotated, 45)
#cv.imshow('Rotated Rotated', rotated_rotated)


#RESIZE
resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow('Resized', resized)

#FLIPPING
#number can be 0, 1, -1
#1 -- horizontal over y axis
#-1 -- both vertical and horizontal
#0 -- vertical flip over x axis
flip = cv.flip(img, 1)
cv.imshow('Flip', flip)

#Cropping AGAIN
cropped = img[50:200, 200:400]
cv.imshow('Cropped', cropped)


cv.waitKey(0)