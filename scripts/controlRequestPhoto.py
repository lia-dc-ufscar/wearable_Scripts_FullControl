#!/usr/bin/env python

import time
import json
import requests
import RPi.GPIO as GPIO
import gps
import picamera
import shutil

import datetime
import os

shutil.copy('/home/pi/scripts/logs/fullcontrol-requestPhoto.txt', '/home/pi/scripts/logs/last-fullcontrol-requestPhoto.log')
shutil.copy('/home/pi/scripts/logs/fullcontrol-requestPhoto-err.txt', '/home/pi/scripts/logs/last-fullcontrol-requestPhoto-err.log')

import sys
sys.stdout = open('/home/pi/scripts/logs/fullcontrol-requestPhoto.txt','w', 0)
sys.stderr = open('/home/pi/scripts/logs/fullcontrol-requestPhoto-err.txt','w', 0)

#Changes
ledRequestSendPhoto = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ledRequestSendPhoto, GPIO.OUT)

GPIO.output(ledRequestSendPhoto, True)

GPIO.setwarnings(False)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url_get_new_clicks = 'http://lia-wearable-fullcontrol.meteor.com/getNewClicks'
url_get_new_photo = 'http://lia-wearable-fullcontrol.meteor.com/getLastClick'
url_clean_clicks = 'http://lia-wearable-fullcontrol.meteor.com/cleanClicks'
url_add_data = 'http://lia-wearable-fullcontrol.meteor.com/addDatum'
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

print("Starting Script controlRequestPhoto")

while True:
	config = open('/home/pi/scripts/var/status-wifi.json', 'r')
	wifiJson = json.load(config)
	statusWIFI = wifiJson['status']
	config.close()

	if statusWIFI == 0:
		r = requests.post(url_get_new_photo, headers=headers)
		if (r.content == "clicked"):
			print("Button Pressed")
			GPIO.output(ledRequestSendPhoto, False)
			time.sleep(2)
			GPIO.output(ledRequestSendPhoto, True)
