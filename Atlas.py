import os
import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
import AtlasMath
import operator

##############################
class AtlasBase(object):
    
    '''the base class for the atlas'''
    def __init__( self, name ):
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
    def __init__( self, name ):
        super(ProgrammableAtlas, self).__init__(name)
        self.__SetPopulation = False
        self.__SetFunctions = False
        self.__Population = dict()
        self.__Functions = dict()
        self.PopulationPaths = []
        self.FunctionPaths = []
        self.CategoryKey = ''
        return


    def ProduceAtlas( self, stdev=None, center=None, populationvar=None, modified=False, jval=2 ):
        if not modified and populationvar is None:
            self.InclusionAtlas(jval)
            return
        elif not modified and populationvar is not None:
            self.WeightedInclusionAtlas(populationvar, stdev, center, jval)
            return
        elif modified and populationvar is None:
            self.ModifiedAtlas(jval)
            return
        elif modified and populationvar is not None:
            self.WeightedModifiedAtlas(populationvar, stdev, center, jval)
            return
        else:
            sys.stdout("Not a valid argument set")
            return


    def ParsePopulationData( self, pathlist=None ):
        if pathlist is None:
            pathlist = self.PopulationPaths
        self.__Population = dict()
        for inputpath in pathlist:
            self.ExtendPopulationData(inputpath)
        return
        

    def ExtendPopulationData( self, inputpath ):
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
                for i,val in enumerate(row):
                    self.__Population[names[i]].extend([float(val)])
        self.__SetPopulation = True
        return
        

    def DefineCategoryKey( self, key ):
        self.CategoryKey = key
        return


    def ParseFunctionData( self, pathlist=None ):
        self.__Functions = dict()
        if pathlist is None:
            pathlist = self.FunctionPaths
        for inputpath in pathlist:
            self.ExtendFunctionData(inputpath)
        return


    def ExtendFunctionData( self, inputpath ):
        with open(inputpath, 'rb') as csvFile:
            reader = csv.reader(csvFile, delimiter=',',quotechar='"')
            header = True
            names = []
            for row in reader:
                if (header):
                    header = False
                    for var in row:
                        self.__Functions[var] = []
                        names.append(var)
                    continue
                for i,val in enumerate(row):
                    self.__Functions[names[i]].extend([float(val)])
        self.__SetFunctions = True
        return


    def GenerateAtlas( self, modified=False, jval=2 ):
        if not self.__SetFunctions:
            sys.stdout("There is no function data")
            return
        bandDepthGenerator = AtlasMath.BandDepth.IndicatorBandDepth
        if modified:
            bandDepthGenerator = AtlasMath.BandDepth.ProportionalBandDepth
        # generate all band depths
        bandDepthScores = dict()
        for key in self.__Functions:
            function = self.__Functions[key]
            bandDepthScores[key] = bandDepthGenerator(function, self.__Functions.values(), jval)
        # order band depths
        sortedBandDepths = sorted(bandDepthScores.items(), key=operator.itemgetter(1))
        # plot the median, the 50% band, the fences, and outliers
        self.__PlotAtlas(sortedBandDepths)
        return


    '''
    "populationvar" is the variable used to give weights to the functions.
    "stdev" is the standard deviation of the gaussian weighting function.
    "center" is the center of the gaussian weighting function. 
    Functions with hidden variable values close to the center are weighted more than
    those that are far away.
    '''
    def GenerateWeightedAtlas( self, populationvar, stdev, center, modified=False, jval=2 ):
        if not self.__SetFunctions:
            sys.stdout("There is no function data")
            return
        if not self.__SetPopulation:
            sys.stdout("There is no population data to use to determine weights")
            return
        # Use the center and the stdev to generate weights for the functions
        hiddenVariableData = self.__Population[populationvar]
        weights = AtlasMath.Weighting.GenerateWeights(hiddenVariableData, stdev, center)

        bandDepthGenerator = AtlasMath.BandDepth.WeightedIndicatorBandDepth
        if modified:
            bandDepthGenerator = AtlasMath.BandDepth.WeightedProportionalBandDepth

        bandDepthScores = dict()
        for key in self.__Functions:
            function = self.__Functions[key]
            bandDepthScores[key] = bandDepthGenerator(function, self.__Functions.values(), weights, jval)

        sortedBandDepth = sorted(bandDepthScores.items(), key=operator.itemgetter(1))
        self.__PlotWeightedAtlas(sortedBandDepth, self.CategoryKey)
        return
        
        
    def __PlotAtlas( self, sortedfunctiontuples ):
        '''
        the function tuples come in key value pairs
        the keys are used with self.__Functions to 
        extract the actual function values
        '''
        median = self.Funtions[sortedfunctiontuples[0][0]]
        minimum = np.Inf + np.zeros(len(median))
        maximum = -np.Inf + np.zeros(len(median))
        half =  ceil(len(sortedfunctiontuples)/2.0)
        for pair in sortedfunctiontuples[:half]:
            maximum = np.maximum(maximum, self.__Functions[pair[0]])
            minimum = np.minimum(minimum, self.__Functions[pair[0]])

        self.__PlotLines(median, maximum, minimum)
        return


    def __PlotWeightedAtlas( self, sortedfunctiontuples, weightdict ):
        median = self.Funtions[sortedfunctiontuples[0][0]]
        minimum = np.Inf + np.zeros(len(median))
        maximum = -np.Inf + np.zeros(len(median))
        cumulativeWeight = weightdict[sortedfunctiontuples[0][0]]
        i = 1
        while cumulativeWeight < .5:
            maximum = np.maximum(maximum, self.Funtions[sortedfunctiontuples[i][0]])
            minimum = np.minimum(minimum, self.Funtions[sortedfunctiontuples[i][0]])
            cumulativeWeight += weightdict[sortedfunctiontuples[i][0]]
            i += 1

        self.__PlotLines(median, maximum, minimum)
        return


    def __PlotLines( self, median, maximum, minimum ):
        x = np.linspace(0.0, 1.0, len(median))
        # Plotting of lines
        plt.plot(x, median, 'k')
        plt.plot(x, maximum, 'b')
        plt.plot(x, minimum, 'b')

        plt.fill_between(x, minimum, maximum, color='magenta', alpha='0.5')
        plt.show()
        return


    def __MatchWeights( self, weights ):
        pairs = dict
        functionIDs = self.__Population[self.CategoryKey]
        for i,weight in enumerate(weights):
            pairs[functionIDs[i]] = weight
        return pairs

    
#############################
