import asyncio
import redis.asyncio as redis
import random

async def setup_devices(redis_client):
    device_data_list = [
        {
            "name": "Cisco 4451-X ISR",
            "type": "Integrated Services Routers",
            "status": "off",
            "online": "true"
        },
        {
            "name": "Cisco ASR 1001-X",
            "type": "Aggregation Services Routers",
            "status": "on",
            "online": "true"
        },
        {
            "name": "Cisco 8000 Series",
            "type": "Carrier-Grade Routers",
            "status": "locked",
            "online": "false"
        }
    ]

    created_devices = []
    for data in device_data_list:
        device_id = "device_id" + str(random.randint(1, 100))

        # Add the generated ID to the device data
        data["id"] = device_id

        # Store the device in Redis
        await redis_client.hset(f"device:{device_id}", mapping=data)


async def delete_devices(redis_client):
    device_keys = []
    async for key in redis_client.scan_iter(match="device:*"):
        device_keys.append(key)

    for key in device_keys:
        print(key)
        await redis_client.delete(key)

async def create_device(redis_client):
    """Creates a single device in Redis and cleans it up after the test."""
    device_id = "test-device-456"  # You can use a static ID or generate a new one
    device_data = {
        "id": device_id,
        "name": "Single Test Device",
        "type": "pressure_sensor",
        "status": "online",
        "online": "true"
    }

    # Store the device data in a Redis Hash
    await redis_client.hset(f"device:{device_id}", mapping=device_data)


async def main():
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    await redis_client.ping()
    print("Connected to Redis successfully!")

    ### create singe device
    await create_device(redis_client)

    ### create singe device
    # await setup_devices(redis_client)

    ### delete devices
    # await delete_devices(redis_client)

if __name__ == "__main__":
    asyncio.run(main())
