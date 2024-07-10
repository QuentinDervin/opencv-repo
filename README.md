# opencv-repo
Repository for OpenCV tutorial projects leading to the ESP-32 Camera-Laser current prototype.
All relevant Files are in the Arduino Folder. These were run through the Arduino IDE.

The SRC and Docker folders contain out-of-date python scripts used for earlier testing.

In the Overview image, you can see an overview of the current prototype.
The laser is powered by the battery pack using two standard AAA batteries. 
The camera and ESP-32 are powered by the USB cord. 
The USB cord is plugged into a computer for transferring files and for powering.

The ESP-32 is covered in electrical tape as to insulate it from the play-do.
Play-do is used to hold the pieces together.

In the Prototype image, you can see the laser at the base and the camera angled downwards.
The exact angle is not measured.

On the Front View image, you can see the camera filter used to filter the light the camera sees.
The Filtered View image shows what that filtered image looks like.

Running the GrayscaleESP.ino will run code that will output a distance.
Changing the angle and distance between the physical laser and camera would result in inaccurate distance measurements.
