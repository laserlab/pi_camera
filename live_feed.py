# import the necessary packages
from picamera.array import PiRGBArray
from picamera.array import PiYUVArray
from picamera import PiCamera
from datetime import datetime
import time
#import cv2
import socket
import io

filepath = '/home/laserlab/git/pi_camera/pics/'

# initialize the camera and grab a reference to the raw camera capture
print('start Raspi Camera')
with PiCamera() as camera:
	print('Camera opened')
	fheight = 1024
	fwidth = 768
	camera.resolution = (fheight, fwidth)
	camera.framerate = 24
	#camera.awb_mode = 'off'
	print('opening socket')
	server_socket = socket.socket()
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind(('0.0.0.0', 8000))
    	server_socket.listen(0)
	print('waiting for connection ...')

	# Accept a single connection and make a file-like object out of it
	conn, addr = server_socket.accept()
	connection = conn.makefile('wb')
	print('conected to {}'.format(addr))
	cmd_conn_open = False
	# allow the camera to warmup
	#time.sleep(0.1)

	# capture frames from the camera
	#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	#image = frame.array

	# show the frame
	#cv2.imshow("Frame", image)
	key = ''
	n_key = ''
	try:		
		camera.start_recording(connection, format='h264', resize=(640,480))
		print('recording')
		while True:
			if key != 'n':
				key = raw_input('command (? for help):')
			if key == '?' or n_key == '?':
				print('available commands:\r')
				print('q: ends programm\r')
				print('i: save image\r')
			if key == 'i' or n_key == 'i': # save to file
				filename = 'pic'+datetime.now().strftime("%Y-%d-%m_%Hh%Mm%Ss")+'.png'
				camera.capture(filepath+filename, use_video_port=True)
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
			if key == 'x':
				camera.meter_mode = 'spot'
			if key in str(range(0,9)):
				#camera.framerate = 10/int(key)
				camera.iso = int(key) * 100
				print('ISO set to {}'.format(camera.iso))
			#enable network mode
			if key == 'n':
				if cmd_conn_open == False: 
					print('opening network control socket')
					cmd_socket = socket.socket()
					cmd_socket.bind(('0.0.0.0', 8001))
					cmd_socket.listen(0)
					print('waiting for network control')
					cmd_conn, cmd_addr = cmd_socket.accept()
					print('connected to {}'.format(cmd_addr))
					cmd_conn_open = True
				# read remote key press
				n_key = cmd_conn.recv(1)
			# if the `q` key was pressed, break from the loop
			if key == 'q' or n_key == 'q':
				break

        	camera.stop_recording()
		print('stopped recording')
 	finally:
		print('closing connections')
		if cmd_conn_open == True:
			cmd_conn.close()
			cmd_socket.shutdown(0)
			cmd_socket.close()
		connection.close()
 		conn.close()
		server_socket.shutdown(0)
 		server_socket.close()
		print('exiting')
