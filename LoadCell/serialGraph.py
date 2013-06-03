import serial
import Tkinter as tk
import sys
import numpy as np
import matplotlib.pyplot as plt
from time import *


root = tk.Tk()
KEY = ""
ZERO_VAL = 0
CONVERSION_RATE = 1
DEBUG = True
ser = 0

def calibrate():
	print "enter to begin callibration"
	calibrate_zero()
	calibrate_weight()

def calibrate_zero():
	global ser
	sys.stdin.readline()
	print "calibrating zero..."
	vals = []
	ser.flush()
	for t in range(100):
		line = ser.readline()
		while('FRC' not in line):
			line = ser.readline()
		reading = (line.split(',')[-1]).split(':')[-1]
		x = float(reading)/1023.0
		if DEBUG:
			print reading
		vals.append(x)
	zeroSum = float(sum(vals))
	global ZERO_VAL
	ZERO_VAL = zeroSum/len(vals)
	print "value to be set as 0: " + str(ZERO_VAL)

def calibrate_weight():
	global ser
	print "please place a weight on the sensor. Press enter when ready to begin calibration"
	sys.stdin.readline()
	vals = []
	ser.flush()
	for t in range(100):
		line = ser.readline()
		while('FRC' not in line):
			line = ser.readline()
		reading = (line.split(',')[-1]).split(':')[-1]
		x = float(reading)/1023.0 - ZERO_VAL
		if x<0:
			x=0
		if DEBUG:
			print reading
		vals.append(x)
	weightSum = float(sum(vals))
	weightVal = weightSum/len(vals)
	print "please enter the weight of the object in kilograms"
	weight = sys.stdin.readline()
	global CONVERSION_RATE
	if weightVal == 0:
		print "no weight was detected!"
		weightVal = 1.0
	CONVERSION_RATE = float(weight)/weightVal
	print "conversion rate = " + str(float(weight)) + "/" + str(weightVal)
	print "conversion rate calculated to be: " + str(CONVERSION_RATE) + " kg per unit"
	
def record(file):
	global ser
	print "press enter the number of samples to record"
	numsamples = sys.stdin.readline()
	vals = []
	ser.flush()
	for i in range(int(numsamples)):
		global CONVERSION_RATE
		global ZERO_VAL
		line = ser.readline()
		while('FRC' not in line):
			line = ser.readline()
		measurements = line.split(',')
		force_reading = (measurements[-1]).split(':')[-1]
		if DEBUG:
			print line
		x = float(force_reading)/1023.0 - ZERO_VAL
		if x<0:
			x=0
		force = CONVERSION_RATE*(x)*10
		if DEBUG:	
			print "" + str(force) + " N" + " " + str(x) 
		for i in range(len(measurements)-1):
			file.write(measurements[i].split(':')[-1])
			file.write(',')
		file.write(str(force))
		file.write('\n')
		vals.append(force)
		
	plt.plot(vals)
	plt.ylabel('Force (N)')
	plt.xlabel('Sample')
	plt.show()

def keypress(event):
	global root
	if event.keysym == 'Escape':
		root.destroy()
	x = event.char
	if x == "c":
		calibrate()
	if x == "r":
		record()

def main():
	#global root
	#print "Press Escape to exit, press c to calibrate press r to record"
	#root.bind_all('<Key>', keypress) #lambda event: keypress(event, root))
	# don't show the tk window
	#root.withdraw()
	#root.mainloop()
	print("enter the serial port:")
	com = sys.stdin.readline()
	global ser
	ser = serial.Serial(int(com)-1, 9600, timeout=1)
	calibrate()
	filename = strftime("%d_%b_%y_%H-%M-%S.csv", localtime())
	file = open(filename, 'w')
	file.write('AccX,AccY,AccZ,Roll,Pitch,Yaw,MagX,MagY,MagZ,MagH,Force\n')
	record(file)
	file.close()
	return

	
main()
