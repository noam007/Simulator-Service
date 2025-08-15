from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import redis.asyncio as redis
from typing import List, Optional
import redis.exceptions as redis_e

app = FastAPI()

# Redis connection pool
async def get_redis():
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    try:
        await redis_client.ping()
        yield redis_client
    except redis_e.ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Redis connection failed: {str(e)}")
    finally:
        await redis_client.close()

# Your models and endpoints here
class DeviceBase(BaseModel):
    name: str
    type: str
    status: str

class Device(DeviceBase):
    id: str
    online: bool

@app.get("/devices", response_model=List[Device])
async def get_devices(r: redis.Redis = Depends(get_redis)):
    # Implement logic to get devices from Redis
    prefix = "device:*"

    # Use SCAN to iterate over keys with the prefix
    cursor = 0
    device_ids = []

    # TODO: extend API for pagination
    while True:
        cursor, keys = await r.scan(cursor=cursor, match=prefix, count=100)
        device_ids.extend(keys)
        if cursor == 0:
            break

    devices = []
    for device_id in device_ids:
        data = await r.hgetall(device_id)
        if data:
            print(Device(**data))
            devices.append(Device(**data))
        print()
    return devices


@app.get("/devices/{device_id}", response_model=Device)
async def get_device(device_id: str, r: redis.Redis = Depends(get_redis)):
# Implement logic to get a specific device from Redis
    data = await r.hgetall(f"device:{device_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Device not found")
    return Device(**data)


@app.post("/devices/{device_id}/command")
async def send_command(device_id: str, command: dict, r: redis.Redis = Depends(get_redis)):
# Implement logic to send a command to a device
    exists = await r.exists(f"device:{device_id}")
    if not exists:
        raise HTTPException(status_code=404, detail="Device not found")
    await r.rpush(f"device:{device_id}:commands", str(command))
    return {"message": f"Command sent to device {device_id}"}


@app.delete("/devices/{device_id}", status_code=204)
async def delete_device(device_id: str, r: redis.Redis = Depends(get_redis)):
    device_key = f"device:{device_id}"
    exists = await r.exists(device_key)
    if not exists:
        raise HTTPException(status_code=404, detail="Device not found")

    pipeline = r.pipeline()
    await pipeline.delete(device_key)
    await pipeline.delete(f"{device_key}:commands")

    await pipeline.execute()

    return {f"device {device_key} was removed"}