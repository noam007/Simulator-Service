Simulator Service using FastAPI and Redis Device API

## Overview
This project implements a simple **FastAPI** application that interacts with **Redis** to manage IoT-like devices.
It provides REST endpoints to:

* Retrieve all registered devices
* Retrieve details of a specific device
* Send commands to a device (stored in Redis)
* Tests using pytest to validate the API behavior.

## Requirements
* Python 3.10+
* Redis server running locally (port `6379`)
* The following Python dependencies:
  fastapi
  pydantic
  redis[asyncio]
  pytest
  pytest-asyncio
  httpx

Install dependencies with:
pip install -r requirements.txt

## File Structure
app.py                # Main FastAPI application with Redis integration

test_app.py           # API test cases for endpoints

conftest.py           # Pytest fixtures for Redis and FastAPI client setup

## Running the Application
1. **Start Redis** (must be running locally on port 6379) 
   redis-server

2. **Run FastAPI app**
  uvicorn app:app --reload

3. API will be available at:
   http://127.0.0.1:8000
   https://redis.io/docs/latest/   # Official Redis Documentation 

## API Endpoints

### `GET /devices`

Returns a list of all devices stored in Redis.

**Example Response:**

```
  {
    "id": "device-1",
    "name": "Test Device",
    "type": "temperature_sensor",
    "status": "normal",
    "online": true
  }
```


GET /devices/{device_id}
Returns details of a single device.

## Example Response:

```
json
{
  "id": "device-1",
  "name": "Test Device",
  "type": "temperature_sensor",
  "status": "normal",
  "online": true
}
```

**Error:** Returns 404 if device is not found.

---

### `POST /devices/{device_id}/command`

Sends a command to a specific device. The command is appended to a Redis list for that device.

**Example Request:**
```json
{
  "action": "measure",
  "parameters": { "unit": "celsius" }
}
```
**Example Response:**

```json
{ "message": "Command sent to device device-1" }
```

## Running Tests
To execute the test suite:
```
pytest -v
```
Tests will:

* Spin up a temporary Redis connection
* Create a sample device
* Validate `/devices` and `/devices/{id}/command` behavior

## Notes

* Redis data is cleared before and after each test run (using 'Clean up' function. 
* Device data is stored as a Redis **hash** (`HSET`), commands are stored in a **list** (`RPUSH`).
* Pagination for `/devices` is not yet implemented but can be added using SCAN cursors.

