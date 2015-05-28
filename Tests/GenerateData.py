import sys
import os
import csv
import random
import numpy as np
import math


def HorizontalLines(n=20, pointsperline=10):
    functionlist = []
    ys = np.linspace(0, 20, 30)
    for i in range(n):
        function = []
        for x in range(pointsperline):
            function.append(ys[i])
        functionlist.append(function)
    return functionlist


def SineFunctions(n=20, pointspercurve=10):
    functionlist = []
    xVals = np.linspace(0.0, 1.0, pointspercurve)
    ys = np.linspace(0., 2., 30.)
    for i in range(n):
        function = []
        for x in xVals:
            function.append(math.sin(x) + ys[i])
        functionlist.append(function)
    return functionlist


def OffsetSines(n=20, pointspercurve=10):
    functionlist = []
    ages = np.linspace(0., 200., n)
    xVals = np.linspace(0., 1., pointspercurve)
    for i in range(n):
        function = []
        for x in xVals:
            function.append(
                500.*(1. + math.sin(2*np.pi*x + .1*np.pi*i)) + 2.*ages[i])
        functionlist.append(function)
    return functionlist

def Crossing(n=20, pointspercurve=10):
    functionlist = []
    ages = np.linspace(0., 200., n)
    xVals = np.linspace(0., 1., pointspercurve)
    for i in range(n):
        function = []
        a = random.random()
        for x in xVals:
            function.append((10 - ages[i]/20.)*x + a*ages[i]/20.)
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
    ScanIDs = range(30)
    # simple points
    file1 = open('SinglePoints.csv', 'wb')
    points = HorizontalLines(30, 1)
    WriteFunctionValues(file1, ScanIDs, points)
    file1.close()

    # Horizontal lines with 4 points
    file2 = open('HorizontalLines4.csv', 'wb')
    functions = HorizontalLines(30, 4)
    WriteFunctionValues(file2, ScanIDs, functions)
    file2.close()

    # Horizontal lines with 100 points
    file3 = open('HorizontalLines100.csv', 'wb')
    functions = HorizontalLines(30, 100)
    WriteFunctionValues(file3, ScanIDs, functions)
    file3.close()

    # Sine Functions
    file4 = open('SineFunctions.csv', 'wb')
    functions = SineFunctions(30, 100)
    WriteFunctionValues(file4, ScanIDs, functions)
    file4.close()

    # Offset Sines
    file5 = open('OffsetSines.csv', 'wb')
    functions = OffsetSines(30, 100)
    WriteFunctionValues(file5, ScanIDs, functions)
    file5.close()

    # Crossing Lines
    file6 = open('Crossing.csv', 'wb')
    functions = Crossing(30, 100)
    WriteFunctionValues(file6, ScanIDs, functions)
    file6.close()

    # Third Variable
    file7 = open('PopulationData.csv', 'wb')
    headers = ['ScanID', 'Age']
    columns = [ScanIDs, np.linspace(0., 200., 30)]
    WriteFunctionValues(file7, headers, columns)
    file7.close()

if __name__ == '__main__':
    main()
