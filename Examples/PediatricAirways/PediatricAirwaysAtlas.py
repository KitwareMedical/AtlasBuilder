# need to develop the pediatric airways atlas. first I need data though.
import sys

sys.path.append('../..')

rootpath = 'Path/goes/here'

from Atlas import *
#################################

''' The two following input functions can be 
	changed to fit hpw the data is stored '''


def UsePopulationData(atlas, inputpath):
    atlas.DefineCategoryKey('Key')
    # can define dataset in one of two ways
    atlas.PopulationPaths = ['Fill in the list']
    atlas.ParsePopulationData()
    # or
    atlas.ParsePopulationData(['same list as earlier'])
    pass


def UseFunctionData(atlas, inputpath):
    pass
'''
Use a function to alter data stored in atlas.
This should be instance specific.
'''


def ModifyFunctions(atlas):
    pass


def InitializeAtlas():
    '''
    the keywords should allow the automatic use of specific atlas type
    '''
    atlas = ProgrammableAtlas("Example Atlas")
    UsePopulationData(atlas, "example/path")
    UseFunctionData(atlas, "example/path2")
    ModifyFunctions(atlas)
    # the keywords describe the type of atlas (Indicator/no weighted/no)
    atlas.ProduceAtlas("lots of keywords to set the stage")
    return


def main():

    InitializeAtlas()
    return

#################################

if __name__ == '__main__':
    main()
