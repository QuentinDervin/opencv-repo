import cv2 as cv
import numpy as np
import time

# Initialize the camera capture
cap = cv.VideoCapture(0, cv.CAP_DSHOW)  # Use 0 for the default camera, or specify the camera index if you have multiple cameras
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    height, width, channels = frame.shape

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    cv.imshow("Camera Feed", frame)

    blank = np.zeros(frame.shape[:2], dtype='uint8')

    #Blurring step
    bilateral = cv.bilateralFilter(frame, 15, 100, 100)
    #cv.imshow('Bilateral', bilateral)

    # Convert the image to HSV color space
    hsv = cv.cvtColor(bilateral, cv.COLOR_BGR2HSV)
    #cv.imshow("hsv red", hsv)

    # Define lower and upper bounds for red color in HSV for Thresholding
    # #CHANGED TO 80%
    # lower_red = np.array([0, 20, 20])
    # upper_red = np.array([10, 255, 255])
    lower_red = np.array([160, 100, 180])
    upper_red = np.array([255, 135, 255])
    #170-180 saturation, 100-135 hue, 180-255 value
    #new 160 255, 100 135, 180 255

    # Threshold mask for the HSV image to get only red colors
    mask = cv.inRange(hsv, lower_red, upper_red)

    #   Bitwise-AND mask and original image
    red_line = cv.bitwise_and(frame, frame, mask=mask)

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

    if len(y_values) > 0:
        y_sum = np.sum(y_values)
        y_avg = y_sum / len(y_values)
    else:
        y_avg = 0 

    print("Y-Average: "+str(y_avg))

    # Display the red line
    #    cv.imshow('Red Line', red_line)

    #Look into edge detection prior hough for clearer output
    canny = cv.Canny(red_line, 200, 250)
    cv.imshow('Canny Edges', canny)

        #HoughTransformation
    #threshold=25, minLineLength=20, maxLineGap=30 -------- works for broken lines
    #HoughLines with 100 threshold worked fine for straight easy lines
    lines = cv.HoughLinesP(canny, 1, np.pi/180, threshold=25, minLineLength=20, maxLineGap=30)  # Adjust parameters as needed

    blank_img = np.zeros_like(frame)

    #Drawing lines for houghLinesP
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]  # Extract line coordinates
            cv.line(blank_img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Draw line on the blank image


    y_unique, y_counts = np.unique(y_values, return_counts=True)

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


    # print(peaks)
    

    # for peak in peaks:
    #     distance = 2 * (1450/peak) -4
    #     print("An object is "+str(distance)+"cm away!")

    blank_img_2 = np.zeros_like(frame)
    for peak in peaks:
        cv.line(blank_img_2, (0, peak), (width - 1, peak), (0, 0, 255), 1)

    interval_size = 384
    print("Interval Size: "+str(interval_size))
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

    intervals = [interval_three]
    int = 1
    for interval in intervals:
        sum = 0
        y_values = []
        for pixel in interval:
            x, y = pixel
            y_values.append(y)
        mean_y = np.mean(y_values)

        # center_distance = 2 * (1450/mean_y) -4

        # center_distance = (60 * (2.7**(3.2-mean_y)))
        # center_distance = (-1*(math.log((mean_y+40)/60, 2.7))) + 3.1

        if 1280>=mean_y>=1025:
            center_distance = (mean_y-1280)/(-1020)
        elif 1025>mean_y>=592:
            center_distance = (mean_y-1169.33)/(-577.33)
        elif 592>mean_y>=247:
            center_distance = (mean_y-1282)/(-690)
        elif 247>mean_y>=101.5:
            center_distance = (mean_y-683.5)/(-291)
        elif 101.5>mean_y>0:
            center_distance = (mean_y-219.7)/(-59.1)
        else:
            center_distance = None


    
        print("Middle Interval "+str(int)+": An object is average "+str(center_distance)+"cm away with average pixel height of"+str(mean_y)+"!")

        

        int = int + 1

    # Check for 'q' key press to exit
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(1)

# Release the capture and close all OpenCV windows
cap.release()
cv.destroyAllWindows()
