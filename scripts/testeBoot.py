#!/usr/bin/env python

import json
import time
import requests
import picamera
import RPi.GPIO as GPIO
import shutil

#shutil.copy('/home/pi/scripts/logs/fullcontrol-requests.txt', '/home/pi/scripts/logs/last-fullcontrol-requests.log')
#shutil.copy('/home/pi/scripts/logs/fullcontrol-requests-err.txt', '/home/pi/scripts/logs/last-fullcontrol-requests-err.log')

#import sys
#sys.stdout = open('/home/pi/scripts/logs/fullcontrol-requests.txt','w', 0)
#sys.stderr = open('/home/pi/scripts/logs/fullcontrol-requests-err.txt','w', 0)

#ledPhotoViewed = 23

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)

#GPIO.setup(buttonWIFI, GPIO.IN, GPIO.PUD_UP)

#GPIO.setup(ledPhotoViewed, GPIO.OUT)
#GPIO.output(ledPhotoViewed, True)

#GPIO.setwarnings(False)

headers = {"Content-type": 'application/json', 'Accept':'text/plain'}
url_get_new_clicks = 'http://lia-wearable-fullcontrol.meteor.com/getNewClicks'
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

print("Starting Script controlRequests")

def verifyNewClick():
	r = requests.post(url_get_new_clicks, data = json.dumps({'auth':auth}), headers=headers)
	if (r.status_code == 200):
		print("Photo Viewed")
	#	GPIO.output(ledPhotoViewed, False)
	#	time.sleep(1)
	#	GPIO.output(ledPhotoViewed, True)

#wifiJson = json.loads('{"status":0}')
count = 0
while (count < 3):
#	GPIO.output(ledPhotoViewed, True)
#	time.sleep(3)
#	GPIO.output(ledPhotoViewed, False)

#	config = open('/home/pi/scripts/var/status-wifi.json', 'r')
#	wifiJson = json.load(config)
#	statusWIFI = wifiJson['status']
#	config.close()
#	if statusWIFI == 0:
	verifyNewClick()
	count = count + 1	
