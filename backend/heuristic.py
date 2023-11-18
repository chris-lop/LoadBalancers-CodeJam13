from datetime import datetime
import math
from sklearn.cluster import DBSCAN
import numpy as np

#############################
#    ML CLUSTERING MODEL    #
#############################
def cluster_loads(load_list):
    # Extracting load locations
    coordinates = np.array([(load['originLatitude'], load['originLongitude']) for load in load_list])
    
    # Apply DBSCAN algorithm
    clustering = DBSCAN(eps=0.1, min_samples=2).fit(coordinates)  # Tune eps and min_samples as needed
    return coordinates, clustering.labels_

def calculate_distance(lat1, lon1, lat2, lon2):
    # Use the existing bird_fly_distance function
    return bird_fly_distance(lat1, lon1, lat2, lon2)

def nearest_cluster_distance(truck, cluster_coords, cluster_labels):
    truck_coords = np.array([truck['positionLatitude'], truck['positionLongitude']])
    unique_labels = set(cluster_labels)
    
    min_distance = float('inf')
    for label in unique_labels:
        if label != -1:  # Ignoring noise points
            # Average coordinates of the cluster
            cluster_center = np.mean(cluster_coords[cluster_labels == label], axis=0)
            distance = calculate_distance(truck_coords[0], truck_coords[1], cluster_center[0], cluster_center[1])
            min_distance = min(min_distance, distance)
    
    return min_distance

def cluster_proximity_score(truck, load, load_list):
    cluster_coords, cluster_labels = cluster_loads(load_list)
    
    # Identify if the truck is isolated
    truck_distance = nearest_cluster_distance(truck, cluster_coords, cluster_labels)
    is_isolated = truck_distance > 100 # TODO: Define a threshold distance for isolation

    if is_isolated:
        # Calculate the distance from the load's destination to the nearest cluster
        load_destination_coords = np.array([load['destinationLatitude'], load['destinationLongitude']])
        min_distance_to_cluster = float('inf')
        for label in set(cluster_labels):
            if label != -1:  # Ignoring noise points
                cluster_center = np.mean(cluster_coords[cluster_labels == label], axis=0)
                distance = calculate_distance(load_destination_coords[0], load_destination_coords[1], cluster_center[0], cluster_center[1])
                min_distance_to_cluster = min(min_distance_to_cluster, distance)

        # Score based on proximity to the nearest cluster
        return 1 / (1 + min_distance_to_cluster) if min_distance_to_cluster != 0 else 0
    else:
        # For non-isolated trucks, you might return a default score or apply different logic
        return 0

#############################
#         HEURISTIC         #
#############################

def get_score(load, truck, load_list):
    weighted_score = 0
    weighted_score += calculate_profit_score(load, truck) * 0.5
    # Do not evaluate unprofitable loads
    if weighted_score <= 0:
        return 0
    # Check for cluster proximity if there is more than 5 available loads
    if (len(load_list) >= 5):
        weighted_score += trip_length_preference_score(load, truck) * 0.2
        weighted_score += idle_time_score(load, truck) * 0.2
        weighted_score += cluster_proximity_score(truck, load, load_list) * 0.1
    else:
        weighted_score += trip_length_preference_score(load, truck) * 0.3
        weighted_score += idle_time_score(load, truck) * 0.2
    return weighted_score


def calculate_profit_score(load, truck):
    """Calculates a score based on estimated profit."""
    # Profit calculation
    distance_in_miles = ((bird_fly_distance(truck['positionLatitude'], truck['positionLongitude'], load['originLatitude'], load['originLongitude'])) * 0.000621371)
    profit = load['price'] - (load['mileage'] * 1.38) - (distance_in_miles*1.38)
    return profit / 1000  # Scale down the profit for scoring

def trip_length_preference_score(load, truck):
    """Scores based on trip length preference."""
    preference = 1 if truck['nextTripLengthPreference'] == 'Long' else 0
    load_trip_length = 1 if load['mileage'] >= 200 else 0
    return 5 if preference == load_trip_length else 0

