
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock, patch
from api import app

client = TestClient(app)


@pytest.fixture
def mock_renault_client():
    with patch('myrenault.client.RenaultClient') as MockClient:
        # Setup the mock to return an async mock for session login
        instance = MockClient.return_value
        instance.session = AsyncMock()
        instance.session.login = AsyncMock()

        # Mock get_api_accounts
        account = AsyncMock()
        account.account_id = "account_123"
        instance.get_api_accounts = AsyncMock(return_value=[account])

        # Mock vehicle
        vehicle = AsyncMock()
        account.get_api_vehicle = AsyncMock(return_value=vehicle)
        vehicle.get_battery_status = AsyncMock(return_value=MagicMock(
            batteryLevel=80,
            batteryAutonomy=200,
            chargingStatus=0.0,
            plugStatus=0,
            batteryTemperature=25,
            chargingInstantaneousPower=0,
            timestamp="2023-01-01T00:00:00Z"
        ))

        yield instance


def test_battery_status_success(mock_renault_client):
    headers = {
        "x-renault-email": "test@example.com",
        "x-renault-password": "password"
    }
    response = client.get(
        "/api/v1/vehicle/VF1234567890/battery", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["batteryLevel"] == 80


def test_auth_failure():
    with patch('myrenault.client.RenaultClient') as MockClient:
        instance = MockClient.return_value
        instance.session = AsyncMock()
        # Simulate login failure
        instance.session.login = AsyncMock(
            side_effect=Exception("Auth failed"))

        headers = {
            "x-renault-email": "test@example.com",
            "x-renault-password": "wrong"
        }
        response = client.get(
            "/api/v1/vehicle/VF1234567890/battery", headers=headers)
        # Note: In our updated api.py, generic exceptions are still 500, but we want to verify this behavior or if specific exceptions are raised.
        # Ideally, we should simulate a RenaultException or aiohttp.ClientResponseError to see improved handling.
        assert response.status_code == 500
        assert "Auth failed" in response.json()["detail"]


def test_missing_headers():
    response = client.get("/api/v1/vehicle/VF1234567890/battery")
    assert response.status_code == 422  # FastAPI default validation error
