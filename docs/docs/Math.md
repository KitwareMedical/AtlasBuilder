# Mathematical Explanation

---

## Background

Most people are familiar with the basic form of a boxplot. It is a graph that visuallizes the median,
interquartile range, and outliers in a population described using point data. For instance you can show
the distribution of ages for a random sampling of 40 individuals. A boxplot is a visualization of qualities
about a population vs. the individuals contained within that population.

We run into problems if we want to try to represent anything besides point data. Howwever, it is easy to
imagine trying to identify the "most typical" individual in a sample population. For such asituation we 
would like to identify an individual instead of producing an average. An average representation could smooth
out the data and produce a representation that is not reflective of any of the individuals in the population.
This is often the case with weighted pointwise boxplots.

To solve this problem there needs to be a way to expand the definition of a median to be useful for
1-D (or N-D) data. To do this we reevaluate the median in the base case.

---

## Median and Band Depth

The typical explanation for the median value in a dataset is the "middle value" of that set. Algorithmically,
this specifies that you sort the dataset then find the N/2'th value in that list. That's the median. Unfortunately,
this algorithm doesn't work well beyond point data. How do you sort a set of sine functions, for instance. However,
there is another algorithm that will yeild the same median. For point data, each value is compared against a pair
of other values in the dataset. If the test value is between the other 2 values then its *depth* is incrimented. 
After this is done for all the data, the value with the highest depth is the median. 

### Band Depth

It is easy to see how this algorithm can be expanded to include functional data. With this new algorithm we check 
whether a test function is between any two other functions. However, there are instances where a function is between 
two others for all but a small portion of time. We account for this using the indicator function or the proportional
function. The indicator returns either a 1 or a 0 and the 1 requires the test function be bounded above and below by
the other functions at all times. The proportional function returns a value from 0 to 1 that reflects the amount of 
proportion of the range where the test function is bounded by the other functions. Once agian, testing all functions
against the function set yeilds a list of *band depths*. The function with the highest band depth is "median"

### J-value


One alternative to using the proportional function is to increase the number of functions the test value is compared
against. The problem with this is that it deviates from the conceptual understanding of what a median should be.
For point data this adds nothing beyond what is already acomplished by using only 2 other points. But with a function
it may expand the bounding region so the indicator function returns 1 more often. The AtlasBuilder module allows the
user to specify the j-value they desire.

---

## Weighted Band Depth

Often times the population the functions come from are not homgeneous. One would reasonably expect there to be some
distribution for a seperate variable. For example, we may have a set of functions that represent tree diameter as a
function of height. However, there would be drastic differences in the population depending on the age of the trees.
To represent an atlas that is more indicative of trees of a specific age we would assign weights to the functions
so that we would emphasize trees close to that age. This is independent of whether or not we want use the indicator
or proportional functions.

---

## 