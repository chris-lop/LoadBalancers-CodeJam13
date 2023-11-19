from datetime import datetime
import os
import json
import random
import requests
from dotenv import load_dotenv
import math
import time 
import heapq
from heuristic import get_score
import concurrent.futures
import asyncio
from gmqtt import Client as MQTTClient
import signal 
from redis_store import store

load_dotenv() 
trucks = {}
loads = {}

latestTimestamp = ""

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("CodeJam")

def on_message(client, topic, payload, qos, properties):
    # send truck events to truck function
    payload = json.loads(payload.decode())
    global latestTimestamp 
    latestTimestamp = payload["timestamp"]
    if(payload["type"] == "Truck"):
        init_truck(payload)
        print("Truck " + str(payload["truckId"]) + " updated")
    elif(payload["type"] == "Load"):
        init_load(payload)
    elif(payload["type"] == "End"):
        print("End")
        end_day()
    elif(payload["type"] == "Start"):
        print("Start")

    else:
        print("Unknown type: " + payload["type"])

def end_day():
    loads.clear()
    trucks.clear()
    # clear redis
    store.redis.flushall()

def init_truck(payload):
    truck_id = payload["truckId"]
    if(truck_id not in trucks):
        #{'seq': 2140, 'type': 'Truck', 'timestamp': '2023-11-17T20:03:18', 'truckId': 104, 'positionLatitude': 40.84517288208008, 'positionLongitude': -73.91064453125, 'equipType': 'Van', 'nextTripLengthPreference': 'Long'}
        trucks[truck_id] = {"seq": payload["seq"], "timestamp": payload["timestamp"], "positionLatitude": payload["positionLatitude"], "positionLongitude": payload["positionLongitude"], "equipType": payload["equipType"], "nextTripLengthPreference": payload["nextTripLengthPreference"], "latestNotification": payload["timestamp"], "latestLoads": []}
        store.set_data("truck_metrics_" + str(truck_id), json.dumps({"positionLatitude": payload["positionLatitude"], "positionLongitude": payload["positionLongitude"], "equipType": payload["equipType"], "nextTripLengthPreference": payload["nextTripLengthPreference"], "latestNotification": payload["timestamp"], "latestLoads": []}))

def init_load(payload):
    load_id = payload["loadId"]
    # {'seq': 51, 'type': 'Load', 'timestamp': '2023-11-17T08:55:55', 'loadId': 40022, 'originLatitude': 29.9561, 'originLongitude': -90.0773, 'destinationLatitude': 33.6821, 'destinationLongitude': -84.1488, 'equipmentType': 'Flatbed', 'price': 1000.0, 'mileage': 480.0}
    if(load_id not in loads):
        loads[load_id] = {"seq": payload["seq"], "timestamp": payload["timestamp"], "originLatitude": payload["originLatitude"], "originLongitude": payload["originLongitude"], "destinationLatitude": payload["destinationLatitude"], "destinationLongitude": payload["destinationLongitude"], "equipmentType": payload["equipmentType"], "price": payload["price"], "mileage": payload["mileage"], "potentialTrucks":{}}
    dists = []
    for truck_id, truck in trucks.items():
        #Only push in heap compatible trucks (size) -> don't bother calculating the rest
        if truck['equipType'] != payload['equipmentType']:
            continue
        distance = bird_fly_distance(truck['positionLatitude'], truck["positionLongitude"], payload['originLatitude'], payload["originLongitude"])
        heapq.heappush(dists, (distance, truck_id))    
    # get 50 closest trucks
    for i in range(50):
        if len(dists) == 0 or len(loads[load_id]["potentialTrucks"]) >= 20:
            break
        truck_id = heapq.heappop(dists)[1]
        loads[load_id]["potentialTrucks"][truck_id] = -1
    # get real distance between truck and load
    start_time = time.time()
    #print("start init_load with " + str(len(loads[load_id]["potentialTrucks"])) + " trucks")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_list = []
        for truck_id in loads[load_id]["potentialTrucks"].keys():
            future = executor.submit(
                        calculate_distance,
                        trucks[truck_id]['positionLatitude'],
                        trucks[truck_id]["positionLongitude"],
                        payload['originLatitude'],
                        payload["originLongitude"]
                    )
            future_list.append(future)
    # Wait for all threads to finish
    concurrent.futures.wait(future_list)
    # Get the results
    for i, truck_id in enumerate(loads[load_id]["potentialTrucks"].keys()):
        loads[load_id]["potentialTrucks"][truck_id] = future_list[i].result()
    notify_truck(load_id)
    end_time = time.time()  # end timer
    elapsed_time = end_time - start_time
    #print("end init_load in " + str(elapsed_time) + " seconds for " + str(len(loads[load_id]["potentialTrucks"])) + " trucks")

