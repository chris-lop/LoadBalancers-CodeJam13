from datetime import datetime
import math

def get_score(load, truck):
    """Calculates a simple heuristic score for given truck."""
    score = 0
    score += calculate_profit_score(load, truck)
    if score <= 0:
        return 0
    score += trip_length_preference_score(load, truck)
    score += idle_time_score(load, truck)
    return score

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
    # Convert string timestamps to datetime objects
    truck_timestamp = datetime.fromisoformat(truck['timestamp'])
    load_timestamp = datetime.fromisoformat(load['timestamp'])

    # Calculate the absolute time difference in hours
    time_difference = abs((truck_timestamp - load_timestamp).total_seconds() / 3600)

    # Assuming a maximum idle time threshold (e.g., 48 hours)
    max_idle_threshold = 48
    # Trucks with shorter idle times get higher scores
    return max(0, max_idle_threshold - time_difference) / max_idle_threshold * 5

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
    'price': 1000.0,
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
    {'seq': 1784, 'type': 'Truck', 'timestamp': '2023-11-18T17:55:21', 'truckId': 224, 'positionLatitude': 38.80051040649414, 'positionLongitude': -77.1159896850586, 'equipType': 'Flatbed', 'nextTripLengthPreference': 'Long'}
]

# Example of using the Heuristic class
for truck in truck_list: 
    truck_score = get_score(load, truck)

    print("Truck score:", truck_score)
    print()
