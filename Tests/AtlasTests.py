import sys

sys.path.append('..')

from Atlas import *

##########################################

def main():
	pointAtlas = ProgrammableAtlas("Points")
	line4Atlas = ProgrammableAtlas("Horizontal4")
	line100Atlas = ProgrammableAtlas("Horizontal100")
	sineAtlas = ProgrammableAtlas("Sine")
	offsetAtlas = ProgrammableAtlas("Off")

	pointAtlas.ParseFunctionData(['SinglePoints.csv'])
	line4Atlas.ParseFunctionData(['HorizontalLines4.csv'])
	line100Atlas.ParseFunctionData(['HorizontalLines100.csv'])
	sineAtlas.ParseFunctionData(['SineFunctions.csv'])
	offsetAtlas.ParseFunctionData(['OffsetSines.csv'])

	line4Atlas.ParsePopulationData(['PopulationData.csv'])
	line100Atlas.ParsePopulationData(['PopulationData.csv'])
	sineAtlas.ParsePopulationData(['PopulationData.csv'])
	offsetAtlas.ParsePopulationData(['PopulationData.csv'])


	# pointAtlas.GenerateAtlas()
	# line4Atlas.GenerateAtlas()
	# line100Atlas.GenerateAtlas()
	# sineAtlas.GenerateAtlas()

	# pointAtlas.GenerateAtlas(modified=True)
	# line4Atlas.GenerateAtlas(modified=True)
	# line100Atlas.GenerateAtlas(modified=True)
	# sineAtlas.GenerateAtlas(modified=True)
	# offsetAtlas.GenerateAtlas()
	# offsetAtlas.GenerateAtlas(modified=True)
	offsetAtlas.CategoryKey = 'ScanID'
	offsetAtlas.GenerateWeightedAtlas(populationvar='Age', stdev=25., center=50.)

if __name__ == '__main__':
	main()