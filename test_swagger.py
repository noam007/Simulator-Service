# filename: test_swagger.py
from http.client import responses

import pytest
from fastapi.testclient import TestClient
import json


@pytest.mark.asyncio
async def test_openapi_schema_is_valid(client: TestClient):
    """Validate that the OpenAPI schema is accessible and is valid JSON."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    try:
        schema = response.json()
        print(schema)
    except json.JSONDecodeError:
        pytest.fail("OpenAPI schema is not a valid JSON document.")

    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema
    assert "components" in schema

    # Simple check for a few key endpoints
    assert "/devices" in schema["paths"]
    assert "/devices/{device_id}" in schema["paths"]
    assert "/devices/{device_id}/command" in schema["paths"]

    # Check for the main Pydantic schemas
    assert "Device" in schema["components"]["schemas"]
    assert "Command" in schema["components"]["schemas"]