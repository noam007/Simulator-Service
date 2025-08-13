import pytest
import json

@pytest.mark.asyncio
async def test_get_devices(client, redis_client, sample_device):
# Test implementation
    async for i in sample_device:
        sample_device = i
    response = client.get("/devices")
    assert response.status_code == 200
    devices = response.json()
    assert len(devices) >= 1

# Verify device from Redis is in the response
    assert any(d["id"] == sample_device["id"] for d in devices)

@pytest.mark.asyncio
async def test_send_command(client, redis_client, sample_device):
# Test sending a command to a device
    async for i in sample_device:
        sample_device = i
        break

 #   async for i in redis_client:
 #       print(i)
 #       redis_client = i

    command = {"action": "measure", "parameters": {"unit": "celsius"}}

    response = client.post(f"/devices/{sample_device['id']}/command", json=command)
    assert response.status_code == 200

# Verify command was stored in Redis
    command_history = await redis_client.lrange(f"device:{sample_device['id']}:commands", 0, -1)
    assert len(command_history) > 0

# Parse the most recent command
    last_command = json.loads(command_history[0])
    assert last_command["action"] == "measure"
