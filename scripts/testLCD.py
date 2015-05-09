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


	def __init__(self, cols=20, lines=4,  pin_rs=27, pin_e=4, pins_db=[17, 18, 22 , 23], GPIO=None):
		if not GPIO:
			import RPi.GPIO as GPIO
			GPIO.setwarnings(False)
		self.GPIO = GPIO
		self.pin_rs = pin_rs
		self.pin_e = pin_e
		self.pins_db = pins_db
		self.numcols = cols
		
		self.GPIO.setmode(GPIO.BCM)
		self.GPIO.setup(self.pin_e, GPIO.OUT)
		self.GPIO.setup(self.pin_rs, GPIO.OUT)

	
		for pin in self.pins_db:
			self.GPIO.setup(pin, GPIO.OUT)
		
		self.write4bits(0x33)
		self.write4bits(0x32)
		self.write4bits(0x50)
		self.write4bits(0x0C)
		self.write4bits(0x06)

		self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF

		self.displayfunction = self.LCD_4BITMODE | self.LCD_5X8DOTS| self.LCD_1LINE 
		
		self.displayfunction |= self.LCD_2LINE

		self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
		self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

		self.clear()

	def begin(self, cols, lines):
	#	if (lines > 1):
	#		self.numlines = lines
	#		self.displayfunction &= self.LCD_2LINE
	
		self.currline = 0
		self.numlines = lines
		self.numcols = cols
		self.clear()	

#	def home(self):
#		self.write4bits(self.LCD_RETURNHOME)
#		self.delayMicroseconds(3000)

	def clear(self):
		self.write4bits(self.LCD_CLEARDISPLAY)
		self.delayMicroseconds(3000)

	def setCursor(self, col, row):
		self.row_offsets = [0x00, 0x40, 0x14, 0x54]
		if row > self.numlines:
			row = self.numlines - 1
		self.write4bits(self.LCD_SETDDRAMADOR | (col + self.row_offsets[row]))

#	def noDisplay(self):
#		"""Turn display off"""
#		self.displaycontrol &= ~self.LCD_DISPLAYON
#		self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

#	def display(self):
#		"""Turn display on"""
#		self.displaycontrol |= self.LCD_DISPLAYON
#		self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)


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
		#for char in text:
		#	if char == '\n':
		#		self.write4bits(0xC0)
		#	else:
		#		self.write4bits(ord(char), True)
		#self.delayMicroseconds(10000000)
		lines = str(text).split('\n')
		for i, line in enumerate (lines):
			if i == 1:
				self.writ4bits(0xC0)
			elif i == 2:
				self.write4bits(0x94)
			elif i >= 3:
				self.write4bits(0xD4)
			lineLenght = len(line)
			limit = self.numcols
			if char_mode <= 0:
				self.write4bits(line, True)
			elif lineLenght >= limit and char_mode == 1:
				limitedLine = line[0:self.numcols]
				self.write4bits(limitedLine, True)
			elif lineLenght >= limit and char_mode == 2:
				limitedLine = line[0:self.numcols-3]+'...'
				self.write4bits(limitedLine, True)
			elif lineLenght >= limit and char_mode == 3:
				self.write4bits(limitedLine, True)
			else:
				self.write4bits(line, True)	
			



if __name__ == '__main__' :
	lcd = Teste_CharLCD()
	lcd.begin(20,4)
	lcd.setCursor(0,0)
	lcd.clear()
	lcd.message("oi csbfcbs testando o lcd hoje no domingo")
