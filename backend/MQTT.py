import os
import paho.mqtt.client as mqtt
import json
import requests
from dotenv import load_dotenv
import math
import time 
import heapq
from heuristic import Heuristic
import concurrent.futures

load_dotenv() 
trucks = {}
loads = {}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("CodeJam")

def on_message(client, userdata, msg):
#     # send truck events to truck function
    payload = json.loads(msg.payload.decode())
    if(payload["type"] == "Truck"):
        init_truck(payload)
    elif(payload["type"] == "Load"):
        init_load(payload)
        load_id = payload["loadId"]
        for truck in loads[load_id]["potentialTrucks"]:
            h_instance = Heuristic(loads[load_id], truck)
            print(h_instance.get_score())      
    else:
        print("Unknown type: " + payload["type"])

def init_truck(payload):
    truck_id = payload["truckId"]
    if(truck_id not in trucks):
        #{'seq': 2140, 'type': 'Truck', 'timestamp': '2023-11-17T20:03:18', 'truckId': 104, 'positionLatitude': 40.84517288208008, 'positionLongitude': -73.91064453125, 'equipType': 'Van', 'nextTripLengthPreference': 'Long'}
        trucks[truck_id] = {"seq": payload["seq"], "timestamp": payload["timestamp"], "positionLatitude": payload["positionLatitude"], "positionLongitude": payload["positionLongitude"], "equipType": payload["equipType"], "nextTripLengthPreference": payload["nextTripLengthPreference"]}

def init_load(payload):
    print("new load")
    load_id = payload["loadId"]
    # {'seq': 51, 'type': 'Load', 'timestamp': '2023-11-17T08:55:55', 'loadId': 40022, 'originLatitude': 29.9561, 'originLongitude': -90.0773, 'destinationLatitude': 33.6821, 'destinationLongitude': -84.1488, 'equipmentType': 'Flatbed', 'price': 1000.0, 'mileage': 480.0}
    if(load_id not in loads):
        loads[load_id] = {"seq": payload["seq"], "timestamp": payload["timestamp"], "originLatitude": payload["originLatitude"], "originLongitude": payload["originLongitude"], "destinationLatitude": payload["destinationLatitude"], "destinationLongitude": payload["destinationLongitude"], "equipmentType": payload["equipmentType"], "price": payload["price"], "mileage": payload["mileage"], "potentialTrucks":[]}
    dists = []
    for truck_id, truck in trucks.items():
        #Only push in heap compatible trucks (size) -> don't bother calculating the rest
        if truck['equipType'] != payload['equipmentType']:
            continue
        distance = bird_fly_distance(truck['positionLatitude'], truck["positionLongitude"], payload['originLatitude'], payload["originLongitude"])
        heapq.heappush(dists, (distance, truck_id))    
    # get 50 closest trucks
    for i in range(50):
        if len(dists) == 0 or len(loads[load_id]["potentialTrucks"]) >= 50:
            break
        truck_id = heapq.heappop(dists)[1]
        loads[load_id]["potentialTrucks"].append(trucks[truck_id])
    # get real distance between truck and load
    start_time = time.time()
    print("start init_load with " + str(len(loads[load_id]["potentialTrucks"])) + " trucks")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_list = []
        for truck in loads[load_id]["potentialTrucks"]:
            future = executor.submit(
                        calculate_distance,
                        truck['positionLatitude'],
                        truck["positionLongitude"],
                        payload['originLatitude'],
                        payload["originLongitude"]
                    )
            future_list.append(future)

    # Wait for all threads to finish
    concurrent.futures.wait(future_list)
    # Get the results
    for i, truck in enumerate(loads[load_id]["potentialTrucks"]):
        truck['distance'] = future_list[i].result()
    # print distance
    for truck in loads[load_id]["potentialTrucks"]:
        print(truck['distance'], "meters")

    end_time = time.time()  # end timer

    elapsed_time = end_time - start_time
    
    print("end init_load in " + str(elapsed_time) + " seconds")

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

def calculate_distance(truck_lat, truck_long, load_lat, load_long):
    api_key = os.getenv('GOOGLE_API_KEY')
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={truck_lat},{truck_long}&destinations={load_lat},{load_long}&key={api_key}'
    
    response = requests.get(url)
    data = json.loads(response.text)
    #print(data)
    if 'rows' in data and 'elements' in data['rows'][0] and 'distance' in data['rows'][0]['elements'][0]:
        return data['rows'][0]['elements'][0]['distance']['value']
    else:
        raise Exception("Error in calculating distance")

client = mqtt.Client(client_id="LoadBalancers01")
client.username_pw_set("CodeJamUser", "123CodeJam")
client.on_connect = on_connect
client.on_message = on_message
client.connect("fortuitous-welder.cloudmqtt.com", 1883, 60)
client.loop_forever()
# Run the loop for 12.5 seconds (1 hour simulation time)
#timeout = 12.5
#start_time = time.time()

#while time.time() - start_time < timeout:
#    client.loop()

# Clean up and disconnect
client.disconnect()