def notify_truck(load_id):
    scores = {}
    load = loads[load_id]
    truck_ids = load["potentialTrucks"].keys()
    # calculate score for each truck
    for truck_id in truck_ids:
        distance = load["potentialTrucks"][truck_id]
        scores[truck_id] = get_score(load, trucks[truck_id], loads, latestTimestamp, distance)
    # sort trucks by score
    truck_ids = sorted(truck_ids, key=lambda x: scores[x]["score"], reverse=True)
    # notify scores > 0
    added = 0
    for i in truck_ids:
        if added <= 20:
            #print((datetime.strptime(latestTimestamp, '%Y-%m-%dT%H:%M:%S') - datetime.strptime(trucks[i]["latestNotification"], '%Y-%m-%dT%H:%M:%S')).total_seconds())
            if scores[i]["score"] > 0:
                added += 1
                # check if time without notification is less than 1 hour
                if (datetime.strptime(latestTimestamp, '%Y-%m-%dT%H:%M:%S') - datetime.strptime(trucks[i]["latestNotification"], '%Y-%m-%dT%H:%M:%S')).total_seconds() < 1800 and not trucks[i]["timestamp"] == trucks[i]["latestNotification"]:
                    added -= 1
                    #print("Truck ", i, " notified less than 1 hour ago, skipping")
                    continue
                #else:
                    #print("Notifying truck " + str(i) + " with score " + str(scores[i]["score"]))
                #print(trucks[i]["latestNotification"], trucks[i]["timestamp"])
                # add timestamp to scores, 
                scores[i]["timestamp"] = latestTimestamp
                # add loadId to scores
                scores[i]["loadId"] = load_id
                # add origin and destination to scores
                scores[i]["originLatitude"] = load["originLatitude"]
                scores[i]["originLongitude"] = load["originLongitude"]
                scores[i]["destinationLatitude"] = load["destinationLatitude"]
                scores[i]["destinationLongitude"] = load["destinationLongitude"]
                # add distance to scores
                scores[i]["mileage"] = load["mileage"]
                # set to current timestamp
                trucks[i]["latestNotification"] = latestTimestamp
                if len(trucks[i]["latestLoads"]) >= 5:
                    trucks[i]["latestLoads"].pop(4)
                # insert at beginning
                trucks[i]["latestLoads"].insert(0, scores[i])
                store.set_data(i, json.dumps(scores[i]))
                # edit truck metrics
                metrics_data = store.get_data("truck_metrics_" + str(i))
                metrics_data = json.loads(metrics_data)
                metrics_data["latestNotification"] = latestTimestamp
                if len(metrics_data["latestLoads"]) >= 5:
                    metrics_data["latestLoads"].pop(0)
                metrics_data["latestLoads"].insert(0, scores[i])
                store.set_data("truck_metrics_" + str(i), json.dumps(metrics_data))
                #print("Truck " + str(i) + " notified with score " + str(scores[i]))
        else:
            break


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
    # convert to miles
    distance = distance * 0.000621371
    return distance

def calculate_distance(truck_lat, truck_long, load_lat, load_long):
    return bird_fly_distance(truck_lat, truck_long, load_lat, load_long)
    api_key = os.getenv('GOOGLE_API_KEY')
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={truck_lat},{truck_long}&destinations={load_lat},{load_long}&key={api_key}'
    
    response = requests.get(url)
    data = json.loads(response.text)
    if 'rows' in data and 'elements' in data['rows'][0] and 'distance' in data['rows'][0]['elements'][0]:
        return data['rows'][0]['elements'][0]['distance']['value']/1000
    else:
        raise Exception("Error in calculating distance")


STOP = asyncio.Event()

def ask_exit(*args):
    STOP.set()

async def main():
    client = MQTTClient("LoadBalancers01")

    client.on_connect = on_connect
    client.on_message = on_message

    client.set_auth_credentials("CodeJamUser", "123CodeJam")

    await client.connect("fortuitous-welder.cloudmqtt.com", 1883, False, 60)

    while not STOP.is_set():
        await asyncio.sleep(1)

    await client.disconnect()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(main())