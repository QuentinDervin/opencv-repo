import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread('/home/quentin/Documents/my_first_simulation/controllers/camera_image_grabber/L2CM_C7CM/CAM_BROKE2.jpg')
cv.imshow('camera', img)

#blank image
blank = np.zeros(img.shape[:2], dtype='uint8')

bilateral = cv.bilateralFilter(img, 15, 100, 100)
cv.imshow('Bilateral', bilateral)

# Convert the image to HSV color space
hsv = cv.cvtColor(bilateral, cv.COLOR_BGR2HSV)
cv.imshow("hsv red", hsv)

# Define lower and upper bounds for red color in HSV
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])


# Threshold the HSV image to get only red colors
mask = cv.inRange(hsv, lower_red, upper_red)

# Bitwise-AND mask and original image
red_line = cv.bitwise_and(img, img, mask=mask)

contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Extract pixel locations of the red line
line_pixels = []
y_values = []
for contour in contours:
    for point in contour[:, 0]:
        line_pixels.append((point[0], point[1]))
        y_values.append(point[1])

mean_y = np.mean(y_values)

# Define a threshold distance from the mean
threshold = 10

# Filter out values that are too far from the mean
filtered_y_values = [y for y in y_values if abs(y - mean_y) <= threshold]

y_sum = 0
for value in filtered_y_values:
    y_sum = y_sum + value
y_avg = y_sum/len(y_values)
# print(np.mean(filtered_y_values))
# print(y_avg)
# print("Filtered y-values:", filtered_y_values)
# print(len(y_values))
# print(len(filtered_y_values))

# Display the red line
cv.imshow('Red Line', red_line)

#Look into edge detection prior hough
canny = cv.Canny(red_line, 200, 250)
cv.imshow('Canny Edges', canny)


#Making a white line on blank image with average y value of red line
# blank = np.zeros(img.shape[:2], dtype='uint8')
# cv.line(blank, (0,int(y_avg)), (640,int(y_avg)), (255, 255, 255), thickness=1)
# cv.imshow('Line', blank)

#HoughTransformation
#threshold=25, minLineLength=20, maxLineGap=30 -------- works for broken lines
#HoughLines with 100 threshold worked fine for straight easy lines
lines = cv.HoughLinesP(canny, 1, np.pi/180, threshold=25, minLineLength=20, maxLineGap=30)  # Adjust parameters as needed

blank_img = np.zeros_like(img)
# Draw detected lines on the original image --- Normal HoughLines
# if lines is not None:
#     for line in lines:
#         rho, theta = line[0]  # Extract rho and theta values
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a * rho
#         y0 = b * rho
#         x1 = int(x0 + 640 * (-b))
#         y1 = int(y0 + 640 * (a))
#         x2 = int(x0 - 640 * (-b))
#         y2 = int(y0 - 640 * (a))
#         cv.line(blank_img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Draw line on the original image

#Drawing lines for houghLinesP
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]  # Extract line coordinates
        cv.line(blank_img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Draw line on the blank image

# Display the result
cv.imshow('Hough Lines Detection', blank_img)

# height, width, channels = img.shape

# print("Image width:", width)
# print("Image height:", height)
# print("Number of channels:", channels)

# # Convert the image to grayscale
# gray_img = cv.cvtColor(blank_img, cv.COLOR_BGR2GRAY)
# cv.imshow('gray hough', gray_img)
# #create mask
# mask = gray_img > 0
# # Calculate histogram
# hist = cv.calcHist([gray_img], [0], mask.astype(np.uint8), [256], [0,256])

# # Plot histogram
# plt.plot(hist)
# plt.xlabel('Pixel Intensity')
# plt.ylabel('Frequency')
# plt.title('Histogram of Pixel Intensities')
# plt.show()

# Plot histogram of y-values
plt.hist(filtered_y_values, bins=50, color='r', alpha=0.7)
plt.xlabel('Y-coordinate')
plt.ylabel('Frequency')
plt.title('Histogram of Lines')
plt.grid(True)
plt.show()

# Sort y-values
filtered_y_values.sort()

# Count occurrences of each y-value
y_unique, y_counts = np.unique(y_values, return_counts=True)

# Plot line graph of y-value counts
plt.plot(y_unique, y_counts, color='r')
plt.xlabel('Y-coordinate')
plt.ylabel('Frequency')
plt.title('Red Frequency')
plt.grid(True)
plt.show()
cv.waitKey(0)