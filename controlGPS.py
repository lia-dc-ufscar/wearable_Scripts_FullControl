import time
import json
import requests
import RPi.GPIO as GPIO
import gps
import picamera
import subprocess

#setup system date 
import datetime
import os

#time.sleep(30)
ledGPS = 19
buttonGPS = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ledGPS, GPIO.OUT)
GPIO.output(ledGPS, False)

GPIO.setup(buttonGPS, GPIO.IN, GPIO.PUD_UP)


GPIO.setwarnings(False)

session = None
connected = False

auth = 'jQ5a6odf3qJfhjyZG8M73C3A8JQyHk6w7R'

GetGPSSystemDate = False
if datetime.date.today().year < 1980:
	GetGPSSystemDate = True
	os.system("date --set '2015-02-13T12:33:43.000Z'")


while not connected:
	try:
		session = gps.gps()
		session.stream(gps.WATCH_ENABLE)
		connected = True
	except Exception, e:
		print("Could not connect")
		subprocess.call(["/bin/gpsd", "/dev/ttyAMA0"])
		time.sleep(2)

PushRate = 30
PushCount = 0
fix = False

def getFix():
	global report
	for satellite in report['satellites']:
		if (satellite['used'] == True):
			return True
	return False


def sendData():
#last lat position
	print("entrou no sendData")
	configlat = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlatJson = json.load(configlat)
	lat = configlatJson['lat']
	configlat.close()
	print ("lat:", lat)

#last lon position
	configlng = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlngJson = json.load(configlng)
	lng = configlngJson['lon']
	configlng.close()
	print ("lon:", lng)

	data = {'auth':auth, 'lat':lat, 'lng':lng, 'display':1, 'extra':{'type':0}}
#	data = {'auth':auth, 'lat':49.2657, 'lng':-123.247394, 'display':1, 'extra':{'type':0}}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.post('http://lia-wearable-fullcontrol.meteor.com/addDatum', data=json.dumps(data), headers = headers)
	if (r.status_code == 200):
		print ("data sent to website")		
		GPIO.output(ledGPS, True)
		time.sleep(2)
		GPIO.output(ledGPS, False)


def noSendData():			
#last lat position
	print("entrou no noSendData")
	configlat = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlatJson = json.load(configlat)
	lat = configlatJson['lat']
	configlat.close()
	print ("lat:", lat)

#last lon position
	configlng = open('/home/pi/scripts/var/last-gps.json', 'r')
	configlngJson = json.load(configlng)
	lng = configlngJson['lon']
	configlng.close()
	print("lon:", lng)

	#behavior when turn off the gps, display is 0
	#data = {'auth':auth, 'lat':lat, 'lng':lng, 'display':0, 'extra':{'type':0}}
	#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	#r = requests.post('http://lia-wearable-fullcontrol.meteor.com/addDatum', data=json.dumps(data), headers = headers)
#	time.sleep(2)	


# A cada um minuto envia dados do gps, pisca Led, verifica se botao de off foi pressionado 
GPIO.add_event_detect(buttonGPS, GPIO.FALLING)
buttonState = 0
nState = 2
#GPIO.output(ledGPS, True)

while True:
	config = open('/home/pi/scripts/var/status-wifi.json', 'r')
	wifiJson = json.load(config)
	statusWIFI = wifiJson['status']
	config.close()

	if statusWIFI == 0:
		try:
			report = session.next()
			print("aquI")
			if report['class'] == 'SKY':
				fix = getFix()
			if not fix:
				print("not fix")
				if PushCount < PushRate:
					PushCount = PushRate
		
			else:
				if report['class'] == 'TPV':
					print("class ok")
					if 'time' in report:
						print("time ok")
						if (GetGPSSystemDate):
							print("getgps ok")
							GetGPSSystemDate = False
							os.system("date --set '%s'"%report.time)
						if GPIO.event_detected(buttonGPS):
							buttonState = (buttonState + 1) % nState
							if buttonState == 1:
								GPIO.output(ledGPS, False)
							#if buttonState == 0:
							#	GPIO.output(ledGPS, True)
						if buttonState == 0:
							lastpos = open('/home/pi/scripts/var/last-gps.json', 'w')
							jsonpos = json.dumps(dict(report))
							print >> lastpos, jsonpos
							lastpos.close()
						print("Push count:", PushCount)
						print("Push Rate:", PushRate)
						if (PushCount >= PushRate):
							print("if pushcount")
							#GpsLog.flush()
							PushCount = 0
						#behavior when the gps is turned off							
							if buttonState == 1:
								print("no envia dado")
								noSendData()
		
							else: 
								print("envia dado")				
								sendData()
		
						
					PushCount += 1

		except StopIteration:
			session = gps.gps()
			session.stream(gps.WATCH_ENABLE)
			continue
