from time import sleep
import requests
import json
import RPi.GPIO as GPIO

class Teste_CharLCD(object):

#Commands

	LCD_CLEARDISPLAY = 0x01
	LCD_RETURNHOME = 0x02
	LCD_ENTRYMODESET = 0x04
	LCD_DISPLAYCONTROL = 0x08
	LCD_CURSORSHIFT = 0x10
	LCD_FUNCTIONSET = 0x20
	LCD_SETCGRAMADOR = 0x40
	LCD_SETDDRAMADOR = 0x80

#flags for display entry mode
	LCD_ENTRYRIGHT = 0X00
	LCD_ENTRYLEFT = 0X02
	LCD_ENTRYSHIFTINCREMENT = 0X01
	LCD_ENTRYSHIFTDECREMENT = 0X00

#Flags fos display on/off control
	LCD_DISPLAYON = 0X04
	LCD_DISPLAYOFF = 0X00
	LCD_CURSORON = 0X02
	LCD_CURSOROFF = 0X00
	LCD_BLINKON = 0X01
	LCD_BLINKOFF = 0X00

#fLAGS FOR DISPLAY CURSOR SHIFT
	LCD_DISPLAYMOVE = 0X08
	LCD_CURSORMOVE = 0X00

#FLAGS FOR DISPLAY/CURSOR SHIFT
	LCD_DISPLAYMOVE = 0X08
	LCD_CURSORMOVE = 0X00
	LCD_MOVERIGHT = 0X04
	LCD_MOVELEFT = 0X00

#FLAGS FOR FUNCTION SET
	LCD_8BITMODE = 0X10
	LCD_4BITMODE = 0X00
	LCD_2LINE = 0X08
	LCD_1LINE = 0X00
	LCD_5X10DOTS = 0X04
	LCD_5X8DOTS = 0X00


	def __init__(self, pin_rs=25, pin_e=24, pins_db=[23, 17, 27 , 22], GPIO=None):
		if not GPIO:
			import RPi.GPIO as GPIO
			GPIO.setwarnings(False)
		self.GPIO = GPIO
		self.pin_rs = pin_rs
		self.pin_e = pin_e
		self.pins_db = pins_db
		#self.pin_v = pin_v
		#self.pin_Ldelete = pin_Ldelete
		#self.pin_Bdelete = pin_Bdelete


		self.GPIO.setmode(GPIO.BCM)
		self.GPIO.setup(self.pin_e, GPIO.OUT)
		self.GPIO.setup(self.pin_rs, GPIO.OUT)
		#self.GPIO.setup(self.pin_v, GPIO.OUT)
		#self.GPIO.output(self.pin_v, False)
		#self.GPIO.setup(self.pin_Ldelete, GPIO.OUT)
		#self.GPIO.output(self.pin_Ldelete, False)
		#self.GPIO.setup(self.pin_Bdelete, GPIO.IN, GPIO.PUD_DOWN)

	
		for pin in self.pins_db:
			self.GPIO.setup(pin, GPIO.OUT)
		
		self.write4bits(0x33)
		self.write4bits(0x32)
		self.write4bits(0x28)
		self.write4bits(0x0C)
		self.write4bits(0x06)

		self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF

		self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5X8DOTS
		self.displayfunction |= self.LCD_2LINE

		self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
		self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

		self.clear()

	def begin(self, col, lines):
		if (lines > 1):
			self.numlines = lines
			self.displayfunction |= self.LCD_2LINE

	def home(self):
		self.write4bits(self.LCD_RETURNHOME)
		self.delayMicroseconds(3000)

	def clear(self):
		self.write4bits(self.LCD_CLEARDISPLAY)
		self.delayMicroseconds(3000)

	def setCursor(self, col, row):
		self.row_offsets = [0x00, 0x40, 0x14, 0x54]
		if row > self.numlines:
			row = self.numlines - 1
		self.write4bits(self.LCD_SETDDRAMADOR | (col + self.row_offsets[row]))

	def noDisplay(self):
		"""Turn display off"""
		self.displaycontrol &= ~self.LCD_DISPLAYON
		self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

	def display(self):
		"""Turn display on"""
		self.displaycontrol |= self.LCD_DISPLAYON
		self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

