import cv2 as cv


#EXISTING VIDEO - rescales the image
def rescaleFrame(frame, scale=0.75):
    #shape[1] is width, shape[0] is height
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    
    #sets a dimensions tuple for return
    dimensions = (width,height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

#LIVE VIDEO
def changeRes(width,height):
    #3 references widht, 4 references height, other numbers reference other things
    #this works for only Live video (webcame, etc...)
    capture.set(3,width)
    capture.set(4,height)

#reads the image file
img = cv.imread('/home/quentin/opencv-repo/src/Photos/cat_large.jpg')

#resize image
resized_image = rescaleFrame(img, scale=0.2)

#shows the image file
cv.imshow('Cat', resized_image)

#putting 0 in VideoCapture will reference webcam, further numbers additional connected cameras
capture = cv.VideoCapture('/home/quentin/opencv-repo/src/Videos/dog.mp4')

while True:
    #grabs the video frame by frame using capture.read
    isTrue, frame = capture.read()

    #frame_resized
    frame_resized = rescaleFrame(frame)

    #displays each frame through cv.imshow
    cv.imshow('Video', frame)
    cv.imshow('Video Resized', frame_resized)

    #if the letter 'd' is pressed, exit loop and end video playback
    if cv.waitKey(20) & 0xFF==ord('d'):
        break
    #(-215:Assertion failed) - this code currently gets this error when the video runs out of frames
    #This error also occurs when the filepath does not lead to expected file


capture.release()
cv.destroyAllWindows
