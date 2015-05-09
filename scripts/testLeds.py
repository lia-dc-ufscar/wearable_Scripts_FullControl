import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

GPIO.output(21, False)
GPIO.output(20, False)

time.sleep(3)

GPIO.output(21, True)
GPIO.output(20, True)

GPIO.setwarnings(False)

#GPIO.output(6, False)
#GPIO.output(13, False)
#GPIO.output(19, False)
#GPIO.output(26, False)


