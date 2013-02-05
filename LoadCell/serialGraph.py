import serial
import Tkinter as tk
import sys
import numpy as np
import matplotlib.pyplot as plt


root = tk.Tk()
WINDOW_SIZE = 20
KEY = ""
ZERO_VAL = 0
CONVERSION_RATE = 1
ser = serial.Serial(6, 9600)

def calibrate():
	print "calibrating zero..."
	vals = []
	for t in range(100):
		x = int(ser.readline())
		vals.append(x)
	zeroSum = sum(vals)
	global ZERO_VAL
	ZERO_VAL = zeroSum/len(vals)
	print "value to be set as 0: " + str(ZERO_VAL)
	print "please place a weight on the sensor. Press enter when ready to begin calibration"
	sys.stdin.readline()
	vals = []
	for t in range(100):
		x = int(ser.readline()) - ZERO_VAL
		if x<0:
			x=0
		print x
		vals.append(x)
	weightSum = sum(vals)
	weightVal = weightSum/len(vals)
	print "please enter the weight of the object in kilograms"
	weight = sys.stdin.readline()
	global CONVERSION_RATE
	if weightVal == 0:
		print "no weight was detected!"
		weightVal = 1
	CONVERSION_RATE = int(weight)/weightVal
	print "conversion rate calculated to be: " + str(CONVERSION_RATE) + " kg per unit"
	
def record():
	print "beginning recording..."	
	vals = []
	for i in range(100):
		global CONVERSION_RATE
		global ZERO_VAL
		global WINDOW_SIZE
		x = int(ser.readline()) - ZERO_VAL
		if x<0:
			x=0
		force = CONVERSION_RATE*(x)*10
		print "" + str(force) + " N" + " " + str(x) 
		vals.append(x)
		#if len(vals) > WINDOW_SIZE:
		#	vals.pop(0)
		
	plt.plot(vals)
	plt.ylabel('force')
	plt.xlabel('sample')
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
	calibrate()
	record()

	
main()