#def noCursor(self)
#def cursor(self)
#def noBlink(self)
#def blink(self)
#def DisplayLeft(self)
#def scrollDisplayRight(self)
#def leftToRight(self)
#def rightToLeft(self)
#def autocroll(self)
#def noAutocroll(self)

	def write4bits(self, bits, char_mode=False):
		"""Send command to LCD"""
		self.delayMicroseconds(1000)
		bits = bin(bits)[2:].zfill(8)
		self.GPIO.output(self.pin_rs, char_mode)
		for pin in self.pins_db:
			self.GPIO.output(pin, False)
		for i in range(4):
			if bits[i] == "1":
				self.GPIO.output(self.pins_db[::-1][i], True)
		self.pulseEnable()
		for pin in self.pins_db:
			self.GPIO.output(pin, False)
		for i in range(4, 8):
			if bits[i] == "1":
				self.GPIO.output(self.pins_db[::-1][i-4], True)
		self.pulseEnable()

	def delayMicroseconds(self, microseconds):
		seconds = microseconds / float(1000000)
		sleep(seconds)

	def pulseEnable(self):
		self.GPIO.output(self.pin_e, False)
		self.delayMicroseconds(1)
		self.GPIO.output(self.pin_e, True)
		self.delayMicroseconds(1)
		self.GPIO.output(self.pin_e, False)
		self.delayMicroseconds(1)

	def message(self, text):
		"""Send string to LCD"""
		for char in text:
			if char == '\n':
				self.write4bits(0xC0)
			else:
				self.write4bits(ord(char), True)
		self.delayMicroseconds(10000000)


	def motorVibration(self):
		GPIO.setup(self.pin_v, GPIO.OUT)
		count = 0
		while count < 3:
			self.GPIO.output(self.pin_v, True)
			self.delayMicroseconds(1000000)
			self.GPIO.output(self.pin_v, False)
			self.delayMicroseconds(500000)
			count += 1

	def verifyMessage(self):
		headers = {'Content-tyoe': 'application/json', 'Accept':'text/plain'}
		url = 'http://catinthemap.meteor.com/getNewMessages'
		data = {'auth': '436174696e7468654d61704c49414a43'}
		r = requests.post(url, data=json.dumps(data), headers=headers)


	def removeMessage(self):
		headers = {'Content-tyoe': 'application/json', 'Accept':'text/plain'}
		url = 'http://catinthemap.meteor.com/deleteText'
		data = {'auth': '436174696e7468654d61704c49414a43', 'id': 'this is the id'}
		r = requests.post(url, data=json.dumps(data), headers=headers)


	def blinkLED(self):
		GPIO.setup(self.pin_Ldelete, GPIO.OUT)
		self.GPIO.output(self.pin_Ldelete, True)
		self.delayMicroseconds(1000000)
		self.GPIO.output(self.pin_Ldelete, False)
	
	def pressButton(self):
		print ("Entrei botao")
		GPIO.wait_for_edge(self.pin_Bdelete, GPIO.FALLING)
		print ("Botao apertado")

if __name__ == '__main__' :
	lcd = Teste_CharLCD()
	lcd.clear()
	#Verifica a cada 10 segundos se tem mensagem
	#lcd.verifyMessage()
	#if r.status_code == 200:
	#arrayTeste = ["Testing LCD new message", "Hey , new message for you"]
	#if arrayTeste:
		#lcd.motorVibration()
	lcd.message("TESTING")
	#Mostra Mensagem message(r.content) por 10 segundos
	#lcd.message(r.content[0].message)
	#lcd.pressButton()
#	lcd.clear()
#	lcd.blinkLED()
	
	#Se botao deletar for pressionado 
	#removeMessage()
	#lcd.message (" Testing lcd new message ")
			