def idle_time_score(load, truck):
    """Scores based on the difference in timestamp (idle time)."""
    truck_timestamp = datetime.fromisoformat(truck['timestamp'])
    load_timestamp = datetime.fromisoformat(load['timestamp'])

    # Calculate the absolute time difference in hours
    time_difference = abs((truck_timestamp - load_timestamp).total_seconds() / 3600)

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


#############################
#         TESTING           #
#############################

# Load List
load_list = [{'seq': 1,
  'type': 'Load',
  'timestamp': '2023-11-12T19:38:14',
  'loadId': 55458,
  'originLatitude': 40.28199218111823,
  'originLongitude': -95.90400069387849,
  'destinationLatitude': 43.13466365667815,
  'destinationLongitude': -118.55849918593577,
  'equipmentType': 'Reefer',
  'price': 1472.2565893304964,
  'mileage': 701.5031870803324},
 {'seq': 2,
  'type': 'Load',
  'timestamp': '2023-11-12T19:38:14',
  'loadId': 90573,
  'originLatitude': 46.61776995296577,
  'originLongitude': -111.85547757032664,
  'destinationLatitude': 45.41567027879734,
  'destinationLongitude': -117.4739778537941,
  'equipmentType': 'Reefer',
  'price': 665.2857913268363,
  'mileage': 297.9398173623498},
 {'seq': 3,
  'type': 'Load',
  'timestamp': '2023-11-17T19:38:14',
  'loadId': 83429,
  'originLatitude': 47.982710374773674,
  'originLongitude': -68.97640162863107,
  'destinationLatitude': 27.582666638347135,
  'destinationLongitude': -108.7377244174949,
  'equipmentType': 'Van',
  'price': 1588.694992267503,
  'mileage': 791.3681118857668},
 {'seq': 4,
  'type': 'Load',
  'timestamp': '2023-11-14T19:38:14',
  'loadId': 48678,
  'originLatitude': 45.21217636820585,
  'originLongitude': -85.74060245380439,
  'destinationLatitude': 35.077818916609075,
  'destinationLongitude': -97.23975729705347,
  'equipmentType': 'Flatbed',
  'price': 775.2265808599146,
  'mileage': 338.6972589935872},
 {'seq': 5,
  'type': 'Load',
  'timestamp': '2023-11-11T19:38:14',
  'loadId': 12162,
  'originLatitude': 35.80899170634069,
  'originLongitude': -85.93624710079492,
  'destinationLatitude': 28.942580798301364,
  'destinationLongitude': -97.37721408142397,
  'equipmentType': 'Reefer',
  'price': 1375.8630836219036,
  'mileage': 968.4686414313076},
 {'seq': 6,
  'type': 'Load',
  'timestamp': '2023-11-17T19:38:14',
  'loadId': 57859,
  'originLatitude': 45.712350974402156,
  'originLongitude': -69.73337160011117,
  'destinationLatitude': 27.39317410775027,
  'destinationLongitude': -97.55891348332342,
  'equipmentType': 'Van',
  'price': 657.0878449744716,
  'mileage': 903.6653126497756},
 {'seq': 7,
  'type': 'Load',
  'timestamp': '2023-11-13T19:38:14',
  'loadId': 92214,
  'originLatitude': 37.76798083794764,
  'originLongitude': -75.91095763521335,
  'destinationLatitude': 31.71510522267922,
  'destinationLongitude': -102.49246274063321,
  'equipmentType': 'Flatbed',
  'price': 931.1582170942684,
  'mileage': 567.0596384902494},
 {'seq': 8,
  'type': 'Load',
  'timestamp': '2023-11-18T19:38:14',
  'loadId': 30432,
  'originLatitude': 37.521313467201175,
  'originLongitude': -82.47658773042832,
  'destinationLatitude': 35.72817895587551,
  'destinationLongitude': -114.7911853649849,
  'equipmentType': 'Reefer',
  'price': 1938.268184162395,
  'mileage': 627.9953568052881},
 {'seq': 9,
  'type': 'Load',
  'timestamp': '2023-11-15T19:38:14',
  'loadId': 37037,
  'originLatitude': 39.78280441644173,
  'originLongitude': -93.5975133620058,
  'destinationLatitude': 32.11587258233195,
  'destinationLongitude': -104.00176978502938,
  'equipmentType': 'Flatbed',
  'price': 1709.973688157892,
  'mileage': 927.2187684021148},
 {'seq': 10,
  'type': 'Load',
  'timestamp': '2023-11-12T19:38:14',
  'loadId': 80262,
  'originLatitude': 31.930042707887964,
  'originLongitude': -103.06751691766391,
  'destinationLatitude': 44.65703730725631,
  'destinationLongitude': -92.32315834676523,
  'equipmentType': 'Reefer',
  'price': 1492.7326825367413,
  'mileage': 586.2515123184021}]

