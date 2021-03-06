# Copyright [2015] [Kitware inc.]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import statsmodels.graphics.functional as fn
import csv
import numpy as np

sys.path.append('..')

from AtlasBuilder import *

##########################################


def ParseCSV(csvFileName):
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
    offsetAtlas = ProgrammableAtlas('Offset Atlas')
    crossAtlas = ProgrammableAtlas("Cross")

    pointAtlas.ParseCurveFromCsv(['SinglePoints.csv'])
    line4Atlas.ParseCurveFromCsv(['HorizontalLines4.csv'])
    line100Atlas.ParseCurveFromCsv(['HorizontalLines100.csv'])
    sineAtlas.ParseCurveFromCsv(['SineFunctions.csv'])
    offsetAtlas.ParseCurveFromCsv(['OffsetSines.csv'])
    crossAtlas.ParseCurveFromCsv(['Crossing.csv'])

    line4Atlas.ParsePopulationFromCsv(['PopulationData.csv'])
    line100Atlas.ParsePopulationFromCsv(['PopulationData.csv'])
    sineAtlas.ParsePopulationFromCsv(['PopulationData.csv'])
    offsetAtlas.ParsePopulationFromCsv(['PopulationData.csv'])
    crossAtlas.ParsePopulationFromCsv(['PopulationData.csv'])

    # pointAtlas.ProduceAtlas()
    # line4Atlas.ProduceAtlas()
    # line100Atlas.ProduceAtlas()
    # sineAtlas.ProduceAtlas()

    # pointAtlas.ProduceAtlas(proportional=True)
    # line4Atlas.ProduceAtlas(proportional=True)
    # line100Atlas.ProduceAtlas(proportional=True)
    # sineAtlas.ProduceAtlas(proportional=True)
    functions = ParseCSV('OffsetSines.csv')

    line4Atlas.CurveKey = 'ScanID'
    line100Atlas.CurveKey = 'ScanID'
    sineAtlas.CurveKey = 'ScanID'
    offsetAtlas.CurveKey = 'ScanID'
    crossAtlas.CurveKey = 'ScanID'

    # line4Atlas.ProduceAtlas(
    #     proportional=False, populationvar='Age', stdev=100., center=20.)
    # line100Atlas.ProduceAtlas(
    #     proportional=False, populationvar='Age', stdev=100., center=200.)

    # crossAtlas.ProduceAtlas(
    #     proportional=False, populationvar='Age', stdev=100., center=200.)
    f, ax0 = plt.subplots(1)
    g, ax1 = plt.subplots(1)
    # fn.fboxplot(functions, xdata=np.linspace(0., 1., 100), ax=ax2)
    a = NormalDist(25., 20.)
    b = NormalDist(25., 100.)
    c = NormalDist(25., 180.)
    x = range(200)
    xdata = np.linspace(0, 200, 30)
    ydata = np.ones(30)/2.
    # ax0.plot(xdata, ydata, 'bo')
    # ax0. plot(x, a)
    # ax0. plot(x, b)
    # ax0. plot(x, c)
    offsetAtlas.ProduceAtlas(ax=ax0)
    offsetAtlas.ProduceAtlas(proportional=True, ax=ax1)
    f, (ax2, ax3) = plt.subplots(2)
    offsetAtlas.ProduceAtlas(
        proportional=True, populationvar='Age', stdev=25., center=100., ax=ax2)

    offsetAtlas.ProduceAtlas(
        proportional=False, populationvar='Age', stdev=25., center=100., ax=ax3)

    # offsetAtlas.ProduceAtlas(
    # proportional=True, populationvar='Age', stdev=100., center=20., ax=ax1)

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
