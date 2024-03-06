import cv2 as cv

img = cv.imread('/home/quentin/opencv-repo/src/Photos/park.jpg')
#cv.imshow('Cat', img)

#Converting to grayscale
#cv,COLOR_ has lots of conversion options
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#cv.imshow('Gray', gray)

#BLUR
#the kernl has to be odd numbers
blur = cv.GaussianBlur(img, (7,7), cv.BORDER_DEFAULT)
#cv.imshow('Blur', blur)

#Edge Cascade
#a lot of blurring and grading computations
#Note that passing in the blurred version decreases excess line
canny = cv.Canny(img, 125, 175)
#cv.imshow("Canny Edges", canny)
cannyblur = cv.Canny(blur, 125, 175)
cv.imshow("Canny Blur Edges", cannyblur)

#Dilating the image
#kinda makes the lines thicker
dilated = cv.dilate(cannyblur, (7,7), iterations=3)
#cv.imshow('Dilated', dilated)

#Eroding
#by eroding the same as you dilated, you will get the original cascade back
eroded = cv.erode(dilated, (7,7), iterations=3)
#cv.imshow('Eroded', eroded)

#Resize image
resized = cv.resize(img, (500, 500), interpolation=cv.INTER_CUBIC)
cv.imshow('Resized', resized)

#Cropping
cropped = img[50:200, 200:400]
cv.imshow('Cropped', cropped)


cv.waitKey(0)