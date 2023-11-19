from datetime import datetime
import math
from sklearn.cluster import DBSCAN
import numpy as np
latestTimestamp = ""
#############################
#    ML CLUSTERING MODEL    #
#############################
def cluster_loads(load_list):
    # Extracting load locations
    coordinates = np.array([(load['originLatitude'], load['originLongitude']) for load in load_list])
    
    # Apply DBSCAN algorithm
    clustering = DBSCAN(eps=0.1, min_samples=2).fit(coordinates)  # Tune eps and min_samples as needed

    return coordinates, clustering.labels_

def nearest_cluster_distance(truck, cluster_coords, cluster_labels):
    truck_coords = np.array([truck['positionLatitude'], truck['positionLongitude']])
    unique_labels = set(cluster_labels)
    
    min_distance = float('inf')
    for label in unique_labels:
        if label != -1:  # Ignoring noise points
            # Average coordinates of the cluster
            cluster_center = np.mean(cluster_coords[cluster_labels == label], axis=0)
            distance = bird_fly_distance(truck_coords[0], truck_coords[1], cluster_center[0], cluster_center[1])
            min_distance = min(min_distance, distance)
    
    return min_distance

def cluster_proximity_score(truck, load, load_list):
    cluster_coords, cluster_labels = cluster_loads(load_list)
    
    # Truck's distance to the nearest cluster
    truck_distance = nearest_cluster_distance(truck, cluster_coords, cluster_labels)

    # Load's destination distance to the nearest cluster
    load_destination_coords = np.array([load['destinationLatitude'], load['destinationLongitude']])
    load_destination_distance = nearest_cluster_distance({'positionLatitude': load_destination_coords[0], 'positionLongitude': load_destination_coords[1]}, cluster_coords, cluster_labels)

    # Define a threshold for isolation
    isolation_threshold = 100 * 1609.34  # This is in miles, adjust as needed

    # Check if the truck is isolated
    is_isolated = truck_distance > isolation_threshold

    # Scoring logic
    if is_isolated:
        # High score for isolated trucks if the load's destination is near a cluster
        score = 1 / (1 + np.log1p(load_destination_distance))
    else:
        # Lower score for non-isolated trucks, or if load's destination is far from clusters
        score = 1 / (1 + np.log1p(truck_distance + load_destination_distance))

    # Scale the score to a desired range, e.g., between 0 and 1
    scaled_score = min(score, 1) * 10

    return scaled_score

#############################
#         HEURISTIC         #
#############################

def get_score(load, truck, load_list, timestamp, distance):
    data = {}
    global latestTimestamp
    latestTimestamp = timestamp
    load_list = load_list.values()
    weighted_score = 0
    weighted_score += calculate_profit_score(load, truck, data, distance*0.621371) * 0.5
    # Do not evaluate unprofitable loads
    if weighted_score <= 0:
        data["score"] = weighted_score
        return data
    # Check for cluster proximity if there is more than 5 available loads
    if (len(load_list) >= 5):
        weighted_score += trip_length_preference_score(load, truck) * 0.2
        weighted_score += idle_time_score(load, truck) * 0.2
        before = weighted_score
        weighted_score += cluster_proximity_score(truck, load, load_list) * 0.1
        #print("prox: " , weighted_score - before)
    else:
        weighted_score += trip_length_preference_score(load, truck) * 0.3
        weighted_score += idle_time_score(load, truck) * 0.2
    
    data["score"] = weighted_score
    return data


def calculate_profit_score(load, truck, data, distance_in_miles):
    """Calculates a score based on estimated profit."""
    # Profit calculation
    profit = load['price'] - (load['mileage'] * 1.38) - (distance_in_miles*1.38)
    data["profit"] = profit
    return profit / 1000  # Scale down the profit for scoring

def trip_length_preference_score(load, truck):
    """Scores based on trip length preference."""
    preference = 1 if truck['nextTripLengthPreference'] == 'Long' else 0
    load_trip_length = 1 if load['mileage'] >= 200 else 0
    return (5 if preference == load_trip_length else 0)

def idle_time_score(load, truck):
    """Scores based on the difference in timestamp (idle time)."""
    global latestTimestamp
    truck_timestamp = datetime.fromisoformat(truck['latestNotification'])
    currTime = datetime.fromisoformat(latestTimestamp)
    # Calculate the absolute time difference in hours
    time_difference = abs((currTime - truck_timestamp).total_seconds() / 3600)

    # Assuming a maximum idle time threshold (e.g., 48 hours)
    max_idle_threshold = 48
    # Trucks with longer idle times get higher scores
    return min(time_difference, max_idle_threshold) / max_idle_threshold * 5

def bird_fly_distance(truck_lat, truck_long, load_lat, load_long):
    # Radius of the Earth in meters
    R = 6371000 

    # Convert degrees to radians
    truck_lat, truck_long, load_lat, load_long = map(math.radians, [truck_lat, truck_long, load_lat, load_long])

    # Differences
    diff_lat = load_lat - truck_lat
    diff_long = load_long - truck_long

    # Haversine formula
    a = math.sin(diff_lat/2) ** 2 + math.cos(truck_lat) * math.cos(load_lat) * math.sin(diff_long/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Distance in meters
    distance = R * c

    return distance
