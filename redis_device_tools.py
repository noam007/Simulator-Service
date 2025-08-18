import asyncio
import redis.asyncio as redis
import random

async def setup_devices(redis_client):
    """ setting up devices using specific device list and random"""
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

    # adding random device ID's
    created_devices = []
    for data in device_data_list:
        device_id = "device_id" + str(random.randint(1, 100))

        # Add the generated ID to the device data
        data["id"] = device_id

        # Store the device in Redis
        await redis_client.hset(f"device:{device_id}", mapping=data)


async def delete_devices(redis_client):
    """removing all devices from DB """
    device_keys = []
    async for key in redis_client.scan_iter(match="device:*"):
        device_keys.append(key)

    for key in device_keys:
        print(key)
        await redis_client.delete(key)


async def get_names(redis_client):
    """getting device list """
    device_keys = []
    async for key in redis_client.scan_iter(match="device:*"):
        device_keys.append(key)

    if not device_keys :
        print("there are no devices in Redis")
    else:
        print(device_keys)

    return device_keys


async def create_device(redis_client):
    """Creates a single device in Redis and cleans it up after the test."""
    device_id = "device_id" + str(random.randint(1, 100))
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


async def add_comment_to_device(redis_client, device_id, comment):
    """adding a comment for a device """
    print(device_id,comment)
    await redis_client.hset(f"device:{device_id}", key="comment", value=comment)
    print(f"Comment added to device '{device_id}'.")


async def modify_field_value(redis_client,device_list):
    """ Fetch all devices and their full data as list of dicts."""
    devices = []
    async for key in redis_client.scan_iter(match="device:*"):
        device_data = await redis_client.hgetall(key)
        if device_data:
            devices.append(device_data)

    if not devices:
        print("No devices found in Redis.")
    else:
        print("\n--- All Devices in Redis ---")
        index  = 0
        for dev in devices:
            print(f"device index {index} is : {dev}")
            index += 1

    """modify field value of a device """

    if devices:
        # TODO: add protection mechanism
        device_choice = input(f"Enter your device ID (0-{index-1}): ")
        change_field = input(f"Enter field choice:")
        value_to_chane = input(f"Enter value to change:")

        device_choice_id = devices[int(device_choice)]["id"]

        await redis_client.hset(
            f"device:{device_choice_id}",
            key=f"{change_field}",
            value=f"{value_to_chane}"
        )


async def main():
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    await redis_client.ping()
    print("Connected to Redis successfully!")

    while True:
        print("\n--- Redis Device Management Menu ---")
        print("1. Create a single device")
        print("2. Create multiple sample devices")
        print("3. Delete all devices")
        print("4. Get all device names")
        print("5. Add a comment to a device")
        print("6. Modify field value")
        print("7. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            await create_device(redis_client)
            print("Single device created.")
        elif choice == '2':
            await setup_devices(redis_client)
            print("Multiple devices created.")
        elif choice == '3':
            await delete_devices(redis_client)
            print("All devices deleted.")
        elif choice == '4':
            await get_names(redis_client)
        elif choice == '5':
            device_id = input("Enter the device ID: ")
            comment = input("Enter the comment: ")
            await add_comment_to_device(redis_client, device_id, comment)
        elif choice == '6':
            device_list = await get_names(redis_client)
            print(device_list)
            await modify_field_value(redis_client,device_list)
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    asyncio.run(main())
