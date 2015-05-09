import sys
import gps
import json
import time
import RPi.GPIO as GPIO

#setup system date
import datetime
import os

GetGPSSystemDate=False
if datetime.date.today().year < 1980:
	print("System date has an odd value: ", datetime.date.today().year)
	GetGPSSystemDate=True
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
	try:
		report = session.next()
		print report
		if report['class'] == 'TPV':
		    if hasattr(report, 'time'):
		        print report.time
	except KeyError:
		pass
	except KeyboardInterrupt:
		quit()
	except StopIteration:
		session = None
		print "GPSD has terminated"

