from fastapi import FastAPI, HTTPException
import redis.asyncio as redis
import asyncio

# notes:
### Part 1: The Simulator Service

# Create a "Device Simulator" service using FastAPI that simulates IoT devices, with Redis as the data store:
#
# 1. Have at least 3 API endpoints:
#     - `GET /devices` - List all simulated devices
#     - `GET /devices/{device_id}` - Get details of a specific device
#     - `POST /devices/{device_id}/command` - Send a command to a device

# Initialize FastAPI app
app = FastAPI()

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Example route: Fetch data with Redis caching
@app.get("/items/{item_id}")
async def get_item(item_id: str):
    # Check if the item is cached in Redis
    cached_item = await redis_client.get(item_id)
    if cached_item:
        return {"item_id": item_id, "data": cached_item, "source": "cache"}

    # Simulate fetching data from a database or external API
    await asyncio.sleep(2)  # Simulate delay
    item_data = f"Data for item {item_id}"

    # Cache the data in Redis (expires in 60 seconds)
    await redis_client.setex(item_id, 60, item_data)

    return {"item_id": item_id, "data": item_data, "source": "database"}

# Health check route
@app.get("/")
async def health_check():
    return {"status": "API is running"}

# Cleanup Redis connection on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()
