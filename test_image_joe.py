# import packages
from picamera.array import PiRGBArray
from fractions import Fraction
import picamera
import time
import cv2

 
# initialize the camera and grab a reference to the raw camera capture
#camera = PiCamera()

#camera.resolution = (2592, 1944)
#camera.shutter_speed = 1000

#rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
#time.sleep(0.1)
 
# grab an image from the camera
#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array
 
# display the image on screen and wait for a keypress
#cv2.imshow("Image", image)
#cv2.waitKey(0)

#cv2.imwrite('pic.jpg',image)

#print camera.resolution, camera.shutter_speed

with picamera.PiCamera(resolution = (2592, 1944), framerate = Fraction(1,6)) as camera:
    camera.sleep(10)
    camera.shutter_speed = camera.exposure_speed
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    camera._exposure_mode = 'off'
    # Finally, take several photos with the fixed settings

    for i in range(1, 7):
	camera.shutter_speed = i * 100000
	camera.capture('image_%02d.jpg' % i)
