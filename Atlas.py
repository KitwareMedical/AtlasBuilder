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
        self.__SetFunctions = False
        self.__Population = dict()
        self.__Functions = dict()
        self.PopulationPaths = []
        self.FunctionPaths = []
        self.CategoryKey = None
        self.__Plot = None
        return

    def ProduceAtlas(self, stdev=None, center=None, populationvar=None, proportional=False, jval=2, ax=None):
        self.__ConvertData()
        self.__SetPlot(ax)
        if populationvar is None:
            self.__GenerateAtlas(proportional, jval)
            return
        elif populationvar is not None:
            self.__ConvertData(populationvar)
            self.__GenerateWeightedAtlas(populationvar, stdev, center, proportional, jval)
            return
        else:
            sys.stdout.write("Not a valid argument set\n")
            return

    def ParsePopulationData(self, pathlist=None):
        if pathlist is None:
            pathlist = self.PopulationPaths
        self.__Population = dict()
        for inputpath in pathlist:
            self.ExtendPopulationData(inputpath)
        return

    def ExtendPopulationData(self, inputpath):
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

    def DefineCategoryKey(self, key):
        self.CategoryKey = key
        return

    def ParseFunctionData(self, pathlist=None):
        self.__Functions = dict()
        if pathlist is None:
            pathlist = self.FunctionPaths
        for inputpath in pathlist:
            self.ExtendFunctionData(inputpath)
        return

    def ExtendFunctionData(self, inputpath):
        with open(inputpath, 'rb') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            header = True
            names = []
            for row in reader:
                if (header):
                    header = False
                    for var in row:
                        self.__Functions[var] = []
                        names.append(var)
                    continue
                for i, val in enumerate(row):
                    self.__Functions[names[i]].extend([val])
        self.__SetFunctions = True
        return

    def __GenerateAtlas(self, proportional=False, jval=2):
        if not self.__SetFunctions:
            sys.stdout.write("There is no function data\n")
            return
        bandDepthGenerator = AtlasMath.BandDepth.IndicatorBandDepth
        if proportional:
            bandDepthGenerator = AtlasMath.BandDepth.ProportionalBandDepth
        # generate all band depths
        bandDepthScores = dict()
        #initialize dictionary
        for key in self.__Functions:
            bandDepthScores[key] = 0.
        # sum from j = 2 to jval
        for j in range(2,jval+1):
            for key in self.__Functions:
                function = self.__Functions[key]
                bandDepthScores[key] += bandDepthGenerator(
                    function, self.__Functions.values(), j)
        # order band depths
        sortedBandDepths = sorted(
            bandDepthScores.items(), key=operator.itemgetter(1), reverse=True)
        # plot the median, the 50% band, the fences, and outliers
        self.__PlotAtlas(sortedBandDepths)
        return

    def __GenerateWeightedAtlas(self, populationvar, stdev, center, proportional=False, jval=2):
        '''
        "populationvar" is the variable used to give weights to the functions.
        "stdev" is the standard deviation of the gaussian weighting function.
        "center" is the center of the gaussian weighting function. 
        Functions with hidden variable values close to the center are weighted more than
        those that are far away.
        '''
        if self.CategoryKey is None:
            sys.stdout.write("Need to set the Category Key\n")
            return
        if not self.__SetFunctions:
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
        print weights
        weightdict = self.__MatchWeights(weights)
        # Determine which band depth function to use
        bandDepthGenerator = AtlasMath.BandDepth.WeightedIndicatorBandDepth
        if proportional:
            bandDepthGenerator = AtlasMath.BandDepth.WeightedProportionalBandDepth
        # initialize dictionary
        bandDepthScores = dict()
        for key in self.__Functions:
            bandDepthScores[key] = 0.
        # Calculate the band depth for all of the functions
        for j in range(2,jval+1):
            for key in self.__Functions:
                function = self.__Functions[key]
                bandDepthScores[key] += bandDepthGenerator(
                    function, self.__Functions.values(), weights, j)
                print key, bandDepthScores[key]
                print key, weightdict[key]
        # sort by depth from deepest to shallowest
        sortedBandDepths = sorted(
            bandDepthScores.items(), key=operator.itemgetter(1), reverse=True)
        print "depths: ", sortedBandDepths
        print "weights: ", [(pair[0], weightdict[pair[0]]) for pair in sortedBandDepths]
        # plot the functional box plot
        self.__PlotWeightedAtlas(sortedBandDepths, weightdict)
        return

    def __PlotAtlas(self, sortedfunctiontuples):
        '''
        the function tuples come in key value pairs
        the keys are used with self.__Functions to 
        extract the actual function values
        '''
        median = self.__Functions[sortedfunctiontuples[0][0]]
        minimum = np.Inf + np.zeros(len(median))
        maximum = -np.Inf + np.zeros(len(median))
        outliers = []
        half = len(sortedfunctiontuples)//2
        # use the deepest half to determine the IQR
        for pair in sortedfunctiontuples[:half]:
            maximum = np.maximum(maximum, self.__Functions[pair[0]])
            minimum = np.minimum(minimum, self.__Functions[pair[0]])

        # need to edit this to calculate the fences and outliers
        lst = [self.__Functions[pair[0]] for pair in sortedfunctiontuples]
        inner_median = np.median(lst, axis=0)
        fences = AtlasMath.BandDepth.GenerateFences(minimum, maximum, inner_median)

        for pair in sortedfunctiontuples:
            if np.any(self.__Functions[pair[0]] > fences[0]) or np.any(self.__Functions[pair[0]] < fences[1]):
                outliers.append(self.__Functions[pair[0]])
        self.__PlotLines(median, maximum, minimum, outliers)
        return

    def __PlotWeightedAtlas(self, sortedfunctiontuples, weightdict):
        # initialize the data
        median = self.__Functions[sortedfunctiontuples[0][0]]
        minimum = np.Inf + np.zeros(len(median))
        maximum = -np.Inf + np.zeros(len(median))
        outliers = []
        cumulativeWeight = weightdict[sortedfunctiontuples[0][0]]
        i = 0
        # determine the functions in inter quartile range (IQR)
        while cumulativeWeight < .5:
            maximum = np.maximum(
                maximum, self.__Functions[sortedfunctiontuples[i][0]])
            minimum = np.minimum(
                minimum, self.__Functions[sortedfunctiontuples[i][0]])
            cumulativeWeight += weightdict[sortedfunctiontuples[i][0]]
            i += 1

        upperfence = maximum[:]
        lowerfence = minimum[:]
        fences = AtlasMath.BandDepth.GenerateFences(minimum, maximum, median)
        # Determine the functions in the 99.3% confidence interval
        while cumulativeWeight < .993:
            upperfence = np.maximum(
                upperfence, self.__Functions[sortedfunctiontuples[i][0]])
            lowerfence = np.minimum(
                lowerfence, self.__Functions[sortedfunctiontuples[i][0]])
            cumulativeWeight += weightdict[sortedfunctiontuples[i][0]]
            i += 1
        fences = [
            np.minimum(upperfence, fences[0]), np.maximum(lowerfence, fences[1])]
        # the left over functions are outliers
        for pair in sortedfunctiontuples[i:]:
            outliers.append(self.__Functions[pair[0]])
        self.__PlotLines(median, maximum, minimum, outliers, fences)
        return

    def __PlotLines(self, median, maximum, minimum, outliers, fences=[]):
        # TODO: Pass in information to use for the axes (finally get to use self.Name!!!)
        x = np.linspace(0.0, 1.0, len(median))
        self.__Plot.plot(x, maximum, color='b', linestyle='-')
        self.__Plot.plot(x, minimum, color='b', linestyle='-')
        self.__Plot.fill_between(x, minimum, maximum, color='magenta', alpha='0.5')
        for bound in fences:
            self.__Plot.plot(x, bound, color='b', linestyle='-')
        for function in outliers:
            self.__Plot.plot(x, function, color='0.5', linestyle=':')
        self.__Plot.plot(x, median, color='k', linestyle='-', lw=2.)
        return

    def __MatchWeights(self, weights):
        pairs = dict()
        functionIDs = self.__Population[self.CategoryKey]
        for i, weight in enumerate(weights):
            pairs[functionIDs[i]] = weight
        return pairs

    def __ConvertData(self, field=None):
        if field is None:
            for key in self.__Functions:
                function = self.__Functions[key]
                self.__Functions[key] = [float(i) for i in function]
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


#############################