# Load and truck data from algorithm.py
load = {
    'seq': 51,
    'type': 'Load',
    'timestamp': '2023-11-18T17:46:00', 
    'loadId': 40022,
    'originLatitude': 29.9561,
    'originLongitude': -90.0773, 
    'destinationLatitude': 33.6821,
    'destinationLongitude': -84.1488, 
    'equipmentType': 'Flatbed',
    'price': 10000.0,
    'mileage': 480.0
}

truck_list = [
    {'seq': 1758, 'type': 'Truck', 'timestamp': '2023-11-18T17:46:07', 'truckId': 160, 'positionLatitude': 41.19511413574219, 'positionLongitude': -79.43486785888672, 'equipType': 'Van', 'nextTripLengthPreference': 'Long'},
    {'seq': 1759, 'type': 'Truck', 'timestamp': '2023-11-18T17:46:17', 'truckId': 427, 'positionLatitude': 33.104087829589844, 'positionLongitude': -83.81094360351562, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Long'},
    {'seq': 1760, 'type': 'Truck', 'timestamp': '2023-11-18T17:46:22', 'truckId': 215, 'positionLatitude': 35.41987609863281, 'positionLongitude': -86.014892578125, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short'},
    {'seq': 1761, 'type': 'Truck', 'timestamp': '2023-11-18T17:46:38', 'truckId': 103, 'positionLatitude': 40.08848190307617, 'positionLongitude': -77.41670227050781, 'equipType': 'Van', 'nextTripLengthPreference': 'Short'},
    {'seq': 1762, 'type': 'Truck', 'timestamp': '2023-11-18T17:46:47', 'truckId': 276, 'positionLatitude': 42.1627311706543, 'positionLongitude': -83.242919921875, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'},
    {'seq': 1763, 'type': 'Truck', 'timestamp': '2023-11-18T17:47:08', 'truckId': 119, 'positionLatitude': 34.66741943359375, 'positionLongitude': -78.7313003540039, 'equipType': 'Van', 'nextTripLengthPreference': 'Long'},
    {'seq': 1764, 'type': 'Truck', 'timestamp': '2023-11-18T17:47:19', 'truckId': 290, 'positionLatitude': 36.65528106689453, 'positionLongitude': -78.1341323852539, 'equipType': 'Van', 'nextTripLengthPreference': 'Short'},
    {'seq': 1765, 'type': 'Truck', 'timestamp': '2023-11-18T17:47:41', 'truckId': 266, 'positionLatitude': 40.76347351074219, 'positionLongitude': -81.59420013427734, 'equipType': 'Van', 'nextTripLengthPreference': 'Long'},
    {'seq': 1766, 'type': 'Truck', 'timestamp': '2023-11-18T17:47:42', 'truckId': 403, 'positionLatitude': 36.32249450683594, 'positionLongitude': -86.70453643798828, 'equipType': 'Van', 'nextTripLengthPreference': 'Long'},
    {'seq': 1767, 'type': 'Truck', 'timestamp': '2023-11-18T17:47:54', 'truckId': 161, 'positionLatitude': 33.903926849365234, 'positionLongitude': -83.57975769042969, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short'},
    {'seq': 1768, 'type': 'Truck', 'timestamp': '2023-11-18T17:48:47', 'truckId': 390, 'positionLatitude': 39.60343933105469, 'positionLongitude': -84.23631286621094, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'},
    {'seq': 1769, 'type': 'Truck', 'timestamp': '2023-11-18T17:48:50', 'truckId': 397, 'positionLatitude': 43.37735748291016, 'positionLongitude': -74.91069030761719, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Short'},
    {'seq': 1770, 'type': 'Truck', 'timestamp': '2023-11-18T17:48:53', 'truckId': 323, 'positionLatitude': 36.549991607666016, 'positionLongitude': -85.50529479980469, 'equipType': 'Van', 'nextTripLengthPreference': 'Long'},
    {'seq': 1771, 'type': 'Truck', 'timestamp': '2023-11-18T17:49:56', 'truckId': 181, 'positionLatitude': 40.64623260498047, 'positionLongitude': -74.59065246582031, 'equipType': 'Van', 'nextTripLengthPreference': 'Short'},
    {'seq': 1772, 'type': 'Truck', 'timestamp': '2023-11-18T17:49:59', 'truckId': 199, 'positionLatitude': 39.651126861572266, 'positionLongitude': -77.88816833496094, 'equipType': 'Van', 'nextTripLengthPreference': 'Short'},
    {'seq': 1773, 'type': 'Truck', 'timestamp': '2023-11-18T17:50:07', 'truckId': 338, 'positionLatitude': 36.16437530517578, 'positionLongitude': -84.07960510253906, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short'},
    {'seq': 1774, 'type': 'Truck', 'timestamp': '2023-11-18T17:51:03', 'truckId': 342, 'positionLatitude': 40.71038436889648, 'positionLongitude': -74.16265106201172, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Short'},
    {'seq': 1775, 'type': 'Truck', 'timestamp': '2023-11-18T17:52:05', 'truckId': 134, 'positionLatitude': 39.89287185668945, 'positionLongitude': -86.05553436279297, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Short'},
    {'seq': 1776, 'type': 'Truck', 'timestamp': '2023-11-18T17:53:34', 'truckId': 232, 'positionLatitude': 34.792808532714844, 'positionLongitude': -85.00074005126953, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Short'},
    {'seq': 1777, 'type': 'Truck', 'timestamp': '2023-11-18T17:53:49', 'truckId': 234, 'positionLatitude': 43.75012969970703, 'positionLongitude': -79.41373443603516, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Short'},
    {'seq': 1778, 'type': 'Truck', 'timestamp': '2023-11-18T17:54:07', 'truckId': 418, 'positionLatitude': 35.47133255004883, 'positionLongitude': -78.37611389160156, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Long'},
    {'seq': 1779, 'type': 'Truck', 'timestamp': '2023-11-18T17:54:13', 'truckId': 236, 'positionLatitude': 35.253353118896484, 'positionLongitude': -82.29132843017578, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'},
    {'seq': 1780, 'type': 'Truck', 'timestamp': '2023-11-18T17:54:15', 'truckId': 129, 'positionLatitude': 32.41004943847656, 'positionLongitude': -83.31920623779297, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Short'},
    {'seq': 1781, 'type': 'Truck', 'timestamp': '2023-11-18T17:54:28', 'truckId': 316, 'positionLatitude': 34.964813232421875, 'positionLongitude': -82.02007293701172, 'equipType': 'Reefer', 'nextTripLengthPreference': 'Long'},
    {'seq': 1782, 'type': 'Truck', 'timestamp': '2023-11-18T17:55:08', 'truckId': 159, 'positionLatitude': 34.650386810302734, 'positionLongitude': -82.57096099853516, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Long'},
    {'seq': 1783, 'type': 'Truck', 'timestamp': '2023-11-18T17:55:09', 'truckId': 137, 'positionLatitude': 40.59501647949219, 'positionLongitude': -74.23518371582031, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Long'},
    {'seq': 1784, 'type': 'Truck', 'timestamp': '2023-11-18T17:55:21', 'truckId': 224, 'positionLatitude': 38.80051040649414, 'positionLongitude': -77.1159896850586, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Long'},
    {'seq': 1785,
  'type': 'Truck',
  'timestamp': '2023-11-16T19:40:39',
  'truckId': 101,
  'positionLatitude': 36.71487399695834,
  'positionLongitude': -70.61676965693785,
  'equipType': 'Van',
  'nextTripLengthPreference': 'Short'},
 {'seq': 1786,
  'type': 'Truck',
  'timestamp': '2023-11-12T19:40:39',
  'truckId': 712,
  'positionLatitude': 46.83239792321747,
  'positionLongitude': -102.81895671996212,
  'equipType': 'Reefer',
  'nextTripLengthPreference': 'Short'},
 {'seq': 1787,
  'type': 'Truck',
  'timestamp': '2023-11-14T19:40:39',
  'truckId': 700,
  'positionLatitude': 45.52220627176716,
  'positionLongitude': -69.01145719109684,
  'equipType': 'Van',
  'nextTripLengthPreference': 'Short'},
 {'seq': 1788,
  'type': 'Truck',
  'timestamp': '2023-11-12T19:40:39',
  'truckId': 301,
  'positionLatitude': 33.557333964642744,
  'positionLongitude': -93.10685254244379,
  'equipType': 'Van',
  'nextTripLengthPreference': 'Short'},
 {'seq': 1789,
  'type': 'Truck',
  'timestamp': '2023-11-15T19:40:39',
  'truckId': 180,
  'positionLatitude': 47.329443511373945,
  'positionLongitude': -121.21449720511305,
  'equipType': 'Flatbed',
  'nextTripLengthPreference': 'Long'},
 {'seq': 1790,
  'type': 'Truck',
  'timestamp': '2023-11-14T19:40:39',
  'truckId': 382,
  'positionLatitude': 43.79101471279656,
  'positionLongitude': -122.74979036618632,
  'equipType': 'Flatbed',
  'nextTripLengthPreference': 'Long'},
 {'seq': 1791,
  'type': 'Truck',
  'timestamp': '2023-11-14T19:40:39',
  'truckId': 481,
  'positionLatitude': 40.280873019859506,
  'positionLongitude': -113.54621401804717,
  'equipType': 'Van',
  'nextTripLengthPreference': 'Short'},
 {'seq': 1792,
  'type': 'Truck',
  'timestamp': '2023-11-16T19:40:39',
  'truckId': 476,
  'positionLatitude': 28.61815728114387,
  'positionLongitude': -108.79176371464996,
  'equipType': 'Van',
  'nextTripLengthPreference': 'Short'},
 {'seq': 1793,
  'type': 'Truck',
  'timestamp': '2023-11-13T19:40:39',
  'truckId': 327,
  'positionLatitude': 30.866853732219518,
  'positionLongitude': -113.85820372981439,
  'equipType': 'Van',
  'nextTripLengthPreference': 'Long'},
 {'seq': 1794,
  'type': 'Truck',
  'timestamp': '2023-11-17T19:40:39',
  'truckId': 554,
  'positionLatitude': 25.324918038542016,
  'positionLongitude': -76.91946338120916,
  'equipType': 'Van',
  'nextTripLengthPreference': 'Short'}
]

# Example of using the Heuristic class
for truck in truck_list: 
    truck_score = get_score(load, truck, load_list)

    print("Truck score:", truck_score)
    print()
