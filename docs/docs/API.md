# API

---
## Classes

1. AtlasBase
    - The base class for the atlas construction. This class has very limited functionality.
2. ProgrammableAtlas
    - This class stores data and generates the atlas graphs. It has multiple data import methods designed to minimize the effort required for a user to format their data.
    - Implements the 4 different algorithms used to generate atlas.
3. Weighting
    - A static class that uses a gaussian distribution to assign each function a weight.
4. BandDepth
    - A static class the contains methods to calculate band-depth of the functions. These methods are available to the user if they are needed.

---

## Functions

### Data Parsing

- **ParsePopulationFromCsv(pathlist=None)**
  
    Pass in a list of csv files and the data will be extracted and stored in the atlas.
    The data must be separated by column and each must have a unique header.

- **ExtendPopulationFromCsv(inputpath)**

    This function will take a csv file and add it's data to an existing dataset. The 
    data must have the same format as with ParsePopulationFromCsv.

- **ParsePopulationFromDict(populationdict)**

    Extracts data from dictionary user passes in and adds it to the atlas dataset.

- **ParsePopulationArray(poparray, rowdata=False, headers=True)**

    Pass in a 2D array of data to be parsed.

    "rowdata" is default as False and means the data is stored in columns. If True then data 
    is stored as rows.

    "headers" is a flag that indicates the data in the first row/column represents labels for the data.
    These will be read in and used as keys for the data when constructing a weighted atlas. If "headers" is
    False the keys will be integers starting at 0.

- **ParseCurveFromCsv(pathlist=None)**

    Very similar to ParsePopulationFromCsv except it is treated as functional data and stored in a different location.

- **ExtendCurveFromCsv(inputpath)**

    Same as for population data except different storage location.

- **ParseCurveFromDict(functiondict)**
    
    Again but with different storage location.

- **ParseCurveArray(funcarray, rowdata=False, headers=True)**

    Again but with different storage location.

### Constructing an Atlas

- **ProduceAtlas(proportional=False, populationvar=None, stdev=None, center=None, jval=2, ax=None)**

    This is the only method that the user needs to call to produce a curve atlas. To produce and indicator un-weighted
    boxplot all of the inputs are left with their default values. To produce a proportional un-weighted boxplot, 
    proportional should be set to "True". 

    ##### *Weighting*

    To produce a weighted curve boxplot "populationvar", "stdev", and "center" must be specified. The "populationvar" given
    is a header in the population data (i.e. 'Age'). The weight is calculated by a normal distribution over that variable with
    mean = "center" and standard deviation = "stdev". The sum of all the weights will be 1.

    The weighted atlas can use either the proportional or indicator function and is specified by the proportional flag.

    ##### *Extras*

    "jval" is where the band depth degree is specified. It must be an integer that is at least 2. The computational complexity 
    of creating an atlas is proportional to (n C "jval") where n is the number of functions. Increasing "jval" will dramatically 
    increase computation time. An explanation of band depth and the j-value can be found [here](/Math/).

    The user can use "ax" to specify how to plot the atlas. If it is left as default the atlas will be plotted on its own graph.
    The user can specify where to plot the atlas by passing in a matplotlib.pyplot.subplots() axis object. Examples are shown 
    in the [examples](/Examples/) page.

    This method also will return a dictionary of the curve keys matched with their band depths.

- **DefineCurveKey(key)**
    
    Before producing a weighted function boxplot you need to specify how the population data is assigned to the function data.
    Each function corresponds to a specific instance and the population data gives information on each instance. The user
    uses this function to align the population data with each function. The "key" provided should correspond to a header 
    from the population data.

- **GetCurves()**
    
    This function returns the dictionary that stores all of the currently uploaded curve data.

### BandDepth Methods

All BandDepth methods are static.

- **IndicatorBandDepth(curve, curveset, j=2)**

    Pass in the curve you are interested in calculating the band depth for, the total set of curves as a list of the curves,
    and the j-value. Returns the band depth of the curve without any weighting and using the indicator curve.

- **ProportionalBandDepth(curve, curveset, j=2)**

    Pass in the curve, list of all curves, and j-value. Returns the band depth based on no weighting and the proportional curve.

- **WeightedIndicatorBandDepth(key, curvedict, weightdict, j=2)**
    
    Pass in the curveID for the test curve, a dictionary that matches the curveIDs to the curve data, a dictionary that matches
    the curveID to the curve weight and the j-value. Returns the band depth of the test curve based on the weights and 
    using the indicator curve.

- **WeightedProportionalBandDepth(key, curvedict, weightdict, j=2)**

    Pass in the curveID for the test curve, a dictionary that matches the curveIDs to the curve data, a dictionary that matches
    the curveID to the curve weight and the j-value. Returns the band depth of the test curve based on the weights and 
    using the proportional curve.

- **Indicator(curve, bandset)**

    Pass in test curve and a list of two or more curves. Will return the value 0 if the test curve is not bounded by the set of curves
    in the bandset. Will return 1 otherwise.

- **Proportion(curve, bandset)**

    Pass in test curve and a list of two or more curves. Will return a number from 0 to 1 based on the proportion of the domain that the 
    test curve is bounded by the curves in the bandset.

- **GenerateFences(minimum, maximum, median)**

    Pass in the median curve, first quartile curve, and third quartile curve. These inputs should be the same shape. Will return 2 curves ina list to represent the upper fence
    and lower fence used to identify outliers.