import serial
import sys
import numpy as np
import matplotlib.pyplot as plt

WINDOW_SIZE = 20
ZERO_VAL = 0
CONVERSION_RATE = 1
ser = serial.Serial(6, 9600)

def calibrate():
	vals = []
	for t in range(30):
		x = int(ser.readline())
		vals.append(x)
	zeroSum = sum(vals)
	global ZERO_VAL
	ZERO_VAL = zeroSum/len(vals)
	print "value to be set as 0: " + str(ZERO_VAL)
	print "please place a weight on the sensor. Press enter when ready to begin calibration"
	sys.stdin.readline()
	vals = []
	for t in range(30):
		x = int(ser.readline()) - ZERO_VAL
		if x<0:
			x=0
		vals.append(x)
	weightSum = sum(vals)
	wegithVal = weightSum/len(vals)
	print "please enter the weight of the object in kilograms"
	weight = sys.stdin.readline()
	global CONVERSION_RATE
	CONVERSION_RATE = int(weight)/wegithVal
	print "conversion rate calculated to be: " + str(CONVERSION_RATE) + " kg per unit"
	
def main():
	calibrate()
	vals = []
	while True:
		global CONVERSION_RATE
		global ZERO_VAL
		global WINDOW_SIZE
		x = int(ser.readline()) - ZERO_VAL
		force = CONVERSION_RATE*(x)*10
		print "" + str(force) + " N" + " " + str(x) 
		vals.append(x)
		if len(vals) > WINDOW_SIZE:
			vals.pop(0)
		plt.plot(vals)
		plt.show()
		
main()
