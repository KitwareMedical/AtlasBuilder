import os
import csv
import sys
import AtlasMath

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
        self.PopulationHeaders = dict()
        self.FunctionHeaders = dict()
        self.PopulationData = []
        self.FunctionData = []
        self.Matched = False
        pass


    def ParsePopulationData( self, inputpath ):
        self.PopulationHeaders = dict()
        self.PopulationData = []

        with open(inputpath, 'rb') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            header = True
            for row in reader:
                if (header):
                    header = False
                    for i,var in enumerate(row):
                        self.PopulationHeaders[var] = i
                        self.PopulationData.append([])
                    continue
                for i,val in enumerate(row):
                    self.PopulationData[i].extend([val])
        

    def ParseFunctionData( self, inputpath ):
        self.FunctionHeaders = dict()
        self.FunctionData = []

        with open(inputpath, 'rb') as csvFile:
            reader = csv.reader(csvFile, delimiter=',',quotechar='"')
            header = True
            for row in reader:
                if (header):
                    header = False
                    for i,var in enumerate(row):
                        self.FunctionHeaders[var] = i
                        self.FunctionData.append([])
                    continue
                for i,val in enumerate(row):
                    self.FunctionData[i].extend([val])

    def __MatchedKey( self, key ):
        return key in self.PopulationHeaders and key in self.FunctionHeaders

    def GenerateInclusionAtlas( self, key ):
        pass

    def GenerateModifiedAtlas( self, key ):
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
    def GenerateWeightedInclusionAtlas( self, key, populationvar, stdev, center ):
        if not self.__MatchedKey(key):
            sys.stdout.write('The functions are not identifiable by the provided key')
            sys.exit(-1)

        # Use the center and the stdev to generate weights for the functions
        hiddenVariableIndex = self.PopulationHeaders[populationvar]
        hiddenVariableData = self.PopulationData[hiddenVariableIndex]
        weights = AtlasMath.Weighting.GenerateWeights(hiddenVariableData, stdev, center)


        pass

    def GenerateWeightedModifiedAtlas( self, key, populationvar, stdev, center ):
        pass
        
#############################
        