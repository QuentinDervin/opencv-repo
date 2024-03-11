import cv2 as cv

img = cv.imread('/home/quentin/opencv-repo/src/Photos/cats.jpg')
cv.imshow('Cats', img)

#kernel - 'window' that goes over a portion of an image, the window size is the kernel size
#the blur effects the middle pixel as a result of surrounding pixels (why it has to be odd number for kernel)

#AVERAGING
#calculates the middle pixel based on the surrounding pixels
average = cv.blur(img, (7,7))
cv.imshow('Average Blur', average)

#GAUSSIAN
#Each surrounding pixel has a different weight for how it influences the middle pixel
#More natural blurring, but less blurry
#the third parameter is the standard deviation in the x direction
gauss = cv.GaussianBlur(img, (7,7), 0)
cv.imshow("Gaussian", gauss)

#MEDIAN BLUR
#Same as averaging, but instead of average of surround, it finds the median
#more effective at eliminating noise than average and even gaussian
#Used in advanced comp projects that need to reduce substantial noice
median = cv.medianBlur(img, 3) #just an integer, cv assumes kernal size from the integer
#not meant for higher kernal sizes like 7 or even 5
cv.imshow('Median', median)

#BILATERAL BLUR
#The most effective, used because of how it blurs
#other blur irregardless of edges
#bilateral applies blurring whilst retaining the edges
#image, diameter int, sigmacolor (highervalue means more colors in neightborhood considred), sigmaSpace(how much further pixels influence pixel)
#higher values, more blur
bilateral = cv.bilateralFilter(img, 10, 35, 25)
cv.imshow('Bilateral', bilateral)

cv.waitKey(0)