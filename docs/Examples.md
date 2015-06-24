# Examples

---

## Basics

AtlasBuilder uses matplotlib.pyplot and abbreviates it as plt. This is why you see plt.show() at the end of each example.
You will not have to import matplotlib.pyplot yourself but should have it installed on you machine.

### Unweighted Indicator Atlas

    import AtlasBuilder
    import matplotlib.pyplot as plt
    
    atlas0 = ProgrammableAtlas("Example0")
    atlas0.ParseFunctionFromCsv(["Functions.csv"])
    atlas0.ProduceAtlas()

    plt.show()

### Unweighted Proportional Atlas

    import AtlasBuilder
    import matplotlib.pyplot as plt

    atlas1 = ProgrammableAtlas("Example1")
    atlas1.ParseFunctionFromCsv(["Functions.csv"])
    atlas1.ProduceAtlas(proportional=True)
    
    plt.show()

### Weighted Indicator Atlas

    import AtlasBuilder
    import matplotlib.pyplot as plt

    atlas2 = ProgrammableAtlas("Example2")
    atlas2.ParseFunctionFromCsv(['Functions.csv'])
    atlas2.ParsePopulationFromCsv(['PopulationData.csv'])
    atlas2.DefineFunctionKey('ScanID')
    atlas2.ProduceAtlas(populationvar='Age', center=30, stdev=10)

    plt.show()

### Weighted Proportional Atlas

    import AtlasBuilder
    import matplotlib.pyplot as plt

    atlas3 = ProgrammableAtlas("Example3")
    atlas3.ParseFunctionFromCsv(['Functions.csv'])
    atlas3.ParsePopulationFromCsv(['PopulationData.csv'])
    atlas3.DefineFunctionKey('ScanID')
    atlas3.ProduceAtlas(proportional=True, populationvar='Age', center=30, stdev=10)

    plt.show()

## Plotting 

### 2x2 Grid

    import AtlasBuilder
    import matplotlib.pyplot as plt

    f, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2)

    atlas4 = ProgrammableAtlas("Example4")
    atlas4.ParseFunctionFromCsv(['Functions.csv'])
    atlas4.ParsePopulationFromCsv(['PopulationData.csv'])
    atlas4.DefineFunctionKey('ScanID')
    atlas4.ProduceAtlas(proportional=False, populationvar='Age', center=30, stdev=10, ax=ax0)
    atlas4.ProduceAtlas(proportional=True, populationvar='Age', center=30, stdev=10, ax=ax1)
    atlas4.ProduceAtlas(proportional=False, populationvar='Age', center=60, stdev=10, ax=ax2)
    atlas4.ProduceAtlas(proportional=True, populationvar='Age', center=60, stdev=10, ax=ax3)

    plt.show()

### Separate Population Variables

    import AtlasBuilder
    import matplotlib.pyplot as plt

    f, (ax0, ax1) = plt.subplots(2)

    atlas5 = ProgrammableAtlas("Example5")
    atlas5.ParseFunctionFromCsv(['Functions.csv'])
    atlas5.ParsePopulationFromCsv(['PopulationData.csv'])
    atlas5.DefineFunctionKey('ScanID')
    atlas5.ProduceAtlas(proportional=True, populationvar='Age', center=30, stdev=10, ax=ax0)
    atlas5.ProduceAtlas(proportional=True, populationvar='Weight', center=72, stdev=15, ax=ax1)

    plt.show()

### Overlapping

    import AtlasBuilder
    import matplotlib.pyplot as plt

    f, ax0 = plt.subplots(1)

    atlas6 = ProgrammableAtlas("Example6")
    atlas6.ParseFunctionFromCsv(['Functions.csv'])
    atlas6.ParsePopulationFromCsv(['PopulationData.csv'])
    atlas6.DefineFunctionKey('ScanID')
    atlas6.ProduceAtlas(proportional=True, populationvar='Age', center=30, stdev=10, ax=ax0)
    atlas6.ProduceAtlas(proportional=True, populationvar='Weight', center=72, stdev=15, ax=ax0)

    plt.show()