import cv2

# Initialize the camera capture
cap = cv2.VideoCapture(5)  # Use 0 for the default camera, or specify the camera index if you have multiple cameras

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

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

    cv2.imshow("Camera Feed", frame)
     # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


print("Width:", width)
print("Height:", height)

# Release the capture
cap.release()
cv2.destroyAllWindows()