import threading
from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routers import metrics, notify
import asyncio
from redis_store import store

import MQTT

app = FastAPI()

import logging

def start_MQTT():
    store.redis.flushall()
    logging.info('Starting MQTT...')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(MQTT.main())
    logging.info('MQTT started.')

@app.on_event("startup")
async def startup_event():
    logging.info('Starting up...')
    threading.Thread(target=start_MQTT, daemon=True).start()
    logging.info('Startup complete.')
    
load_dotenv()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# default route
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(metrics.router)
app.include_router(notify.router)