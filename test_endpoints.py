import pytest

@pytest.mark.asyncio
async def test_get_devices(client, redis_client, sample_device):
    """ this test will get a list of devices """
    async for i in sample_device:
        sample_device = i
    response = client.get("/devices")
    assert response.status_code == 200
    devices = response.json()
    assert len(devices) >= 1

# Verify device from Redis is in the response
    assert any(d["id"] == sample_device["id"] for d in devices)



@pytest.mark.asyncio
async def test_create_and_delete_device(client,redis_client,sample_device):
    """ this test will create and delete a single device """

    sample_device_dict = []

    async for device_data in sample_device:
        sample_device_dict = device_data
        break

    device_id_to_delete = sample_device_dict['id']

    if device_id_to_delete:
        response = client.delete(f"/devices/{device_id_to_delete}")
        print(response.status_code)

    else:
        assert device_id_to_delete == 0
        print("no devices to delete")



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