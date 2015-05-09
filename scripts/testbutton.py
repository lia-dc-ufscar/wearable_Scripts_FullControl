import time
import picamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.IN, GPIO.PUD_UP)
GPIO.setwarnings(False)
#GPIO.setup(13, GPIO.OUT)
#GPIO.output(13, False)
	
GPIO.wait_for_edge(12, GPIO.FALLING)
#GPIO.output(13, True)
#time.sleep(3)
#GPIO.output(13, False)

with picamera.PiCamera() as camera:
	camera.start_preview()
	time.sleep(5)
	camera.capture('/home/pi/scripts/image.jpg')
	camera.stop_preview()

#upload photos



