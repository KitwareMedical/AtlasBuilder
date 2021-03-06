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
import os
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
import AtlasMath
import operator
import math

##############################


class AtlasBase(object):

    '''the base class for the atlas'''

    def __init__(self, name):
        self.Name = name
        return


##############################
class ProgrammableAtlas(AtlasBase):

    '''
    class that represents the full atlas.
    the population data is scalar data 
    about each function that is included. 
    The function data is used to produce 
    the atlas but because the functions are 
    not from a homogeneous sample we want to
    be able to describe a variable atlas.
    '''

    def __init__(self, name):
        super(ProgrammableAtlas, self).__init__(name)
        self.__SetPopulation = False
        self.PopulationPaths = []
        self.__Population = {}
        self.__SetCurves = False
        self.CurvePaths = []
        self.CurveKey = None
        self.__Curves = {}
        self.__Plot = None
        return

    def ProduceAtlas(self, proportional=False, populationvar=None, stdev=None, center=None, jval=2, ax=None):
        self.__ConvertData()
        self.__SetPlot(ax)
        if populationvar is None:
            return self.__GenerateAtlas(proportional, jval)
        elif populationvar is not None:
            self.__ConvertData(populationvar)
            return self.__GenerateWeightedAtlas(populationvar, stdev, center, proportional, jval)
        else:
            sys.stdout.write("Not a valid argument set\n")
            return None

    def ParsePopulationFromCsv(self, pathlist=None):
        if pathlist is None:
            pathlist = self.PopulationPaths
        self.__Population = {}
        for inputpath in pathlist:
            self.ExtendPopulationFromCsv(inputpath)
        return

    def ExtendPopulationFromCsv(self, inputpath):
        with open(inputpath, 'rb') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            header = True
            names = []
            for row in reader:
                if (header):
                    header = False
                    for var in row:
                        self.__Population[var] = []
                        names.append(var)
                    continue
                for i, val in enumerate(row):
                    self.__Population[names[i]].extend([val])
        self.__SetPopulation = True
        return

    def ParsePopulationFromDict(self, populationdict):
        for key in populationdict:
            self.__Population[key] = populationdict[key]
        self.__SetPopulation = True
        return

    def ParsePopulationArray(self, poparray, rowdata=False, headers=True):
        if not rowdata:
            self.__ParseRows(poparray, headers, self.__Population)
            return
        self.__ParseColumns(poparray, headers, self.__Population)

    def DefineCurveKey(self, key):
        if key not in self.__Population:
            sys.stdout.write(key + " is not key for population data")
        self.CurveKey = key
        return

    def ParseCurveFromCsv(self, pathlist=None):
        self.__Curves = {}
        if pathlist is None:
            pathlist = self.CurvePaths
        for inputpath in pathlist:
            self.ExtendCurveFromCsv(inputpath)
        return

    def ExtendCurveFromCsv(self, inputpath):
        with open(inputpath, 'rb') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            header = True
            names = []
            for row in reader:
                if (header):
                    header = False
                    for var in row:
                        self.__Curves[var] = []
                        names.append(var)
                    continue
                for i, val in enumerate(row):
                    self.__Curves[names[i]].extend([val])
        self.__SetCurves = True
        return

    def ParseCurveFromDict(self, functiondict):
        for key in functiondict:
            self.__Population[key] = functiondict[key]
        self.__SetCurves = True

    def ParseCurveArray(self, funcarray, rowdata=False, headers=True):
        if not rowdata:
            self.__ParseColumns(poparray, headers, self.__Curves)
            return
        self.__ParseRows(poparray, headers, self.__Curves)

    def GetCurves(self):
        return self.__Curves

    def GetPopulationData(self):
        return self.__Population

    def ParseCurveArray(self, funcarray, rowdata=False, headers=True):
        if not rowdata:
            self.__ParseColumns(poparray, headers, self.__Curves)
            return
        self.__ParseRows(poparray, headers, self.__Curves)

    def GetCurves(self):
        return self.__Curves

    def GetPopulationData(self):
        return self.__Population

    def __GenerateAtlas(self, proportional=False, jval=2):
        if not self.__SetCurves:
            sys.stdout.write("There is no function data\n")
            return
        bandDepthGenerator = AtlasMath.BandDepth.IndicatorBandDepth
        if proportional:
            bandDepthGenerator = AtlasMath.BandDepth.ProportionalBandDepth
        # generate all band depths
        bandDepthScores = {}
        # initialize dictionary
        for key in self.__Curves:
            bandDepthScores[key] = 0.
        # sum from j = 2 to jval
        for j in range(2, jval+1):
            for key in self.__Curves:
                function = self.__Curves[key]
                bandDepthScores[key] += bandDepthGenerator(
                    function, self.__Curves.values(), j)
        # order band depths
        sortedBandDepths = sorted(
            bandDepthScores.items(), key=operator.itemgetter(1), reverse=True)
        # plot the median, the 50% band, the fences, and outliers
        self.__PlotAtlas(sortedBandDepths)
        return bandDepthScores

    def __GenerateWeightedAtlas(self, populationvar, stdev, center, proportional=False, jval=2):
        '''
        "populationvar" is the variable used to give weights to the functions.
        "stdev" is the standard deviation of the gaussian weighting function.
        "center" is the center of the gaussian weighting function. 
        Curves with hidden variable values close to the center are weighted more than
        those that are far away.
        '''
        if self.CurveKey is None:
            sys.stdout.write(
                "Need to define the function Key: DefineCurveKey('key')\n")
            return
        if not self.__SetCurves:
            sys.stdout.write("There is no function data\n")
            return
        if not self.__SetPopulation:
            sys.stdout.write(
                "There is no population data to use to determine weights\n")
            return
        # Use the center and the stdev to generate weights for the functions
        hiddenVariableData = self.__Population[populationvar]
        weights = AtlasMath.Weighting.GenerateWeights(
            hiddenVariableData, stdev, center)
        weightdict = self.__MatchWeights(weights)
        # Determine which band depth function to use
        bandDepthGenerator = AtlasMath.BandDepth.WeightedIndicatorBandDepth
        if proportional:
            bandDepthGenerator = AtlasMath.BandDepth.WeightedProportionalBandDepth
        # initialize dictionary
        bandDepthScores = {}
        for key in self.__Curves:
            bandDepthScores[key] = 0.
        # Calculate the band depth for all of the functions
        for j in range(2, jval+1):
            for key in self.__Curves:
                bandDepthScores[
                    key] += bandDepthGenerator(key, self.__Curves, weightdict, j)
        # sort by depth from deepest to shallowest
        sortedBandDepths = sorted(
            bandDepthScores.items(), key=operator.itemgetter(1), reverse=True)
        # plot the functional box plot
        self.__PlotWeightedAtlas(sortedBandDepths, weightdict)
        return bandDepthScores

    def __PlotAtlas(self, sortedfunctiontuples):
        '''
        the function tuples come in key value pairs
        the keys are used with self.__Curves to 
        extract the actual function values
        '''
        median = self.__Curves[sortedfunctiontuples[0][0]]
        minimum = np.Inf + np.zeros(len(median))
        maximum = -np.Inf + np.zeros(len(median))
        outliers = []
        half = len(sortedfunctiontuples)//2
        # use the deepest half to determine the IQR
        for pair in sortedfunctiontuples[:half]:
            maximum = np.maximum(maximum, self.__Curves[pair[0]])
            minimum = np.minimum(minimum, self.__Curves[pair[0]])

        # calculate the fences and outliers
        lst = [self.__Curves[pair[0]] for pair in sortedfunctiontuples]
        inner_median = np.median(lst, axis=0)
        fences = AtlasMath.BandDepth.GenerateFences(
            minimum, maximum, inner_median)

        for pair in sortedfunctiontuples:
            if np.any(self.__Curves[pair[0]] > fences[0]) or np.any(self.__Curves[pair[0]] < fences[1]):
                outliers.append(self.__Curves[pair[0]])
        self.__PlotLines(median, maximum, minimum, outliers)
        return

    def __PlotWeightedAtlas(self, sortedfunctiontuples, weightdict):
        # initialize the data
        median = self.__Curves[sortedfunctiontuples[0][0]]
        minimum = np.Inf + np.zeros(len(median))
        maximum = -np.Inf + np.zeros(len(median))
        outliers = []
        cumulativeWeight = weightdict[sortedfunctiontuples[0][0]]
        i = 0
        # determine the functions in inter quartile range (IQR)
        while cumulativeWeight < .5:
            maximum = np.maximum(
                maximum, self.__Curves[sortedfunctiontuples[i][0]])
            minimum = np.minimum(
                minimum, self.__Curves[sortedfunctiontuples[i][0]])
            cumulativeWeight += weightdict[sortedfunctiontuples[i][0]]
            i += 1

        upperfence = maximum[:]
        lowerfence = minimum[:]
        fences = AtlasMath.BandDepth.GenerateFences(minimum, maximum, median)
        # Determine the functions in the 99.3% confidence interval
        while cumulativeWeight < .993:
            upperfence = np.maximum(
                upperfence, self.__Curves[sortedfunctiontuples[i][0]])
            lowerfence = np.minimum(
                lowerfence, self.__Curves[sortedfunctiontuples[i][0]])
            cumulativeWeight += weightdict[sortedfunctiontuples[i][0]]
            i += 1
        fences = [
            np.minimum(upperfence, fences[0]), np.maximum(lowerfence, fences[1])]
        # the left over functions are outliers
        for pair in sortedfunctiontuples[i:]:
            outliers.append(self.__Curves[pair[0]])
        self.__PlotLines(median, maximum, minimum, outliers, fences)
        return

    def __PlotLines(self, median, maximum, minimum, outliers, fences=[]):
        # TODO: Pass in information to use for the axes (finally get to use
        # self.Name!!!)
        x = np.linspace(0.0, 1.0, len(median))
        self.__Plot.plot(x, maximum, color='b', linestyle='-')
        self.__Plot.plot(x, minimum, color='b', linestyle='-')
        self.__Plot.fill_between(
            x, minimum, maximum, color='magenta', alpha='0.5')
        for bound in fences:
            self.__Plot.plot(x, bound, color='b', linestyle='-')
        for function in outliers:
            self.__Plot.plot(x, function, color='0.5', linestyle=':')
        self.__Plot.plot(x, median, color='k', linestyle='-', lw=2.)
        return

    def __MatchWeights(self, weights):
        pairs = {}
        functionIDs = self.__Population[self.CurveKey]
        for i, weight in enumerate(weights):
            pairs[functionIDs[i]] = weight
        return pairs

    def __ConvertData(self, field=None):
        if field is None:
            for key in self.__Curves:
                function = self.__Curves[key]
                self.__Curves[key] = [float(i) for i in function]
            return
        function = self.__Population[field]
        self.__Population[field] = [float(i) for i in function]
        return

    def __SetPlot(self, ax):
        if ax is None:
            f, self.__Plot = plt.subplots()
            return
        self.__Plot = ax
        return

    def __ParseRows(self, dataarray, headers=True, datadict=None):
        if datadict is None:
            sys.stdout.write('no location to store data specified')
            return
        if headers:
            keys = [row[0] for row in dataarray]
            functions = [row[1:] for row in dataarray]
            for i in range(len(keys)):
                datadict[keys[i]] = functions[i]
            return
        keys = [str(i) for i in range(np.shape(dataarray)[0])]
        functions = [row for row in dataarray]
        for i in range(len(keys)):
            datadict[keys[i]] = functions[i]

    def __ParseColumns(self, dataarray, headers=True, datadict=None):
        if datadict is None:
            sys.stdout.write('no location to store data specified')
            return
        if headers:
            names = dataarray[0]
            body = dataarray[1:]
            for i, key in enumerate(names):
                datadict[key] = [row[i] for row in body]
            return
        names = [str(i) for i in range(np.shape(dataarray)[1])]
        for i, key in enumerate(names):
            datadict[key] = [row[i] for row in dataarray]

#############################
