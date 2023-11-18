from fastapi import Query, HTTPException, APIRouter
import random

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

@router.get("/metrics", tags=["metrics"])
async def get_metrics():
    # Randomly generate values for the specified metrics
    metrics_data = {
        'earnings_overview': round(random.uniform(1000, 5000), 2),
        'earnings_breakdown_by_load': {f'load_{i}': round(random.uniform(100, 500), 2) for i in range(1, 6)},
        'mileage_log': round(random.uniform(5000, 20000), 2),
        'fuel_efficiency': round(random.uniform(5, 10), 2),
        'load_acceptance_rate': round(random.uniform(0.5, 1.0), 2),
        'deadhead_analysis': round(random.uniform(100, 500), 2),
        'average_trip_duration': round(random.uniform(5, 15), 2),
        'idle_time': round(random.uniform(1, 5), 2),
        'load_rejection_analysis': {
            'unfavorable_route': round(random.uniform(0, 1), 2),
            'low_payment': round(random.uniform(0, 1), 2),
            'equipment_mismatch': round(random.uniform(0, 1), 2)
        },
        'destination_preferences': {
            'destination_A': round(random.uniform(0, 1), 2),
            'destination_B': round(random.uniform(0, 1), 2),
            'destination_C': round(random.uniform(0, 1), 2),
        },
        'incident_reports': round(random.uniform(0, 1), 2),
        'notification_response_time': round(random.uniform(1, 5), 2),
        'feedback': round(random.uniform(0, 1), 2),
    }

    return metrics_data
