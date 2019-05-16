from RPLCD.i2c import CharLCD

lcd = None

def setup():
	global lcd
	lcd = CharLCD('PCF8574', 0x27, backlight_enabled=True)
	lcd.write_string('Speed:       mph')

def change_speed(speed):
	lcd.cursor_pos = (0, 7)
	lcd.write_string(str(speed))

def change_second_line(string):
	lcd.cursor_pos = (1, 0)
	lcd.write_string(str(string))

