import sys
import os
import csv
import random
import numpy as np
import math


def HorizontalLines(n=20, pointsperline=10):
	functionlist = []
	for i in range(n):
		yValue = random.random()*20
		function = []
		for x in range(pointsperline):
			function.append(yValue)
		functionlist.append(function)
	return functionlist


def SineFunctions(n=20, pointspercurve=10):
	functionlist = []
	xVals = np.linspace(0.0, 1.0, pointspercurve)
	for i in range(n):
		yOffset = random.random()*2
		function = []
		for x in xVals:
			function.append(math.sin(x) + yOffset)
		functionlist.append(function)
	return functionlist

def OffsetSines(n=20, pointspercurve=10):
	functionlist = []
	ages = np.linspace(0., 200. , n)
	xVals = np.linspace(0., 1., pointspercurve)
	for i in range(n):
		function = []
		for x in xVals:
			function.append(500.*(1. + math.sin(2*np.pi*x + .1*np.pi*i)) + 2.*ages[i])
		functionlist.append(function)
	return functionlist



def ThirdVariableGenerator(n=20, minV=0., maxV=1.):
	thirdVar = []
	for i in range(n):
		thirdVar.append(np.linspace(minV, maxV, n))
	return 

def WriteFunctionValues(fileobject, headers, functionlist):
	writer = csv.writer(fileobject)
	writer.writerow(headers)
	rows = []
	for i in range(len(functionlist[0])):
		rows.append([point[i] for point in functionlist])
        writer.writerows(rows)

def main():
	ScanIDs = range(20)
	# simple points
	file1 = open('SinglePoints.csv', 'wb')
	points = HorizontalLines(20,1)
	WriteFunctionValues(file1, ScanIDs, points)
	file1.close()

	# Horizontal lines with 4 points
	file2 = open('HorizontalLines4.csv', 'wb')
	functions = HorizontalLines(20,4)
	WriteFunctionValues(file2, ScanIDs, functions)
	file2.close()

	# Horizontal lines with 100 points
	file3 = open('HorizontalLines100.csv','wb')
	functions = HorizontalLines(20,100)
	WriteFunctionValues(file3, ScanIDs, functions)
	file3.close()

	# Sine Functions
	file4 = open('SineFunctions.csv','wb')
	functions = SineFunctions(20,100)
	WriteFunctionValues(file4, ScanIDs, functions)
	file4.close()

	# Offset Sines
	file5 = open('OffsetSines.csv','wb')
	functions = OffsetSines(20, 1000)
	WriteFunctionValues(file5, ScanIDs, functions)
	file5.close()

	# Third Variable
	file6 = open('PopulationData.csv','wb')
	headers = ['ScanID', 'Age']
	columns = [ScanIDs, np.linspace(0., 100., 20)]
	WriteFunctionValues(file6, headers, columns)
	file6.close()

if __name__ == '__main__':
	main()
