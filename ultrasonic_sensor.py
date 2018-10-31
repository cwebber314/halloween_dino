from __future__ import print_function
import RPi.GPIO as GPIO
import time
import pygame

pygame.init()
sound = pygame.mixer.Sound("roar.wav")

print("hello world")
GPIO.setmode(GPIO.BCM)

TRIGGER_DISTANCE_BOX = 48
TRIGGER_DISTANCE_ROAR = 200
LIGHT1 = 2
LIGHT2 = 27
TRIG = 3
ECHO = 4
BOX = 17

print("Distance Measurement In progress")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LIGHT1, GPIO.OUT)
GPIO.setup(LIGHT2, GPIO.OUT)
GPIO.setup(BOX, GPIO.OUT)

GPIO.output(TRIG, False)
GPIO.output(BOX, False)

print("Waiting for sensor to settle")
time.sleep(2)

# Duration is in seconds
TIMEOUT = 1

def blink():
	"""
	100 ms blink 
	"""
	GPIO.output(LIGHT1, False)
	GPIO.output(LIGHT2, False)
	time.sleep(25e-3)
	GPIO.output(LIGHT1, True)
	GPIO.output(LIGHT2, True)
	time.sleep(75e-3)
	return

GPIO.output(LIGHT1, True)
GPIO.output(LIGHT2, True)
	
while True:
	timeout_start = time.time()
	timeout = False
	GPIO.output(TRIG, True)
	time.sleep(10e-6)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO) == 0:
		pulse_start = time.time()
		if pulse_start - timeout_start > TIMEOUT:
			timeout = True
			break

	if timeout:
		print("Sensor TIMEOUT... restarting loop")
		continue
		
	while GPIO.input(ECHO) == 1:
		pulse_end = time.time()
		
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2) / 2.54
	if distance < TRIGGER_DISTANCE_BOX:
		print("TRIGGER_DISTANCE_BOX")
		if not pygame.mixer.get_busy():
			pygame.mixer.Sound.play(sound)
		#pygame.mixer.music.stop()
		#time.sleep(2.0)

		# Momentary Switch
		GPIO.output(BOX, True)
		time.sleep(100e-3)
		GPIO.output(BOX, False)

		for i in range(25):
			blink()

		# Momentary Switch
		GPIO.output(BOX, True)
		time.sleep(100e-3)
		GPIO.output(BOX, False)
	elif distance < TRIGGER_DISTANCE_ROAR:
		print("TRIGGER_DISTANCE_ROAR")
		if not pygame.mixer.get_busy():
			pygame.mixer.Sound.play(sound)
		for i in range(10):
			blink()

	print("Distance: %s in" % distance) 
	time.sleep(50e-3)
