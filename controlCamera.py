import gps
import time
import json
import requests
import RPi.GPIO as GPIO
import picamera
import datetime
import os

PhotoCounter = 0	

buttonTakePhoto = 16
ledRequestSendPhoto = 5
ledPhotoTaken = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buttonTakePhoto, GPIO.IN, GPIO.PUD_UP)

GPIO.setup(ledRequestSendPhoto, GPIO.OUT)
GPIO.output(ledRequestSendPhoto, False)

GPIO.setup(ledPhotoTaken, GPIO.OUT)
GPIO.output(ledPhotoTaken, False)

GPIO.setwarnings(False)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} 

def savePhoto():
	global PhotoCounter 
	url = 'http://lia.dc.ufscar.br/image_upload/fileupload.php'
	files = {'file': open('/home/pi/scripts/photos/photo'+str(PhotoCounter)+'.jpg', 'rb')}
	f = requests.post(url, files=files)

def sendPhoto():
	#GET LAST GPS POSITION 
	global PhotoCounter
	path = 'photo'+str(PhotoCounter)+'.jpg'

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
	
	dataGPSoff = {'auth': 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R', 'lat': lat, 'lng': lng, 'display': 0, 'extra': {'type': 1, 'path': path}}
	r = requests.post('http://lia-wearable-fullcontrol.meteor.com/addDatum', data=json.dumps(dataGPSoff), headers = headers)


def sendPhotoGPS():
	global PhotoCounter
	path = 'photo'+str(PhotoCounter)+'.jpg'

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

	
	dataGPSon = {'auth': 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R', 'lat': lat, 'lng': lng, 'display': 1, 'extra': {'type': 1, 'path': path}}
	r = requests.post('http://lia-wearable-fullcontrol.meteor.com/addDatum', data=json.dumps(dataGPSon), headers = headers)
	print("status", r.status_code)


while True:
	config = open('/home/pi/scripts/var/status-wifi.json', 'r')
	wifiJson = json.load(config)
	statusWIFI = wifiJson['status']
	config.close()
	
	if statusWIFI == 0:
		GPIO.wait_for_edge(buttonTakePhoto, GPIO.FALLING)
		GPIO.output(ledRequestSendPhoto, False)
		GPIO.output(ledPhotoTaken, True)
		time.sleep(2)
		GPIO.output(ledPhotoTaken, False)
		with picamera.PiCamera() as camera:
		#save photo
			try: 
				PhotoCounter = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
				path = '/home/pi/scripts/photos/photo'+str(PhotoCounter)+'.jpg'
				camera.start_preview()
				time.sleep(3)
				camera.capture(path)
				camera.stop_preview()
			except:
				print("Could not take photo")
		savePhoto()	
		sendPhotoGPS()





