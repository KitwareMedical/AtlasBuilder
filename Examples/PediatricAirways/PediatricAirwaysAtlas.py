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


def UsePopulationData(atlas, categorykey):
    atlas.DefineCategoryKey(categorykey)
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

def main():
    PediatricAirwaysAtlas = ProgrammableAtlas("Example Atlas")
    UsePopulationData(PediatricAirwaysAtlas, "CategoryKey")
    PediatricAirwaysAtlas.ParsePopulationData()
    UseFunctionData(PediatricAirwaysAtlas)
    # simply by defining the subplots beforehand and passing them you
    # can control the placement of the output graphs
    f, ax0 = plt.subplots(1)
    g, ax1 = plt.subplots(1)
    PediatricAirwaysAtlas.ProduceAtlas(ax=ax0)
    PediatricAirwaysAtlas.ProduceAtlas(proportional=True, ax = ax1)
    plt.show()
    return

#################################

if __name__ == '__main__':
    main()
