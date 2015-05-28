import sys
import statsmodels.graphics.functional as fn
import csv
import numpy as np

sys.path.append('..')

from Atlas import *

##########################################

def ParseCSV( csvFileName ):
    out = []
    with open(csvFileName, 'rb') as csvFile:
        reader = csv.reader(csvFile, delimiter=',', quotechar='"')
        skip = True
        for row in reader:
            if (skip):
                skip = False
                for fn in row:
                	out.append([])
                continue
            for i, val in enumerate(row):
            	out[i].append(float(val))
    return out

def NormalDist(stdev=15., center=100., minv=0, maxv=200):
    return [np.exp(-((i - center)**2.)/(2.*(stdev**2.))) for i in range(minv, maxv)]

def main():
    pointAtlas = ProgrammableAtlas("Points")
    line4Atlas = ProgrammableAtlas("Horizontal4")
    line100Atlas = ProgrammableAtlas("Horizontal100")
    sineAtlas = ProgrammableAtlas("Sine")
    offsetAtlas = ProgrammableAtlas("Off")
    crossAtlas = ProgrammableAtlas("Cross")

    pointAtlas.ParseFunctionData(['SinglePoints.csv'])
    line4Atlas.ParseFunctionData(['HorizontalLines4.csv'])
    line100Atlas.ParseFunctionData(['HorizontalLines100.csv'])
    sineAtlas.ParseFunctionData(['SineFunctions.csv'])
    offsetAtlas.ParseFunctionData(['OffsetSines.csv'])
    crossAtlas.ParseFunctionData(['Crossing.csv'])

    line4Atlas.ParsePopulationData(['PopulationData.csv'])
    line100Atlas.ParsePopulationData(['PopulationData.csv'])
    sineAtlas.ParsePopulationData(['PopulationData.csv'])
    offsetAtlas.ParsePopulationData(['PopulationData.csv'])
    crossAtlas.ParsePopulationData(['PopulationData.csv'])


    # pointAtlas.ProduceAtlas()
    # line4Atlas.ProduceAtlas()
    # line100Atlas.ProduceAtlas()
    # sineAtlas.ProduceAtlas()


    # pointAtlas.ProduceAtlas(proportional=True)
    # line4Atlas.ProduceAtlas(proportional=True)
    # line100Atlas.ProduceAtlas(proportional=True)
    # sineAtlas.ProduceAtlas(proportional=True)
    functions = ParseCSV('OffsetSines.csv')

    line4Atlas.CategoryKey = 'ScanID'
    line100Atlas.CategoryKey = 'ScanID'
    sineAtlas.CategoryKey = 'ScanID'
    offsetAtlas.CategoryKey = 'ScanID'
    crossAtlas.CategoryKey = 'ScanID'


    # line4Atlas.ProduceAtlas(
    #     proportional=False, populationvar='Age', stdev=100., center=20.)
    # line100Atlas.ProduceAtlas(
    #     proportional=False, populationvar='Age', stdev=100., center=200.)
    
    # crossAtlas.ProduceAtlas(
    #     proportional=False, populationvar='Age', stdev=100., center=200.)
    f, (ax0, ax1) = plt.subplots(2)
    # fn.fboxplot(functions, xdata=np.linspace(0., 1., 100), ax=ax1)
    a = NormalDist(15., 15.)
    b = NormalDist(15., 100.)
    c = NormalDist(15., 200.)
    x = range(200)
    xdata = np.linspace(0, 200, 30)
    ydata = np.ones(30)/2.
    ax0.plot(xdata, ydata, 'bo')
    ax0. plot(x, a)
    # ax0. plot(x, b)
    # ax0. plot(x, c)

    line100Atlas.ProduceAtlas(proportional=False, populationvar='Age', stdev=15., center=15., ax=ax1)

    # line100Atlas.ProduceAtlas(proportional=False, populationvar='Age', stdev=15., center=100., ax=ax3)

    # line100Atlas.ProduceAtlas(proportional=False, populationvar='Age', stdev=15., center=200., ax=ax5)

    
    
    

    # offsetAtlas.ProduceAtlas(
    #     proportional=True, populationvar='Age', stdev=100., center=20., ax=ax1)
    
    # # line100Atlas.ProduceAtlas(
    # #     proportional=True, populationvar='Age', stdev=100., center=200.)
    # offsetAtlas.ProduceAtlas(
    #     proportional=True, populationvar='Age', stdev=100., center=180., ax=ax2)
    # plt.show()
    # crossAtlas.ProduceAtlas(
    #     proportional=True, populationvar='Age', stdev=100., center=200.)
    # offsetAtlas.ProduceAtlas(
    #     proportional=True, populationvar='Age', stdev=70., center=20.)
    plt.show()
#################################

if __name__ == '__main__':
    main()