import numpy as np               # for linear algebra
import pandas as pd              # for tabular output
from scipy.stats import rankdata # for ranking the candidates
import random  # Import the random module

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
        raw_data = np.zeros((len(self.truck_data), len(self.attributes)))

        for i, truck in enumerate(self.truck_data):
            # Calculate each attribute
            raw_data[i][0] = self.calculate_profit(truck)  # Profit
            raw_data[i][1] = self.trip_length_preference_match(truck)  # TripLengthPreference Match
            raw_data[i][2] = self.calculate_idle_time(truck)  # Idle Time

        return raw_data

    def calculate_profit(self, truck):
        """Calculate the profit for a truck."""
        # TODO: Add deadhead to profit function, for now random
        random_deadhead = (random.randint(1, 100) * 1.38)

        return self.load['price'] - (self.load['mileage'] * 1.38) - (random_deadhead)

    def trip_length_preference_match(self, truck):
        """Check if the truck's trip length preference matches the load's trip length."""
        load_trip_length = self.get_load_trip_length(self.load)
        preference = 1 if truck['nextTripLengthPreference'] == 'Long' else 0
        return 1 if preference == load_trip_length else 0

    def calculate_idle_time(self, truck):
        """Calculate idle time (dummy function for now)."""
        # TODO: Calculate idle time correctly
        return 0.1

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
        # Rank in descending order, highest value gets rank 1
        # 'max' method assigns the highest rank to all tied elements
        ranks = rankdata(-data, method='max').astype(int)
        sorted_indices = np.argsort(-data)  # Sort indices in descending order of data
        return self.candidates[sorted_indices]
    
    def print_results(self):
        cs_order = self.get_rankings()
        cs_scores = self.separation_measures[2]  # Assuming the third element is C*
        
        if cs_order.size > 0:
            print("Rankings and Scores:")
            for i, truck_id in enumerate(cs_order):
                print(f"{i+1}. Truck ID: {truck_id}, Score: {cs_scores[np.where(self.candidates == truck_id)][0]:.3f}")
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
    {'seq': 52, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 189, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'},
    {'seq': 53, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 201, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short'},
    {'seq': 54, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 301, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'},
    {'seq': 55, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 401, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short'},
    {'seq': 56, 'type': 'Truck', 'timestamp': '2023-11-17T08:56:37', 'truckId': 501, 'positionLatitude': 40.37152862548828, 'positionLongitude': -76.68165588378906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'}
]

# Create an instance of RankingSystem
ranking_system = RankingSystem(load, truck_data)

# Print the results
ranking_system.print_results()
