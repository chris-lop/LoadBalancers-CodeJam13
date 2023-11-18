# All the packages that we need to import
import numpy as np               # for linear algebra
import pandas as pd              # for tabular output
from scipy.stats import rankdata # for ranking the candidates

#############################################################
#                     Pre-requisites                        #
#############################################################

# Raw Data
load = {'seq': 51, 'type': 'Load', 'timestamp': '2023-11-17T08:55:55', 'loadId': 40022, 'originLatitude': 29.9561, 'originLongitude': -90.0773, 'destinationLatitude': 33.6821, 'destinationLongitude': -84.1488, 'equipmentType': 'Flatbed', 'price': 1000.0, 'mileage': 480.0}

data = [
    {'seq': 52, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37','truckId': 189, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'},
    {'seq': 53, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37','truckId': 201, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short'},
    {'seq': 54, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37','truckId': 301, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'},
    {'seq': 55, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37','truckId': 401, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short'},
    {'seq': 56, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37','truckId': 501, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'}
]

# Determine if the load's trip is short or long
def get_load_trip_length(load):
    return 1 if load['mileage'] >= 200 else 0  # 1 for long, 0 for short

# Load trip length
load_trip_length = get_load_trip_length(load)

trucker_preferences = {
    trucker['truckId']: 1 if trucker['nextTripLengthPreference'] == 'Long' else 0
    for trucker in data
}

# The given data encoded into vectors and matrices
attributes = np.array(["Profit", "nextTripLengthPreference", "idleTime"])
candidates = np.array([189, 201, 301, 401, 501])
raw_data = np.array([
    [690, 1,  1],
    [590, 0,  0.25],
    [600, 1,  0.5],
    [620, 0,  2],
    [700, 1, 0.75],
])

for i in range(len(candidates)):
    trucker_id = candidates[i]
    preference_match = 1 if trucker_preferences[trucker_id] == load_trip_length else 0
    raw_data[i][1] = preference_match

# Adjusting the weights
weights = np.array([0.5, 0.2, 0.3])

# The indices of the attributes (zero-based) that are considered beneficial.
# 'idleTime' is a cost attribute (therefore omited from benefit attributes)
benefit_attributes = set([0, 1])  # 'Profit' and 'nextTripLengthPreference' are benefit attributes

# Display the raw data we have
pd.DataFrame(data=raw_data, index=candidates, columns=attributes)
print(raw_data)
print('\n')


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


# Ensure that there are entries in cs_order before accessing them
if cs_order.size > 0:
    print("The best candidate/alternative according to C* is " + str(cs_order[0]))
    print("The preferences in descending order are " + ", ".join(map(str, cs_order)) + ".")
else:
    print("No candidates available for ranking.")