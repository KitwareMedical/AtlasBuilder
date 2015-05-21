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
        pass

    
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
        self.Population = dict()
        self.Functions = dict()
        pass


    def ParsePopulationData( self, inputpath ):
        self.Population = dict()

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
        pass
        

    def ParseFunctionData( self, inputpath ):
        self.Functions = dict()

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
        pass


    def InclusionAtlas( self, jval=2 ):
        # generate all band depths
        bandDepthScores = dict()
        for key in self.Functions:
            function = Functions[key]
            bandDepthScores[key] = AtlasMath.BandDepth.IndicatorBandDepth(function, self.Functions.values(), jval)
        # order band depths
        sortedBandDepths = sorted(bandDepthScores.items(), key=operator.itemgetter(1))

        # plot the median, the 50% band, the fences, and outliers
        self.__PlotAtlas(sortedBandDepths)

        pass

    def ModifiedAtlas( self, jval=2 ):
        # generate all band depths
        bandDepthScores = dict()
        for key in self.Functions:
            function = Functions[key]
            bandDepthScores[key] = AtlasMath.BandDepth.ProportionalBandDepth(function, self.Functions.values(), jval)
        # order band depths
        sortedBandDepths = sorted(bandDepthScores.items(), key=operator.itemgetter(1))
        
        self.__PlotAtlas(sortedBandDepths)
        
        pass


    '''
    "key" is the way to identify the matching between the population
    data and the function data. Should be a key in the population header dict.
    "populationvar" is the variable to use to give weights to the functions.
    "stdev" is the standard deviation of the gaussian weighting function.
    "center" is the center of the gaussian weighting function. 
    Functions with hidden variable values close to the center are weighted more than
    those that are far away.
    '''
    def WeightedInclusionAtlas( self, key, populationvar, stdev, center ):
        # Use the center and the stdev to generate weights for the functions
        hiddenVariableIndex = self.PopulationHeaders[populationvar]
        hiddenVariableData = self.PopulationData[hiddenVariableIndex]
        weights = AtlasMath.Weighting.GenerateWeights(hiddenVariableData, stdev, center)

        
        self.__PlotWeightedAtlas( )

        pass

    def WeightedModifiedAtlas( self, key, populationvar, stdev, center ):
        hiddenVariableIndex = self.PopulationHeaders[populationvar]
        hiddenVariableData = self.PopulationData[hiddenVariableIndex]
        weights = AtlasMath.Weighting.GenerateWeights(hiddenVariableData, stdev, center)
        pass
        
    def __PlotAtlas( self, sortedfunctiontuples ):
        '''
        the function tuples come in key value pairs
        the keys are used with self.Functions to 
        extract the actual function values
        '''
        median = self.Funtions[sortedfuntiontuples[0][0]]
        minimum = np.Inf + np.zeros(len(median))
        maximum = -np.Inf + np.zeros(len(median))
        half =  len(sortedfuntiontuples)/2
        for pair in sortedFunctionTuples[:half]:
            maximum = np.maximum(maximum, self.Functions[pair[0]])
            minimum = np.minimum(minimum, self.Functions[pair[0]])

        self.__plotlines__(median, maximum, minimum)
        pass

    def __PlotWeightedAtlas( self, sortedfuntiontuples, functionweights):
        pass

    def __plotlines__( self, median, maximum, minimum):
        x = np.linspace(0.0, 1.0, len(median))
        # Plotting of lines
        plt.plot(x, median, 'k')
        plt.plot(x, maximum, 'b')
        plt.plot(x, minimum, 'b')

        plt.fill_between(x, minimum, maximum, color='magenta', alpha='0.5')
        plt.show()
        pass
    

#############################
