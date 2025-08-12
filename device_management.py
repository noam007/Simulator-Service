import asyncio
import redis.asyncio as redis

async def setup_devices(redis_client):
    devices = {
        "device-1": {
            "name": "Device One",
            "type": "temperature_sensor",
            "status": "normal",
            "online": "true"
        },
        "device-2": {
            "name": "Device Two",
            "type": "humidity_sensor",
            "status": "warning",
            "online": "false"
        },
        "device-3": {
            "name": "Device Three",
            "type": "pressure_sensor",
            "status": "error",
            "online": "true"
        },
    }

    await redis_client.sadd("device_ids", *devices.keys())

    for device_id, device_data in devices.items():
        await redis_client.hset(f"device:{device_id}", mapping=device_data)

    print("Devices loaded to Redis")


async def delete_devices(redis_client):
    device_ids = await redis_client.smembers("device_ids")
    if device_ids:
        for device_id in device_ids:
            await redis_client.delete(f"device:{device_id}")
        await redis_client.delete("device_ids")
        print("Devices deleted from Redis")
    else:
        print("No devices to delete")


async def main():
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


    await delete_devices(redis_client)
    # await setup_devices(redis_client)

    await redis_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
