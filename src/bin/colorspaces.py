import cv2 as cv
#import matplotlib.pyplot as plt

img = cv.imread('/home/quentin/opencv-repo/src/Photos/park.jpg')
cv.imshow('Park', img)

#CV default is BGR
#plt.imshow(img) #displays BGR as RGB so colors inverted
#plt.show()

#BGR to Gray
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

#BGR to HSV (Hue saturation value, how humans think and see color)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
cv.imshow('HSV', hsv)

#BGR TO L*a*b
lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
cv.imshow('LAB', lab)


#BGR to RGB
rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
cv.imshow('RGB', rgb)
#now using image in plt will show the colors not inverted

#NOTE: cannot change HSV to LAB, have to change HSV-BGR, BGR-LAB

cv.waitKey(0)