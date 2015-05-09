#!/usr/bin/env python

import json
import time
import requests
import picamera
import RPi.GPIO as GPIO
import shutil

shutil.copy('/home/pi/scripts/logs/fullcontrol-wifi.txt', '/home/pi/scripts/logs/last-fullcontrol-wifi.log')
shutil.copy('/home/pi/scripts/logs/fullcontrol-wifi-err.txt', '/home/pi/scripts/logs/last-fullcontrol-wifi-err.log')

import sys
sys.stdout = open('/home/pi/scripts/logs/fullcontrol-wifi.txt','w', 0)
sys.stderr = open('/home/pi/scripts/logs/fullcontrol-wifi-err.txt','w', 0)

buttonWIFI = 20
ledWIFI = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(buttonWIFI, GPIO.IN, GPIO.PUD_UP)

GPIO.setup(ledWIFI, GPIO.OUT)
GPIO.output(ledWIFI, False)


GPIO.setwarnings(False)

print("Starting Script controlWIFI")

headers = {"Content-type": 'application/json', 'Accept':'text/plain'}
#url_get_new_clicks = 'http://lia-wearable-fullcontrol.meteor.com/getNewClicks'
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

GPIO.add_event_detect(buttonWIFI, GPIO.FALLING, bouncetime = 200)
buttonStateWIFI = 0
nStateWIFI = 2
GPIO.output(ledWIFI, True)

while True:
	if GPIO.event_detected(buttonWIFI):
		buttonStateWIFI = (buttonStateWIFI + 1) % nStateWIFI
		print("buttonState:", buttonStateWIFI)
		GPIO.output(ledWIFI, False)
		statuswifi = open('/home/pi/scripts/var/status-wifi.json', 'w')
		jsonwifi = json.dumps({"status":buttonStateWIFI})
		statuswifi.write(jsonwifi)
		statuswifi.close()
		time.sleep(1)
	if buttonStateWIFI == 0:
		GPIO.output(ledWIFI, True)
	

