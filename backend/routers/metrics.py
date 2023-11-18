from fastapi import Query, HTTPException, APIRouter
from redis_store import store
import random
import json
'''
Earnings overview
Earnings Breadkown by Load
Mileage Log
Fuel Efficiency
Load Acceptance Rate
Deadhead Analysis
Average Trip Duration
Idle Time
Load Rejection Analysis
Destination Preferences
Incident reports
Notification Response Time
Feedback

TRUCK
{
  "seq": 2,
  "type": "Truck",
  "timestamp": "2023-11-17T09:10:23.2531001-05:00",
  "truckId": 346,
  "positionLatitude": 39.195726,
  "positionLongitude": -84.665296,
  "equipType": "Van",
  "nextTripLengthPreference": "Long"
}

LOAD
{
  "seq": 3,
  "type": "Load",
  "timestamp": "2023-11-17T11:31:35.0481646-05:00",
  "loadId": 101,
  "originLatitude": 39.531354,
  "originLongitude": -87.440632,
  "destinationLatitude": 37.639,
  "destinationLongitude": -121.0052,
  "equipmentType": "Van",
  "price": 3150.0,
  "mileage": 2166.0
}
'''
router = APIRouter()
@router.get("/metrics/{truck_id}", tags=["metrics"])
async def get_metrics(truck_id: str):
    # Randomly generate values for the specified metrics
    print("Getting metrics for truck " + str(truck_id))
    metrics_data = store.get_data("truck_metrics_" + str(truck_id))
    # metrics_Data should be a dict
    
    if(metrics_data is None):
        raise HTTPException(status_code=404, detail="Truck not found")
    metrics_data = json.loads(metrics_data)
    if("earnings" not in metrics_data):
        metrics_data["earnings"] = random.randint(0, 4000)
        store.set_data("truck_metrics_" + str(truck_id), json.dumps(metrics_data))
    if("mileage" not in metrics_data):
        metrics_data["mileage"] = metrics_data["earnings"] * random.randint(50, 88) / 100
        store.set_data("truck_metrics_" + str(truck_id), json.dumps(metrics_data))
    if("last_month_earnings" not in metrics_data):
        metrics_data["last_month_earnings"] = random.randint(0, 4000)
        store.set_data("truck_metrics_" + str(truck_id), json.dumps(metrics_data))
    if("last_month_mileage" not in metrics_data):
        metrics_data["last_month_mileage"] = metrics_data["last_month_earnings"] * random.randint(50, 88) / 100
        store.set_data("truck_metrics_" + str(truck_id), json.dumps(metrics_data))
    if("load_acceptance_rate" not in metrics_data):
        metrics_data["load_acceptance_rate"] = random.randint(0, 100)
        store.set_data("truck_metrics_" + str(truck_id), json.dumps(metrics_data))
    if("last_month_load_acceptance_rate" not in metrics_data):
        metrics_data["last_month_load_acceptance_rate"] = random.randint(0, 100)
        store.set_data("truck_metrics_" + str(truck_id), json.dumps(metrics_data))
    return metrics_data
