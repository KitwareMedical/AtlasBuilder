### need to develop the pediatric airways atlas. first I need data though. LOLOLOL
import sys

sys.path.append('../..')

from Atlas import *
#################################

''' The two following input functions can be 
	changed to fit hpw the data is stored '''
def UsePopulationData(atlas, inputpath):
	pass

def UseFunctionData(atlas, inputpath):
	pass
'''
Use a function to alter data stored in atlas.
This should be instance specific.
'''
def ModifyFunctions(atlas):
	pass

def DisplayAtlas(**kwargs):

def InitializeAtlas():
	'''
	the keywords should allow the automatic use of specific atlas type
	'''
	atlas = ProgrammableAtlas("Example Atlas")
	UsePopulationData(atlas, "example/path")
	UseFunctionData(atlas, "example/path2")
	ModifyFunctions(atlas)
	DisplayAtlas('list of keywords')
	return

def main():


	InitializeAtlas()
	return

#################################

if __name__ == '__main__':
	main()