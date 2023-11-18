# All the packages that we need to import
import numpy as np               # for linear algebra
import pandas as pd              # for tabular output
from scipy.stats import rankdata # for ranking the candidates

#############################################################
#                     Pre-requisites                        #
#############################################################

# The given data encoded into vectors and matrices

attributes = np.array(["GRE", "GPA", "College ranking", "Recommendation Rating", "Interview Rating"])
candidates = np.array(["Alfred", "Beverly", "Calvin", "Diane", "Edward", "Fran"])
raw_data = np.array([
    [690, 3.1,  9,  7,  4],
    [590, 3.9,  7,  6, 10],
    [600, 3.6,  8,  8,  7],
    [620, 3.8,  7, 10,  6],
    [700, 2.8, 10,  4,  6],
    [650, 4.0,  6,  9,  8],
])

weights = np.array([0.3, 0.2, 0.2, 0.15, 0.15])

# The indices of the attributes (zero-based) that are considered beneficial.
# Those indices not mentioned are assumed to be cost attributes.
benefit_attributes = set([0, 1, 2, 3, 4])

# Display the raw data we have
pd.DataFrame(data=raw_data, index=candidates, columns=attributes)


#############################################################
#                 Normalizing the ratings                   #
#############################################################

m = len(raw_data)
n = len(attributes)
divisors = np.empty(n)
for j in range(n):
    column = raw_data[:,j]
    divisors[j] = np.sqrt(column @ column)

raw_data /= divisors

columns = ["$X_{%d}$" % j for j in range(n)]
pd.DataFrame(data=raw_data, index=candidates, columns=columns)# The given data encoded into vectors and matrices

attributes = np.array(["GRE", "GPA", "College ranking", "Recommendation Rating", "Interview Rating"])
candidates = np.array(["Alfred", "Beverly", "Calvin", "Diane", "Edward", "Fran"])
raw_data = np.array([
    [690, 3.1,  9,  7,  4],
    [590, 3.9,  7,  6, 10],
    [600, 3.6,  8,  8,  7],
    [620, 3.8,  7, 10,  6],
    [700, 2.8, 10,  4,  6],
    [650, 4.0,  6,  9,  8],
])

weights = np.array([0.3, 0.2, 0.2, 0.15, 0.15])

# The indices of the attributes (zero-based) that are considered beneficial.
# Those indices not mentioned are assumed to be cost attributes.
benefit_attributes = set([0, 1, 2, 3, 4])

# Display the raw data we have
pd.DataFrame(data=raw_data, index=candidates, columns=attributes)