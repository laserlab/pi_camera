# import the necessary packages
from picamera.array import PiRGBArray
from picamera.array import PiYUVArray
from picamera import PiCamera
from datetime import datetime
import time
import cv2
import socket
import io

# initialize the camera and grab a reference to the raw camera capture
with PiCamera() as camera:
	fheight = 1024
	fwidth = 768
	camera.resolution = (fheight, fwidth)
	camera.framerate = 24

	server_socket = socket.socket()
	server_socket.bind(('0.0.0.0', 8000))
    	server_socket.listen(0)
	print('opening socket')

	# Accept a single connection and make a file-like object out of it
	conn, addr = server_socket.accept()
	connection = conn.makefile('wb')
	print('conected to {}'.format(addr))
	# allow the camera to warmup
	#time.sleep(0.1)

	# capture frames from the camera
	#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	#image = frame.array

	# show the frame
	#cv2.imshow("Frame", image)
	try:		
		camera.start_recording(connection, format='h264', resize=(320,240))
		print('recording')
		while True:
			key = raw_input('command (? for help):')
			if key == '?':
				print('available commands:\r')
				print('q: ends programm\r')
				print('i: save image\r')
			if key == 'i': # save to file
				filename = 'pic'+datetime.now().strftime("%Y-%d-%m_%Hh%Mm%Ss")+'.png'
				camera.capture(filename, use_video_port=True)
				print('Saved to {}'.format(filename))
				camera.annotate_text = 'Saved to {}'.format(filename)
				camera.wait_recording(1) # wait one second to display annotation
				camera.annotate_text = ''
			if key == 'r': # save raw data
				#with PiYUVArray(camera, size=(fheight, fwidth)) as rawCapture:
				#	camera.capture(rawCapture, 'yuv')
				#	print(rawCapture.array.shape)
				stream = io.BytesIO()
				camera.capture(stream, format='jpeg', bayer=True)				
			# if the `q` key was pressed, break from the loop
			if key == 'q':
				break
        	camera.stop_recording()
		print('stopped recording')
 	finally:
		connection.close()
 		conn.close()
 		server_socket.close()
