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
pd.DataFrame(data=raw_data, index=candidates, columns=columns)


#############################################################
#       Calculating the Weighted Normalized Ratings         #
#############################################################
raw_data *= weights
pd.DataFrame(data=raw_data, index=candidates, columns=columns)

#############################################################
#        Identifying PIS ( A*) and NIS ( A-)                #
#############################################################
a_pos = np.zeros(n)
a_neg = np.zeros(n)
for j in range(n):
    column = raw_data[:,j]
    max_val = np.max(column)
    min_val = np.min(column)
    
    # See if we want to maximize benefit or minimize cost (for PIS)
    if j in benefit_attributes:
        a_pos[j] = max_val
        a_neg[j] = min_val
    else:
        a_pos[j] = min_val
        a_neg[j] = max_val

pd.DataFrame(data=[a_pos, a_neg], index=["$A^*$", "$A^-$"], columns=columns)

#############################################################
#  Calculating Separation Measures and Similarities to PIS  #
#############################################################
sp = np.zeros(m)
sn = np.zeros(m)
cs = np.zeros(m)

for i in range(m):
    diff_pos = raw_data[i] - a_pos
    diff_neg = raw_data[i] - a_neg
    sp[i] = np.sqrt(diff_pos @ diff_pos)
    sn[i] = np.sqrt(diff_neg @ diff_neg)
    cs[i] = sn[i] / (sp[i] + sn[i])

pd.DataFrame(data=zip(sp, sn, cs), index=candidates, columns=["$S^*$", "$S^-$", "$C^*$"])


#############################################################
#             Ranking the candidates/alternatives           #
#############################################################
def rank_according_to(data):
    ranks = rankdata(data).astype(int)
    ranks -= 1
    return candidates[ranks][::-1]

cs_order = rank_according_to(cs)
sp_order = rank_according_to(sp)
sn_order = rank_according_to(sn)

pd.DataFrame(data=zip(cs_order, sp_order, sn_order), index=range(1, m + 1), columns=["$C^*$", "$S^*$", "$S^-$"])

#############################################################
#                      Printing Results                     #
#############################################################
print("The best candidate/alternative according to C* is " + cs_order[0])
print("The preferences in descending order are " + ", ".join(cs_order) + ".")