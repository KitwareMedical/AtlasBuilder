import os
import csv



##############################
class AtlasBase(object):
    
    '''the base class for the atlas'''
    def __init__( self, name ):
        self.Name = name
        pass
    
    def WriteAtlasToFile( self, outputpath ):
        pass
    
    def RestoreAtlas( self, inputpath ):
        pass

    
##############################
class ProgrammableAtlas(AtlasBase):
    
    '''class that represents the full atlas'''
    def __init__( self, name ):
        super(ProgrammableAtlas, self).__init__(name)
        self.Initialize = False
        self.Headers = dict()
        self.Data = []
        pass

    # extracts data only if it has not happened yet
    def ExtractData( self, inputpath ):
        if self.Initialize == False:
            self.__ParseCSV(inputPath)
            self.Initialize == True
        
    # this enables the reading of an arbitrary csv file
    def __ParseCSV( self, inputpath ):
        with open(inputpath, 'rb') as csvFile:
            reader = csv.reader(csvFile, delimiter=',', quotechar='"')
            header = True
            for row in reader:
                if (header):
                    header = False
                    for i,var in enumerate(row):
                        self.Headers[var] = i
                        self.Data.append([])
                    continue
                for i,val in enumerate(row):
                    self.Data[i].extend(val)
                    
                    
    def GenerateModel( self, xvar, yvar):
        pass
        
        
        