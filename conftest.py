import pytest
import redis.asyncio as redis
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
async def redis_client():
# Setup Redis connection
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
# Clear database before test
    await redis_client.flushdb()

    yield redis_client

# Clear database after test
    await redis_client.flushdb()
    await redis_client.close()

@pytest.fixture
def client():
# Setup logic - what needs to happen before tests?
    with TestClient(app) as test_client:
# Provide the client to the test
        yield test_client
# Teardown logic - what needs to happen after tests?

@pytest.fixture
async def sample_device(redis_client):

    async for i in redis_client:
        redis_client = i
# Create a sample device in Redis
    device_id = "device-1"
    device_data = {
        "name": "Test Device",
        "type": "temperature_sensor",
        "status": "normal",
        "online": "true"
    }
    await redis_client.sadd("device_ids", device_id)
# Store in Redis
    await redis_client.hset(f"device:{device_id}", mapping=device_data)
    print("await happened")
    yield {"id": device_id, **device_data}

# Clean up
    #await redis_client.delete(f"device:{device_id}")
