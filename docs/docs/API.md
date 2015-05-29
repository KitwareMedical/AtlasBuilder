# API

---

## Classes

1. AtlasBase
    - The base class for the atlas construction. This class has very limited functionality.
2. ProgrammableAtlas
    - This class stores data and gerneates the atlas graphs. It has multiple data import methods designed to minimize the effort required for a user to format their data.
    - Implements the 4 different algorithms used to generate atlas.
3. Weighting
    - A static class that uses a gaussian distribution to assign each function a weight.
4. BandDepth
    - A static class the contains methods to calculate band-depth of the functions. These functionas are available to the user if they are needed.

---

## Functions

### Data Parsing

- **ParsePopulationFromCsv(pathlist=None)**
  
    Pass in a list of csv files and the data will be extracted and stored in the atlas.
    The data must be seperated by column and each must have a unique header.

- **ExtendPopulationFromCsv(inputpath)**

    This function will take a csv file and add it's data to an existing dataset. The 
    data must have the same format as with ParsePopulationFromCsv.

- **ParsePopulationFromDict(populationdict)**

    Extracts data from dictionary user passes in and adds it to the atlas dataset.

- **ParsePopulationArray(poparray, rowdata=False, headers=True)**

    Pass in a 2D array of data to be parsed.

    "rowdata" is default as False and means the data is stored in columns. If True then data 
    is stored as rows.

    "headers" is a flag that indicates the data in the first row/collumn represents labels for the data.
    These will be read in and used as keys for the data when constructing a weighted atlas. If "headers" is
    False the keys will be integers starting at 0.

- **ParseFunctionFromCsv(pathlist=None)**

    Very similar to ParsePopulationFromCsv except it is treated as functional data and stored in a different location.

- **ExtendFunctionFromCsv(inputpath)**

    Same as for population data except different storage location aswell.

- **ParseFunctionFromDict(functiondict)**
    
    Again but with different storage.

- **ParseFunctionArray(funcarray, rowdata=False, headers=True)**

    Again but with different storage.

### Constructing an Atlas

- **ProduceAtlas(proportional=False, populationvar=None, stdev=None, center=None, jval=2, ax=None)**

    This is the only function that the user needs to call to produce a function atlas. To produce and indicator un-weighted
    boxplot all of the inputs are left with their default values. To produce a proportional un-weighted boxplot, 
    proportional should be set to "True". 

    ##### *Weighting*

    To produce a weighted function boxplot "populationvar", "stdev", and "center" must be specified. The "populationvar" given
    is a header in the population data (i.e. 'Age'). The weight is calculated by a normal distribution over that variable with
    mean = "center" and standar deviation = "stdev". The sum of all the weights will be 1.

    The weighted atlas can be either proportional or indicative which is specified by the proportional flag.

    ##### *Extras*

    "jval" is where the band depth "degree" is specified. It must be at least 2. The computational complexity of creating an atlas
    is proportional to (n C "jval") where n is the number of functions. Increasing "jval" will dramatically increase computation
    time. More on the math behind band depth can be found [here](/Math/).

    The user can use "ax" to specify how to plot the atlas. If it is left as default the atlas will be plotted on its own graph.
    The user can specify where to plot the atlas by passing in a matplotlib.pyplot.subplots() axis object. Examples are shown 
    in the [examples](/Examples/) page.

- **DefineFunctionKey(key)**
    
    Before producing a weighted function boxplot you need to specify how the population data is assigned to the function data.
    Each function corresponds to a specific instance and the population data gives information on each instance. The user
    uses this function to allign the population data with each function. The "key" provided should correspond to a header 
    from the population data.




