import cv2 as cv
import numpy as np

#NOTE: pixel off with value of 0, on with value of 1

blank = np.zeros((400,400), dtype='uint8')

rectangle = cv.rectangle(blank.copy(), (30,30), (370,370), 255, -1)
circle = cv.circle(blank.copy(), (200,200), 200, 255, -1)

cv.imshow('Rectangle', rectangle)
cv.imshow('Circle', circle)


#bitwise AND --> intersecting regions
#returns common regions of both
bitwise_and = cv.bitwise_and(rectangle, circle)
cv.imshow('Bitwise And', bitwise_and)

#Bitwise OR --> intersecting and non-intersecting regions
#returns the combination where either of them are
bitwise_or = cv.bitwise_or(rectangle, circle)
cv.imshow('Bitwise Or', bitwise_or)

#Bitwise XOR --> non-intersecting regions
#Where only one or the other is without the other
bitwise_xor = cv.bitwise_xor(rectangle, circle)
cv.imshow('Bitwise XOR', bitwise_xor)

#Bitwise NOT --> inverts binary color

bitwise_not = cv.bitwise_not(rectangle)
cv.imshow('Rectangle Not', bitwise_not)


cv.waitKey(0)
