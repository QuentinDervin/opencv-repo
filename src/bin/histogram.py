import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('/home/quentin/opencv-repo/src/Photos/cats.jpg')
cv.imshow('Cats', img)

#blank image
blank = np.zeros(img.shape[:2], dtype='uint8')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

circle = cv.circle(blank, (img.shape[1]//2,img.shape[0]//2), 100, 255, -1)
mask = cv.bitwise_and(gray,gray, mask=circle)

#Grayscale Histogram
#image list, channels, mask (only a portion of image?), histsize (the number of bins), range of pixel values
gray_hist = cv.calcHist([gray], [0], mask, [256], [0,256])

plt.figure()
plt.title('Grayscale Histogram')
plt.xlabel('Bins')
plt.ylabel('# of pixels')
plt.plot(gray_hist)
plt.xlim([0,256])
plt.show()
#there are close to 4000 pixels that have an intensity of 50 for Cats
#cats2 has a peak around 230 cus image is mostly white


#COLOR Historgram

plt.figure()
plt.title('Color Histogram')
plt.xlabel('Bins')
plt.ylabel('# of pixels')
colors = ('b', 'g', 'r')
for i,col in enumerate(colors):
    hist = cv.calcHist([img], [i], circle, [256], [0,256]) #Note: you use the circle directly instead of the mask like before
    plt.plot(hist, color=col)
    plt.xlim([0,256])
plt.show()
#This shows a histogram for each color channel

cv.waitKey(0)