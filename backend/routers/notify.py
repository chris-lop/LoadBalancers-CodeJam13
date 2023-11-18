from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import StreamingResponse
from typing import Generator
from redis_store import store
import time

router = APIRouter()

def event_generator(truck_id: str) -> Generator:
    """
    This function generates server-sent events.
    """
    while True:
        # check if new event is available for this truckId in redis
        event = store.get_data(truck_id)
        if event is not None:
            # if new event is available, delete it from redis and yield it
            store.set_data(truck_id, "")
            yield f"data: {event}\n\n"
        time.sleep(1)

@router.get("/events/{truck_id}", tags=["events"])
async def get_server_events(truck_id: str):
    return StreamingResponse(event_generator(truck_id), media_type="text/event-stream")