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
        self.SetPopulation = False
        self.SetFunctions = False
        self.Population = dict()
        self.Functions = dict()
        return


    def ParsePopulationData( self, inputpath ):
        self.Population = dict()
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
                        self.Population[var] = []
                        names.append(var)
                    continue
                for i,val in enumerate(row):
                    self.Population[names[i]].extend([float(val)])
        self.SetPopulation = True
        return
        

    def ParseFunctionData( self, inputpath ):
        self.Functions = dict()
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
                        self.Functions[var] = []
                        names.append(var)
                    continue
                for i,val in enumerate(row):
                    self.Functions[names[i]].extend([float(val)])
        self.SetFunctions = True
        return


    def InclusionAtlas( self, jval=2 ):
        if not self.SetFunctions:
            sys.stdout("There is no function data")
            return
        # generate all band depths
        bandDepthScores = dict()
        for key in self.Functions:
            function = self.Functions[key]
            bandDepthScores[key] = AtlasMath.BandDepth.IndicatorBandDepth(function, self.Functions.values(), jval)
        # order band depths
        sortedBandDepths = sorted(bandDepthScores.items(), key=operator.itemgetter(1))
        # plot the median, the 50% band, the fences, and outliers
        self.__PlotAtlas(sortedBandDepths)
        return


    def ModifiedAtlas( self, jval=2 ):
        if not self.SetFunctions:
            sys.stdout("There is no function data")
            return
        # generate all band depths
        bandDepthScores = dict()
        for key in self.Functions:
            function = self.Functions[key]
            bandDepthScores[key] = AtlasMath.BandDepth.ProportionalBandDepth(function, self.Functions.values(), jval)
        # order band depths
        sortedBandDepths = sorted(bandDepthScores.items(), key=operator.itemgetter(1))
        # plot the median, the 50% band, the fences, and outliers
        self.__PlotAtlas(sortedBandDepths)
        return


    '''
    "categorykey" is the key that identifies how the population
    data and the function data match. It is a key in the population dict.
    "populationvar" is the variable used to give weights to the functions.
    "stdev" is the standard deviation of the gaussian weighting function.
    "center" is the center of the gaussian weighting function. 
    Functions with hidden variable values close to the center are weighted more than
    those that are far away.
    '''
    def WeightedInclusionAtlas( self, categorykey, populationvar, stdev, center, jval=2 ):
        if not self.SetFunctions:
            sys.stdout("There is no function data")
            return
        if not self.SetPopulation:
            sys.stdout("There is no population data to use to determine weights")
            return
        # Use the center and the stdev to generate weights for the functions
        hiddenVariableData = self.Population[populationvar]
        weights = AtlasMath.Weighting.GenerateWeights(hiddenVariableData, stdev, center)

        bandDepthScores = dict()
        for key in self.Functions:
            function = self.Functions[key]
            bandDepthScores[key] = AtlasMath.BandDepth.WeightedIndicatorBandDepth(function, self.Functions.values(), weights, jval)

        sortedBandDepth = sorted(bandDepthScores.items(), key=operator.itemgetter(1))
        self.__PlotWeightedAtlas(sortedBandDepth, categorykey)
        return


    def WeightedModifiedAtlas( self, categorykey, populationvar, stdev, center, jval=2 ):
        if not self.SetFunctions:
            sys.stdout("There is no function data")
            return
        if not self.SetPopulation:
            sys.stdout("There is no population data to use to determine weights")
            return
        hiddenVariableData = self.Population[populationvar]
        weights = AtlasMath.Weighting.GenerateWeights(hiddenVariableData, stdev, center)

        bandDepthScores = dict()
        for key in self.Functions:
            function = self.Functions[key]
            bandDepthScores[key] = AtlasMath.BandDepth.WeightedProportionalBandDepth(function, self.Functions.values(), weights, jval)

        sortedBandDepth = sorted(bandDepthScores.items(), key=operator.itemgetter(1))
        self.__PlotWeightedAtlas(sortedBandDepth, self.__matchweights__(weights, categorykey))
        return
        
        
    def __PlotAtlas( self, sortedfunctiontuples ):
        '''
        the function tuples come in key value pairs
        the keys are used with self.Functions to 
        extract the actual function values
        '''
        median = self.Funtions[sortedfunctiontuples[0][0]]
        minimum = np.Inf + np.zeros(len(median))
        maximum = -np.Inf + np.zeros(len(median))
        half =  ceil(len(sortedfunctiontuples)/2.0)
        for pair in sortedfunctiontuples[:half]:
            maximum = np.maximum(maximum, self.Functions[pair[0]])
            minimum = np.minimum(minimum, self.Functions[pair[0]])

        self.__plotlines__(median, maximum, minimum)
        return


    def __PlotWeightedAtlas( self, sortedfunctiontuples, weightdict):
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

        self.__plotlines__(median, maximum, minimum)
        return


    def __plotlines__( self, median, maximum, minimum):
        x = np.linspace(0.0, 1.0, len(median))
        # Plotting of lines
        plt.plot(x, median, 'k')
        plt.plot(x, maximum, 'b')
        plt.plot(x, minimum, 'b')

        plt.fill_between(x, minimum, maximum, color='magenta', alpha='0.5')
        plt.show()
        return


    def __matchweights__( self, weights, categorykey ):
        pairs = dict
        functionIDs = self.Population[categorykey]
        for i,weight in enumerate(weights):
            pairs[functionIDs[i]] = weight
        return pairs

    
#############################
