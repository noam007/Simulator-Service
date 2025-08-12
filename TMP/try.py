# Create a "Device Simulator" service using FastAPI that simulates IoT devices, with Redis as the data store:
#
# 1. Have at least 3 API endpoints:
#     - `GET /devices` - List all simulated devices
#     - `GET /devices/{device_id}` - Get details of a specific device
#     - `POST /devices/{device_id}/command` - Send a command to a device

# Redis Documentations : http://127.0.0.1:8001/docs#/

from fastapi import FastAPI
import uvicorn
import redis

app = FastAPI(title="Noam", version="1.0") # create the APP instance

redis_client = redis.Redis(host="localhost", port=6379, db=0)
redis_client.ping()

# Add a string key-value pair
redis_client.set('device1', 'Hello Redis_1')
redis_client.set('device2', 'Hello Redis_2')
redis_client.set('device3', 'Hello Redis_3')

# first End point    ( need to run this in the brouwer 'http://127.0.0.1:8001/devices')
@app.get("/devices")
def get_devices():
    cursor = 0
    cursor, keys = redis_client.scan(cursor=cursor)
    return keys

# device_id
@app.get("/devices/{device_id}") # needs an input , run like "http://127.0.0.1:8001/devices/device1"
def get_devic_id(device_id):
    retrieved_value = redis_client.get(device_id)
    return retrieved_value


# POST /devices/{device_id}/command    # CANNOT BE DONE BY BROWSER (POSTMAN or CURL Command)
@app.post("/devices/{device_id}/command") # needs an input , run like "http://127.0.0.1:8001/devices/device1"
def post_devic_id(device_id):
    command = "hi from NY"
    redis_client.set(device_id, command)
    return "success"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001) # running the APP instance where the APP starts






