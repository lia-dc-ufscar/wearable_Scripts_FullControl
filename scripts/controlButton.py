#!/usr/bin/env python

import time
import json
import requests
import RPi.GPIO as GPIO
import gps
import picamera

import datetime
import os


ledRequestPhoto = 5
ledAuthorizeDeny = 19
ledPhotoSent = 13

buttonDeny = 16
buttonAuthorize = 12 
buttonPhoto = 20
buttonGPS = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ledRequestPhoto, GPIO.OUT)
GPIO.setup(ledAuthorizeDeny, GPIO.OUT)
GPIO.setup(ledPhotoSent, GPIO.OUT)

GPIO.output(ledRequestPhoto, False)
GPIO.output(ledAuthorizeDeny, False)
GPIO.output(ledPhotoSent, False)

GPIO.setup(buttonAuthorize, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(buttonDeny, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(buttonPhoto, GPIO.IN, GPIO.PUD_UP)
#GPIO.setup(buttonGPS, GPIO.IN, GPIO.PUD_UP)


GPIO.setwarnings(False)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url_get_new_clicks = 'http://lia-wearable-fullcontrol.meteor.com/getNewClicks'
url_update = 'http://lia-wearable-fullcontrol.meteor.com/updateClickPermission'
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
	dataPhoto = {'auth': auth, 'lat': 49.2657, 'lng': -123.247394, 'display':0, 'extra':{'type': 1, 'path': path}}
	r = requests.post(url_add_data, data=json.dumps(dataPhoto), headers = headers)
	if (r.status_code == 200):
		GPIO.output(ledPhotoSent, True)
		time.sleep(2)
		GPIO.output(ledPhotoSent, False)

def sendPhotoGPS():
	global PhotoRequestCounter
	path = 'image'+str(PhotoRequestCounter)+'.jpg'
	dataPhotoGPS = {'auth': auth, 'lat': 49.2657, 'lng': -123.247394, 'display':1, 'extra':{'type': 1, 'path': path}}
	r = requests.post(url_add_data, data=json.dumps(dataPhotoGPS), headers = headers)
	if (r.status_code == 200):
		GPIO.output(ledPhotoSent, True)
		time.sleep(2)
		GPIO.output(ledPhotoSent, False)

buttonState = 0
nState = 2
#GPIO.add_event_detect(buttonGPS, GPIO.FALLING)


def takePhoto():
	global PhotoRequestCounter
	with picamera.PiCamera() as camera:
		try:
			path = '/home/pi/scripts/photos/image'+str(PhotoRequestCounter)+'.jpg'
			camera.start_preview()
			time.sleep(5)
			camera.capture(path)
			camera.stop_preview()
		except:
			print("Could not take the photo")
	savePhoto()
	
#	if GPIO.event_detected(buttonGPS):
#		buttonState = (buttonState + 1) % nState
#	if buttonState = 1:
#		sendPhoto()
#	else
	sendPhotoGPS()
	
	PhotoRequestCounter += 1		


def denyPhoto(buttonDeny):
	print("botton deny pressed")
	GPIO.output(ledRequestPhoto, False)
#	d = requests.post(url_update, data=json.dumps ({'auth':auth, 'id': ID, 'status': 0}), headers=headers)
#	if (d.status_code == 200):
	GPIO.output(ledAuthorizeDeny, True)
	time.sleep(2)
	GPIO.output(ledAuthorizeDeny, False)
		 

def authorizePhoto(buttonAuthorize):
#def authorizeButton():
	print("botton authorize pressed")
	GPIO.output(ledRequestPhoto, False)
	#url update for give the message that the photo will be taken
	a = requests.post(url_update, data=json.dumps({'auth':auth, 'id': ID, 'status': 1}), headers=headers)
	if (a.status_code == 200):
		GPIO.output(ledAuthorizeDeny, True)
		time.sleep(2)
		GPIO.output(ledAuthorizeDeny, False)
#	else:
#		print("Entrou no botao mas deu erro no request")
	#call one function to take the photo and send to the website
	takePhoto()


GPIO.add_event_detect(buttonDeny, GPIO.RISING)
GPIO.add_event_detect(buttonAuthorize, GPIO.RISING)
#GPIO.add_event_callback(buttonDeny, callback = denyPhoto)
#GPIO.add_event_callback(buttonAuthorize, callback = authorizePhoto)


while True:
	#if request lights up led for 10s and wait the button yes/no
	r = requests.post(url_get_new_clicks, data=json.dumps({'auth':auth}), headers=headers)
	if (r.status_code == 200):
		GPIO.output(ledRequestPhoto, True)
		time.sleep(2)
		GPIO.output(ledRequestPhoto, False)
		
		#time 10s to responde the request
	#	timeout_start = time.time()
	#	timeout = 10
		#print ("time: %f", timeout_start) 
	#	for ID in r.content.split("|"):
	#		GPIO.add_event_callback(buttonDeny, callback = denyPhoto)
	#		GPIO.add_event_callback(buttonAuthorize, callback = authorizePhoto)
	#		while (time.time() < timeout_start + timeout):
	#			pass
			#GPIO.wait_for_edge(buttonAuthorize, GPIO.FALLING)
			#if pass 10s and none of the buttons are pressed the LED lights down
			#authorizeButton()
	#		GPIO.output(ledRequestPhoto, False)
			#b = requests.post(url_clean_clicks, data=json.dumps({'auth':auth}), headers=headers)
	#		GPIO.setup(buttonAuthorize, GPIO.IN, GPIO.PUD_UP)
	#		GPIO.setup(buttonDeny, GPIO.IN, GPIO.PUD_UP)

