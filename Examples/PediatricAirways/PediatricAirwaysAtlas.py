# need to develop the pediatric airways atlas. first I need data though.
import sys
import matplotlib.pyplot as plt
import os

sys.path.append('../..')

datapath = 'Path/to/data/'

from Atlas import *
#################################

''' The two following input functions can be 
	changed to fit hpw the data is stored '''


def UsePopulationData(atlas):
    atlas.DefineCategoryKey(categorykey)
    # can define dataset in one of two ways
    atlas.PopulationPaths = [
        os.path.join(datapath,'populationFile0.csv'),
        os.path.join(datapath,'populationFile1.csv'),
        os.path.join(datapath,'populationFile2.csv')]
    return


def UseFunctionData(atlas):
    '''
    Use a function to alter data stored in atlas.
    This should be instance specific.
    '''
    atlas.FunctionPaths = [
        os.path.join(datapath,'FunctionFile0.csv'),
        os.path.join(datapath,'FunctionFile1.csv'),
        os.path.join(datapath,'FunctionFile2.csv')]
    return

def ModifyFunctions(atlas):
    '''
    This is needed on a case by case basis.
    I suggest reading the function files, modifying the data 
    and writing the new data to a new file.
    '''
    pass



def main():
    PediatricAirwaysAtlas = ProgrammableAtlas("Example Atlas")
    UsePopulationData(PediatricAirwaysAtlas)
    PediatricAirwaysAtlas.ParsePopulationData()
    UseFunctionData(PediatricAirwaysAtlas)
    # simply by defining the subplots beforehand and passing them you
    # can control the placement of the output graphs
    f, ax = plt.subplots(1)
    g, ax1 = plt.subplots(1)
    PediatricAirwaysAtlas.ProduceAtlas(ax=ax1)
    PediatricAirwaysAtlas.ProduceAtlas(proportional=True, ax = ax)
    plt.show()
    return

#################################

if __name__ == '__main__':
    main()
