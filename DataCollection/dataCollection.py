import serial, sys, re, urllib, urllib2
import numpy as np
import matplotlib.pyplot as plt
from time import *

KEY = ""
ZERO_VAL = 0
CONVERSION_RATE = 1
DEBUG = False
ser = 0
timeRef = time()*1000

def calibrate():
	print "Enter to begin callibration"
	sys.stdin.readline()
	calibrate_zero()
	calibrate_weight()


def calibrate_zero():
	global ser
	print "Calibrating zero..."
	vals = []
	ser.flush()
	for t in range(30):
		line = ser.readline()
		while('FRC' not in line):
			line = ser.readline()
		reading = (line.split(',')[-1]).split(':')[-1]
		x = float(reading)/1023.0
		if DEBUG:
			print reading
		vals.append(x)
	zeroSum = float(sum(vals))
	zero_val = zeroSum/len(vals)
	print "Value to be set as 0: " + str(zero_val)
	return zero_val

def calibrate_weight():
	global ser
	print "Please place a weight on the sensor. Press enter when ready to begin calibration"
	sys.stdin.readline()
	vals = []
	ser.flush()
	for t in range(50):
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
	weight = raw_input("Please enter the weight of the object in kilograms: ")
	if weightVal == 0:
		print "No weight was detected!"
		weightVal = 1.0
	conversion_rate = float(weight)/weightVal
	print "Conversion rate = " + str(float(weight)) + "/" + str(weightVal)
	print "Conversion rate calculated to be: " + str(conversion_rate) + " kg per unit"
	return conversion_rate
	
def record(file):
	global ser
	global timeRef
	print "Press enter to begin recording. Press Ctrl+C to exit at any time."
	sys.stdin.readline()
	vals = []
	ser.flush()
	timeRef = time()*1000
	while True:
		try:
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
			file.write(str(time()*1000-timeRef))
			file.write(',')
			for i in range(len(measurements)-1):
				file.write(measurements[i].split(':')[-1])
				file.write(',')
			file.write(str(force))
			file.write('\n')
			vals.append(force)
		except KeyboardInterrupt:
			print("Closing File and terminating.")
			plt.plot(vals)
			plt.ylabel('Force (N)')
			plt.xlabel('Sample')
			plt.show()
			return

def getComFromPrompt():
	COM = raw_input("COM Port device is on: ")
	print("Attempting to connect to the device...")
	try:
		global ser
		ser = serial.Serial(int(COM)-1, 9600, timeout=1)
		print("Successfully connected to the device.")
	except Exception:
		print("Could not connect to device. Please make sure device is turned on and Blutooth on this machine is turned on. If error still occurs, reset the device.")
		raise
	return COM

# This file is used by getDataFromDotFile to set up the device
def updateDotFile(com, zero, conv):
	with open(".deviceprefs", 'w') as datafile:
		datafile.write("COM="+str(com)+"\n")
		datafile.write("zero="+str(zero)+"\n")
		datafile.write("conversion="+str(conv)+"\n")
	return (com,zero,conv)

# Look for .deviceprefs in the database folder and parse for preferences
# If the file or information are not present, prompt the user and fix it
def getDataFromDotFile():
	try:
		with open(".deviceprefs", 'r') as datafile:
			com = -99
			zero = -99
			conv = -99
			for line in datafile:
				field = line.partition('=')[0].strip()
				value = line.partition('=')[2].strip()
				if "COM" in field:
					com = value
				if "zero" in field:
					zero = value
				if "conversion" in field:
					conv = value
			if com != -99 and zero != -99 and conv != -99:
				return (com,zero,conv)
			# if we're here, we didn't find our data in the dotfile
			print "Data not found in .deviceprefs. Adding now."
			return updateDotFile(getComFromPrompt(), calibrate_zero(), calibrate_weight())
	except IOError:
		# This means .deviceprefs didn't exist
		return updateDotFile(getComFromPrompt(), calibrate_zero(), calibrate_weight())
	
def main():
	global ZERO_VAL
	global CONVERSION_RATE
	debugChoice = raw_input("DEBUG mode (Y/N)? ")
	global DEBUG
	DEBUG = False
	if str(debugChoice).lower() == "y":
		DEBUG = True	
	prefChoice = raw_input("Perform new calibration (Y/N)? ")
	if str(prefChoice).lower() == "y":
		updateDotFile(getComFromPrompt(), calibrate_zero(), calibrate_weight())
	cachedData = getDataFromDotFile()
	com, ZERO_VAL, CONVERSION_RATE = cachedData[0], float(cachedData[1]), float(cachedData[2])
	print("Attempting to connect to the device...")
	try:
		global ser
		ser = serial.Serial(int(com)-1, 9600, timeout=1)
		print("Successfully connected to the device.")
	except Exception:
		print("Already connected to the device.")
		pass
	filename = strftime("%d_%b_%y_%H-%M-%S.csv", localtime())
	file = open(filename, 'w')
	file.write('Time (ms),AccX,AccY,AccZ,Roll,Pitch,Yaw,MagX,MagY,MagZ,MagH,Force (N)\n')
	record(file)
	file.close()
	return

	
main()
