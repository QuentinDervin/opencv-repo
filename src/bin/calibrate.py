import cv2
import numpy as np
import os

# Step 1: Camera calibration
# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Images for calibration
images_folder = 'images_calibration'

# Loop through the images in the folder
for filename in os.listdir(images_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"): # You can add more image formats if needed
        img = cv2.imread(os.path.join(images_folder, filename))

        # Get the size of the loaded image
        height, width = img.shape[:2]  # For grayscale images, use img.shape[:2]
        print(f"Loaded image {filename}: Height = {height}, Width = {width}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Define the chessboard size (number of inner corners)
        chessboard_size = (9, 6)  # Change this according to your chessboard

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
            objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
            objpoints.append(objp)
            imgpoints.append(corners)

# Calibrate the camera
ret, K, D, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Step 2: Undistort the image
def undistort_fisheye(img, K, D):
    h, w = img.shape[:2]
    new_K, roi = cv2.getOptimalNewCameraMatrix(K, D, (w, h), 1, (w, h))
    mapx, mapy = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, (w, h), cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, mapx, mapy, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    x, y, w, h = roi
    undistorted_img = undistorted_img[y:y+h, x:x+w]
    return undistorted_img

# np.save('camera_matrix.npy', K)
# np.save('distortion_coefficients.npy', D)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the folder containing the images
images_folder = os.path.join(script_dir, 'images_calibration')
# Path to the specific image relative to the script location
image_path = os.path.join(images_folder, 'img0.png')

# Load the distorted image
distorted_img = cv2.imread(image_path)

height, width = distorted_img.shape[:2]  # For grayscale images, use img.shape[:2]
print(f"Loaded distorted image {filename}: Height = {height}, Width = {width}")

D1 = D[:, :4]

print("Camera Matrix (K):\n", K)
print("Distortion Coefficients (D1):\n", D1)

# Undistort the image
undistorted_img = undistort_fisheye(distorted_img, K, D1)
height, width = undistorted_img.shape[:2]  # For grayscale images, use img.shape[:2]
print(f"Loaded unistorted image {filename}: Height = {height}, Width = {width}")

# Display the results
cv2.imshow('Distorted Image', distorted_img)
cv2.imshow('Undistorted Image', undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
