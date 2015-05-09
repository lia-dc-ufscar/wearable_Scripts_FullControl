import time
import json
import requests
import RPi.GPIO as GPIO

#changepins
ledRequestPhoto = 9
ledAuthorizeDeny = 7
#buttonDeny = 
buttonAuthorize = 12 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ledRequestPhoto, GPIO.OUT)
GPIO.setup(ledAuthorizeDeny, GPIO.OUT)

GPIO.output(ledRequestPhoto, False)
GPIO.output(ledAuthorizeDeny, False)


GPIO.setup(buttonAuthorize, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(buttonDeny, GPIO.IN, GPIO.PUD_UP)

GPIO.setwarnings(False)

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url_get_new_clicks = 'http://wearable-fullcontrol.meteor.com/getNewClicks'
url_update = 'http://wearable-fullcontrol.meteor.com/updateClickPermission'

def denyPhoto(buttonDeny):
	GPIO.output(ledRequestPhoto, False)
	d = requests.post(url_update, data=json.dumps ({'auth':'436174696e7468654d61704c49414a43', 'id': ID, 'status': 0}), headers=headers)
	if (d.status_code == 200):
		GPIO.output(ledAuthorizeDeny, True)
		time.sleep(2)
		GPIO.output(ledAuthorizeDeny, False)
		 

def authorizePhoto(buttonAuthorize):
	GPIO.output(ledRequestPhoto, False)
	a = requests.post(url_update, data=json.dumps({'auth':'436174696e7468654d61704c49414a43', 'id': ID, 'status': 1}), headers=headers)
	if (a.status_code == 200):
		GPIO.output(ledAuthorizeDeny, True)
		time.sleep(2)
		GPIO.output(ledAuthorizeDeny, False)



while True:
	#if request lights up led for 10s and wait the button yes/no
	r = requests.post(url_get_new_clicks, data=json.dumps({'auth':'436174696e7468654d61704c49414a43'}), headers=headers)
	if (r.status_code == 200):
		GPIO.output(ledRequestPhoto, True)
		#time 10s to responde the request
		timeout_start = time.time()
		timeout = 10 
		for ID in r.content.split("|"):
			while time.time() < timeout_start + timeout:
				GPIO.add_event_detect(buttonDeny, GPIO.FALIING, callback = denyPhoto)
				GPIO.add_event_detect(buttonAuthorize, GPIO.FALLING, callback = authorizePhoto)

			#if pass 10s and none of the buttons are pressed the LED lights down
			GPIO.output(ledRequestPhoto, False)

