import cv2 as cv
import numpy as np

#creates a blank image, size 500 by 500, 3 color channels
blank = np.zeros((500,500,3), dtype='uint8')

cv.imshow('Blank', blank)

#COLOR THE WHOLE IMAGE
blank[:] = 0,255,0
#cv.imshow('Color', blank)

#to do a section filled in
blank[200:300, 300:400] = 0,0,255
#cv.imshow('Color', blank)

#DRAW A RECTANGLE
#rectangle(image, point1, point2, color, thickness)
cv.rectangle(blank, (0,0), (300, 300), (255, 155, 0), thickness=2)
#this fills in the rectangle, or -1 does it too
cv.rectangle(blank, (0,0), (250, 250), (0, 255, 255), thickness=cv.FILLED)
#can also scale using shape[0], shape[1]
cv.rectangle(blank, (0,0), (blank.shape[1]//5, blank.shape[0]//5), (0, 0, 200), thickness=cv.FILLED)
cv.imshow('Rectangle', blank)

#cricle(image, centerpoint, radius, color, thickness)
cv.circle(blank, (blank.shape[1]//2, blank.shape[0]//2), 40, (0, 0, 255), thickness=3)
cv.imshow('Circle', blank)

#line(image, point1, point2, color, thickness)
cv.line(blank, (0,0), (500,500), (255, 255, 255), thickness=10)
cv.imshow('Line', blank)


#TEXT
cv.putText(blank, 'Hello I am Jerry', (100, 255), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,0,100), thickness=2)
cv.imshow('Text', blank)


cv.waitKey(0)