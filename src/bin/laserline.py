import cv2 as cv
import numpy as np
# import matplotlib.pyplot as plt


img = cv.imread("2inch.png")
cv.imshow('camera', img)
height, width, channels = img.shape

# Blank image
blank = np.zeros(img.shape[:2], dtype='uint8')

# Blurring step
bilateral = cv.bilateralFilter(img, 15, 100, 100)
#cv.imshow('Bilateral', bilateral)

# Convert the image to HSV color space
hsv = cv.cvtColor(bilateral, cv.COLOR_BGR2HSV)
cv.imshow("hsv red", hsv)

# Define lower and upper bounds for red color in HSV for Thresholding
lower_red = np.array([160, 100, 180])
upper_red = np.array([255, 135, 255])
#170-180 saturation, 100-135 hue, 180-255 value
#new 160 255, 100 135, 180 255

# Threshold mask for the HSV image to get only red colors
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

if len(y_values) > 0:
    mean_y = np.mean(y_values)
else:
    mean_y = 0

# Define a threshold distance from the mean
threshold = 10

# Filter out values that are too far from the mean
#filtered_y_values = [y for y in y_values if abs(y - mean_y) <= threshold]

y_sum = 0
for value in y_values:
    y_sum = y_sum + value

if y_sum > 0:
    y_avg = y_sum/len(y_values)
else:
    y_avg = 0

print(y_avg)

# Display the red line
#cv.imshow('Red Line', red_line)

#Look into edge detection prior hough for clearer output
canny = cv.Canny(red_line, 200, 250)
#cv.imshow('Canny Edges', canny)

#HoughTransformation
#threshold=25, minLineLength=20, maxLineGap=30 -------- works for broken lines
#HoughLines with 100 threshold worked fine for straight easy lines
lines = cv.HoughLinesP(canny, 1, np.pi/180, threshold=25, minLineLength=20, maxLineGap=30)  # Adjust parameters as needed

blank_img = np.zeros_like(img)

#Drawing lines for houghLinesP
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]  # Extract line coordinates
        cv.line(blank_img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Draw line on the blank image

# Display the result
cv.imshow('Hough Lines Detection', blank_img)

# # Plot histogram of y-values
# plt.hist(y_values, bins=50, color='r', alpha=0.7)
# plt.xlabel('Y-coordinate')
# plt.ylabel('Frequency')
# plt.title('Histogram of Lines')
# plt.grid(True)
# plt.show()

# # Count occurrences of each y-value
y_unique, y_counts = np.unique(y_values, return_counts=True)

# # Plot line graph of y-value counts
# plt.plot(y_unique, y_counts, color='r')
# plt.xlabel('Y-coordinate')
# plt.ylabel('Frequency')
# plt.title('Red Frequency')
# plt.grid(True)
# plt.show()

# Find peaks in the line graph manually
peaks = []
i = 1
while i < len(y_counts) - 1:
    if y_counts[i] > y_counts[i-1] and y_counts[i] > y_counts[i+1]:
        peaks.append(y_unique[i])
    elif y_counts[i] == y_counts[i-1]:
        if y_counts[i-1] > y_counts[i-2]:
            j = i
            z = i
            while j < len(y_counts) and y_counts[j] == y_counts[i]:
                j += 1
            if j < len(y_counts) and y_counts[j] < y_counts[j-1]:
                x = (j+z)//2
                peaks.append(y_unique[x])
            i = j
    i += 1


print(peaks)

for peak in peaks:
    distance = 2 * (1450/peak) -4
    print("Peak: An object is "+str(distance)+"cm away!")

blank_img_2 = np.zeros_like(img)
for peak in peaks:
    cv.line(blank_img_2, (0, peak), (width - 1, peak), (0, 0, 255), 1)

cv.imshow("blank line graph", blank_img_2)

interval_size = int(width/5)
print(interval_size)
interval_one = []
interval_two = []
interval_three = []
interval_four = []
interval_five = []
for pixel in line_pixels:
    x, y = pixel
    if x < interval_size:
        interval_one.append(pixel)
    elif x < 2*interval_size:
        interval_two.append(pixel)
    elif x < 3*interval_size:
        interval_three.append(pixel)
    elif x < 4*interval_size:
        interval_four.append(pixel)
    elif x < 5*interval_size:
        interval_five.append(pixel)    

intervals = [interval_one, interval_two, interval_three, interval_four, interval_five]
int = 1
for interval in intervals:
    sum = 0
    y_values = []
    # print(interval[0])
    # print(interval[-1])
    for pixel in interval:
        x, y = pixel
        y_values.append(y)
    mean_y = np.mean(y_values)

    center_distance = 2 * (1450/mean_y) -4
    #then here do some diagonal distance calc for some intervals
    true_distance = center_distance
    print("Interval "+str(int)+": An object is average "+str(true_distance)+"cm away with average pixel of"+str(mean_y)+"!")

    

    int = int + 1

# X value average in intervals check

int = 1
for interval in intervals:
    sum = 0
    x_values = []
    for pixel in interval:
        x, y = pixel
        x_values.append(x)
    mean_x = np.mean(x_values)
    print("Interval "+str(int)+": Average "+str(mean_x))
    int = int +1
            



cv.waitKey(0)

