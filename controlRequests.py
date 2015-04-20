import json
import time
import requests
import picamera
import RPi.GPIO as GPIO

ledPhotoViewed = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO.setup(buttonWIFI, GPIO.IN, GPIO.PUD_UP)

GPIO.setup(ledPhotoViewed, GPIO.OUT)
GPIO.output(ledPhotoViewed, True)

GPIO.setwarnings(False)

headers = {"Content-type": 'application/json', 'Accept':'text/plain'}
url_get_new_clicks = 'http://lia-wearable-fullcontrol.meteor.com/getNewClicks'
auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

def verifyNewClick():
	r = requests.post(url_get_new_clicks, data = json.dumps({'auth':auth}), headers=headers)
	if (r.status_code == 200):
		#print("get ok")
		GPIO.output(ledPhotoViewed, False)
		time.sleep(1)
		GPIO.output(ledPhotoViewed, True)

wifiJson = json.loads('{"status":0}')

while True:
#	GPIO.output(ledPhotoViewed, True)
#	time.sleep(3)
#	GPIO.output(ledPhotoViewed, False)

	config = open('/home/pi/scripts/var/status-wifi.json', 'r')
	wifiJson = json.load(config)
	statusWIFI = wifiJson['status']
	config.close()
	if statusWIFI == 0:
		verifyNewClick()
#		time.sleep(1)
