#!/usr/bin/env python

import gps
import time
import json
import requests
import RPi.GPIO as GPIO
import picamera
import shutil

import datetime
import os


shutil.copy('/home/pi/scripts/logs/fullcontrol-camera.txt', '/home/pi/scripts/logs/last-fullcontrol-camera.log')
shutil.copy('/home/pi/scripts/logs/fullcontrol-camera-err.txt', '/home/pi/scripts/logs/last-fullcontrol-camera-err.log')

import sys
sys.stdout = open('/home/pi/scripts/logs/fullcontrol-camera.txt','w', 0)
sys.stderr = open('/home/pi/scripts/logs/fullcontrol-camera-err.txt','w', 0)

PhotoCounter = 0	
countSave = 0
countSend = 0

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

print("Starting Script controlCamera.py")

def savePhoto():
	global PhotoCounter 
	global countSave
	url = 'http://lia.dc.ufscar.br/image_upload/fileupload.php'
	files = {'file': open('/home/pi/scripts/photos/photo'+str(PhotoCounter)+'.jpg', 'rb')}
	f = requests.post(url, files=files)
	countSave = countSave + 1
	print("SavePhoto:", countSave)

def sendPhoto():
	#GET LAST GPS POSITION 
	global PhotoCounter

	path = 'photo'+str(PhotoCounter)+'.jpg'

	configFile = open('/home/pi/scripts/var/last-gps.json', 'r')
	configInfo = json.load(configFile)

	lat = configInfo['lat']
	lng = configInfo['lon']

	configFile.close()
	
	dataGPSoff = {'auth': 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R', 'lat': lat, 'lng': lng, 'display': 0, 'extra': {'type': 1, 'path': path}}
	r = requests.post('http://lia-wearable-fullcontrol.meteor.com/addDatum', data=json.dumps(dataGPSoff), headers = headers)

def sendPhotoGPS():
	global PhotoCounter
	global countSend

	path = 'photo'+str(PhotoCounter)+'.jpg'

	configFile = open('/home/pi/scripts/var/last-gps.json', 'r')
	configInfo = json.load(configFile)

	lat = configInfo['lat']
	lng = configInfo['lon']

	configFile.close()

	
	dataGPSon = {'auth': 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R', 'lat': lat, 'lng': lng, 'display': 1, 'extra': {'type': 1, 'path': path}}
	r = requests.post('http://lia-wearable-fullcontrol.meteor.com/addDatum', data=json.dumps(dataGPSon), headers = headers)
	if (r.status_code == 200):
		countSend = countSend + 1
		print("SendPhoto", countSend)


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
		print("Button Pressed")
		with picamera.PiCamera() as camera:
		#save photo
			try: 
				PhotoCounter = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
				path = '/home/pi/scripts/photos/photo'+str(PhotoCounter)+'.jpg'
				print("Start Preview")
				camera.start_preview()
				time.sleep(3)
				camera.capture(path)
				camera.stop_preview()
				print("Stop Preview")
			except:
				print("Could not take photo")
		savePhoto()	
		sendPhotoGPS()





