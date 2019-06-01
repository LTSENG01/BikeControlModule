import RPi.GPIO as GPIO
import lcd
import sys
import time
import math

# TODO: Half the speed to get actual MPH

WHEEL_DIAMETER = 26	# diameter of the wheel in inches
DETECTION_ZONE = 5	# the angle where the sensor is detecting in degrees
REED_PIN = 23		# BCM port 23 (board port 16)
MAX_PERIOD = 5000	# maximum time before discarding buffer
SAMPLE_COUNT = 1	# number of samples for averaging
DEBOUNCE_TIME = 100	# time to debounce before reading a second tick (in ms)

CIRCUMFERENCE = WHEEL_DIAMETER * math.pi	# circumference of the bicycle wheel

time_buffer = []
last_timestamp = 0
trip_distance = 0
total_distance = 0

def get_current_millis():
	return int(round(time.time() * 1000))

def on_rising_edge(channel):
	global last_timestamp
	global time_buffer

	delta_time = get_current_millis() - last_timestamp

	print("Rising edge " + str(delta_time) + " " + str(last_timestamp))

	if delta_time > MAX_PERIOD:	# measuring 150ms and 5s
		# invalid delta_time
		time_buffer.clear()
		calculate_mph([0])
	elif delta_time < 100:
		pass
	elif delta_time > 100 and delta_time < 150:
		calculate_mph([0])
		pass				# ignore it
	else:
		if len(time_buffer) >= SAMPLE_COUNT:
			calculate_mph(time_buffer)
			time_buffer.clear()

		time_buffer.append(delta_time / 1000 / 3600)
 		# print("valid delta_time (hours): " + str(delta_time / 1000 / 3600))

	last_timestamp = get_current_millis()

def calculate_mph(time_buffer):
	# print(time_buffer)
	average_time = sum(time_buffer) / SAMPLE_COUNT
	if not average_time == 0.0:
		mph = CIRCUMFERENCE / 63360 / average_time
	else:
		mph = 0.00

	print("\naverage mph: " + str("%.2f" % mph) + "\n")
	lcd.change_speed("%.2f" % mph)

def setup():
	print("--------------------------")
	print("Bike program is starting!")
	print("Wheel Diameter: " + str(WHEEL_DIAMETER) + " inches")
	print("--------------------------")

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(REED_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	GPIO.add_event_detect(REED_PIN, GPIO.RISING, callback=on_rising_edge, bouncetime=DEBOUNCE_TIME)

def main():
	try:
		lcd.setup()
		setup()
		while True:
			if get_current_millis() - last_timestamp > 5000 and not last_timestamp == 0:
				calculate_mph([0])
				time.sleep(3)
	except KeyboardInterrupt:
		GPIO.cleanup()
		sys.exit()

main()

