import cv2 as cv
import numpy as np

img = cv.imread('/home/quentin/opencv-repo/src/Photos/cats.jpg')
cv.imshow('Cats', img)

#blank image defined by size of img
blank = np.zeros(img.shape, dtype='uint8')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Gray', gray)

blur = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)

canny = cv.Canny(blur, 125, 175)
cv.imshow('Canny Edges', canny)

#findContours returns 2 values
#contours - a list of all edges found
#heirarchies - the representation that opencv uses to find the contours
#cv.RETR_LIST - returns all found contours (RETR_EXTERNAL returns external contours, other options return other subsets)
#CHAIN_APPROX_NONE - sowan nothing, just returns all from RETR_LIST
#CHAIN_APPROX_NONE will give all points from a line
#CHAIN_APPROX_SIMPLE will compress the points from a line and compress it into just the endpoints
contours, heirarchies = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
#length of contours list is numbers of lines found
print(f'{len(contours)} contour(s) found!')
#Before blurring, this gives 2794 contours - thats a lot
#blurring beforehand with (5,5) kernalsize, it gives 380


#THRESHOLD - another method for finding lines
#if pixel intensity is below 125, black, above 125, white
#Binaries the image into black and white
#threshold isnt ideal, but useful and works well in right situation
ref, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
cv.imshow('Thresh', thresh)
contours2, heirarchies2 = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
print(f'{len(contours2)} contour(s) found!')
#839 contours

#drawing contours
#image to draw on, contours to draw, contour index (-1 is all), color, thickness
cv.drawContours(blank, contours, -1, (0,0,255), 1)
cv.imshow('Contours', blank)


cv.waitKey(0)