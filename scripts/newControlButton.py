import time
import json
import requests
import RPi.GPIO as GPIO
import gps
import picamera

import datetime
import os

#Changes
ledRequestSendPhoto = 6
ledPhotoViewed = 13

buttonTakePhoto = 16
#buttonGPS = 21
#buttonWIFI = 20

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ledRequestSendPhoto, GPIO.OUT)
GPIO.setup(ledPhotoViewed, GPIO.OUT)

GPIO.output(ledRequestSendPhoto, False)
GPIO.output(ledPhotoViewed, False)

GPIO.setup(buttonTakePhoto, GPIO.IN, GPIO.PUD_UP)


GPIO.setwarnings(False)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url_get_new_clicks = 'http://lia-wearable-fullcontrol.meteor.com/getNewClicks'
url_get_new_photo = 'http://lia-wearable-fullcontrol.meteor.com/getLastClick'
url_clean_clicks = 'http://lia-wearable-fullcontrol.meteor.com/cleanClicks'
url_add_data = 'http://lia-wearable-fullcontrol.meteor.com/addDatum'
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

PhotoRequestCounter = 0


b = requests.post(url_clean_clicks, data=json.dumps({'auth':'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'}), headers=headers)

def savePhoto():
	global PhotoRequestCounter
	url = 'http://lia.dc.ufscar.br/image_upload/fileupload.php'
	files = {'file': open('/home/pi/scripts/photos/image'+str(PhotoRequestCounter)+'.jpg', 'rb')}
	f = requests.post(url, files=files)
	
def sendPhoto():
	global PhotoRequestCounter
	path = 'image'+str(PhotoRequestCounter)+'.jpg'

#last lat position
	configlat = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlatJson = json.load(configlat)
	lat = configlatJson['lat']
	configlat.close()

#last lon position
	configlng = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlngJson = json.load(configlng)
	lng = configlngJson['lon']
	configlng.close()
	

	dataPhoto = {'auth': auth, 'lat': lat, 'lng': lng, 'display':0, 'extra':{'type': 1, 'path': path}}
	r = requests.post(url_add_data, data=json.dumps(dataPhoto), headers = headers)

def sendPhotoGPS():
	global PhotoRequestCounter
	path = 'image'+str(PhotoRequestCounter)+'.jpg'

#last lat position
	configlat = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlatJson = json.load(configlat)
	lat = configlatJson['lat']
	configlat.close()

#last lon position
	configlng = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlngJson = json.load(configlng)
	lng = configlngJson['lon']
	configlng.close()


	dataPhotoGPS = {'auth': auth, 'lat': lat, 'lng': lng, 'display':1, 'extra':{'type': 1, 'path': path}}
	r = requests.post(url_add_data, data=json.dumps(dataPhotoGPS), headers = headers)

def takePhoto():
	global PhotoRequestCounter
	with picamera.PiCamera() as camera:
		try:
			path = '/home/pi/scripts/photos/image'+str(PhotoRequestCounter)+'.jpg'
			camera.start_preview()
			time.sleep(3)
			camera.capture(path)
			camera.stop_preview()
		except:
			print("Could not take the photo")
	savePhoto()	
	sendPhotoGPS()
	PhotoRequestCounter += 1		


def authorizePhoto():
	print("botton authorize pressed")
	GPIO.output(ledRequestSendPhoto, False)
	takePhoto()


GPIO.add_event_detect(buttonTakePhoto, GPIO.FALLING, bouncetime = 200)


while True:
	r = requests.post(url_get_new_photo, headers=headers)
	if (r.content == "clicked"):
		GPIO.output(ledRequestSendPhoto, True)
		#time 10s to responde the request
		timeout_start = time.time()
		timeout = 10
		while (time.time() < timeout_start + timeout):
			if GPIO.event_detected(buttonTakePhoto):
				authorizePhoto()			
		GPIO.output(ledRequestSendPhoto, False)
		GPIO.setup(buttonTakePhoto, GPIO.IN, GPIO.PUD_UP)
