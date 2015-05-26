import numpy as np
import scipy.misc as misc
import itertools

################################


class Weighting:

    @staticmethod
    def GenerateWeights(data, stdev, center):
        weights = []
        running_sum = 0
        for value in data:
            w = np.exp(((value - center)**2)/(2*(stdev**2)))
            weights.extend([w])
            running_sum = running_sum + w
        return [i/running_sum for i in weights]


################################
class BandDepth:

    @staticmethod
    # Right now the functionsets are Dictionaries
    def IndicatorBandDepth(function, functionset, j=2):
        function
        bandDepth = 0.0
        normalizingValue = 1.0/misc.comb(len(functionset), j)
        for testBandSet in itertools.combinations(functionset, j):
            bandDepth = bandDepth + BandDepth.Indicator(function, testBandSet)
        return bandDepth*normalizingValue

    @staticmethod
    def ProportionalBandDepth(function, functionset, j=2):
        bandDepth = 0.0
        normalizingValue = 1.0/misc.comb(len(functionset), j)
        for testBandSet in itertools.combinations(functionset, j):
            bandDepth = bandDepth + BandDepth.Proportion(function, testBandSet)
        return bandDepth*normalizingValue

    @staticmethod
    def WeightedIndicatorBandDepth(function, functionset, weights, j=2):
        numerator = 0.0
        denominator = 0.0
        for indicies in itertools.combinations(range(len(weights)), j):
            weightSubset = BandDepth.ExtractSubset(weights, indicies)
            testBandSet = BandDepth.ExtractSubset(functionset, indicies)
            product = BandDepth.ProductOfList(weightSubset)
            denominator += product
            numerator += product*BandDepth.Indicator(function, testBandSet)
        return numerator/denominator

    @staticmethod
    def WeightedProportionalBandDepth(function, functionset, weights, j=2):
        numerator = 0.0
        denominator = 0.0
        for indicies in itertools.combinations(range(len(weights)), j):
            weightSubset = BandDepth.ExtractSubset(weights, indicies)
            testBandSet = BandDepth.ExtractSubset(functionset, indicies)
            product = BandDepth.ProductOfList(weightSubset)
            denominator += product
            numerator += product*BandDepth.Proportion(function, testBandSet)
        return numerator/denominator

    @staticmethod
    def Indicator(function, bandset):
        '''
        returns 1 if the function is within the band 
        generated by the bandset for all x. 0 otherwise
        '''
        for x in range(len(function)):
            bandRange = BandDepth.BandBounds(bandset, x)
            if function[x] < bandRange[0] or function[x] > bandRange[1]:
                return 0.0
        return 1

    @staticmethod
    def Proportion(function, bandset):
        '''
        return the proportion of the domain where 
        function is betwen the band values
        '''
        proportion = 0.0
        for x in range(len(function)):
            bandRange = BandDepth.BandBounds(bandset, x)
            if (bandRange[0] <= function[x]) and (bandRange[1] >= function[x]):
                proportion = proportion + 1.0
        return proportion/len(function)

    @staticmethod
    def BandBounds(bandset, x):
        minVal = float("inf")
        maxVal = float("-inf")

        for function in bandset:
            if function[x] < minVal:
                minVal = function[x]
            if function[x] > maxVal:
                maxVal = function[x]

        return [minVal, maxVal]

    @staticmethod
    def ExtractSubset(objectset, indextuple):
        output = []
        for i in indextuple:
            output.append(objectset[i])
        return output

    @staticmethod
    def ProductOfList(numericallist):
        r = 1
        for i in numericallist:
            r *= i
        return r
