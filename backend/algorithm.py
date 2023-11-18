import numpy as np               # for linear algebra
import pandas as pd              # for tabular output
from scipy.stats import rankdata # for ranking the candidates

class RankingSystem:
    """
    RankingSystem class is used to rank the trucks of a load based on various attributes 
    like profit, trip length preference, and idle time.
    """

    def __init__(self, load, truck_data):
        """
        Initializes the RankingSystem with load and truck data.
        """
        #------------------------#
        # Attribute Declarations #
        #------------------------#
        self.load = load
        self.truck_data = truck_data
        self.attributes = np.array(["Profit", "nextTripLengthPreference", "idleTime"])
        self.weights = np.array([0.5, 0.2, 0.3])
        self.benefit_attributes = set([0, 1])  # 'Profit' and 'nextTripLengthPreference' are benefit attributes ('idleTime' is a cost attribute)
        self.candidates = np.array([truck['truckId'] for truck in truck_data])
        self.raw_data = self.initialize_raw_data()
        self.normalized_data = self.normalize_ratings()
        self.weighted_normalized_data = self.calculate_weighted_normalized_ratings()
        self.a_pos, self.a_neg = self.identify_pis_nis()
        self.separation_measures = self.calculate_separation_measures()

    #------------------------#
    # Method Implementations #
    #------------------------#
    def initialize_raw_data(self):
        """Initializes raw data from truck data."""
        load_trip_length = self.get_load_trip_length(self.load)
        trucker_preferences = {
            trucker['truckId']: 1 if trucker['nextTripLengthPreference'] == 'Long' else 0
            for trucker in self.truck_data
        }
        raw_data = np.array([truck['attributes'] for truck in self.truck_data])  # Replace 'attributes' with actual data structure key
        for i in range(len(self.candidates)):
            trucker_id = self.candidates[i]
            preference_match = 1 if trucker_preferences[trucker_id] == load_trip_length else 0
            raw_data[i][1] = preference_match
        return raw_data

    def normalize_ratings(self):
        """Normalizes ratings for each attribute."""
        divisors = np.linalg.norm(self.raw_data, axis=0)
        return self.raw_data / divisors

    def calculate_weighted_normalized_ratings(self):
        """Initializes raw data from truck data."""
        return self.normalized_data * self.weights

    def identify_pis_nis(self):
        """Normalizes ratings for each attribute."""
        a_pos = np.max(self.weighted_normalized_data, axis=0)
        a_neg = np.min(self.weighted_normalized_data, axis=0)
        for j in range(len(self.attributes)):
            if j not in self.benefit_attributes:
                a_pos[j], a_neg[j] = a_neg[j], a_pos[j]
        return a_pos, a_neg

    def calculate_separation_measures(self):
        """Normalizes ratings for each attribute."""
        m = len(self.weighted_normalized_data)
        sp = np.zeros(m)
        sn = np.zeros(m)
        cs = np.zeros(m)
        for i in range(m):
            diff_pos = self.weighted_normalized_data[i] - self.a_pos
            diff_neg = self.weighted_normalized_data[i] - self.a_neg
            sp[i] = np.linalg.norm(diff_pos)
            sn[i] = np.linalg.norm(diff_neg)
            cs[i] = sn[i] / (sp[i] + sn[i])
        return sp, sn, cs
    
    def get_load_trip_length(self, load):
        return 1 if load['mileage'] >= 200 else 0
    
    def get_rankings(self):
        """Calculate rankings based on C*, S*, and S-"""
        cs_order = self.rank_according_to(self.separation_measures[2])  # Assuming the third element is C*
        return cs_order
    
    def rank_according_to(self, data):
        ranks = rankdata(data).astype(int)
        ranks -= 1
        return self.candidates[ranks][::-1]
    
    def print_results(self):
        cs_order = self.get_rankings()
        if cs_order.size > 0:
            print("The best candidate/alternative according to C* is " + str(cs_order[0]))
            print("The preferences in descending order are " + ", ".join(map(str, cs_order)) + ".")
        else:
            print("No candidates available for ranking.")



#############################
#         TESTING           #
#############################

# Load and truck data from algorithm.py
load = {
    'seq': 51,
    'type': 'Load',
    'timestamp': '2023-11-17T08:55:55', 
    'loadId': 40022,
    'originLatitude': 29.9561,
    'originLongitude': -90.0773, 
    'destinationLatitude': 33.6821,
    'destinationLongitude': -84.1488, 
    'equipmentType': 'Flatbed',
    'price': 1000.0,
    'mileage': 480.0
}

truck_data = [
    {'seq': 52, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 189, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long', 'attributes': [690, 1, 1]},
    {'seq': 53, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 201, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short', 'attributes': [590, 0, 0.25]},
    {'seq': 54, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 301, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long', 'attributes': [600, 1, 0.5]},
    {'seq': 55, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 401, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short', 'attributes': [620, 0, 2]},
    {'seq': 56, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 501, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long', 'attributes': [700, 1, 0.75]}
]

# Create an instance of RankingSystem
ranking_system = RankingSystem(load, truck_data)

# Print the results
ranking_system.print_results()
