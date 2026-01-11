
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

        # Mock vehicle list
        vehicle_link = MagicMock()
        vehicle_link.vin = "VF1234567890"
        vehicle_link.vehicleDetails = MagicMock()
        vehicle_link.vehicleDetails.get_brand_label.return_value = "Renault"
        vehicle_link.vehicleDetails.get_model_label.return_value = "Zoe"
        vehicle_link.vehicleDetails.registrationNumber = "AB-123-CD"
        vehicle_link.vehicleDetails.get_energy_code.return_value = "ELEC"
        vehicle_link.vehicleDetails.get_picture.return_value = "http://example.com/pic.jpg"

        vehicles_response = MagicMock()
        vehicles_response.vehicleLinks = [vehicle_link]
        account.get_vehicles = AsyncMock(return_value=vehicles_response)

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


def test_get_vehicles_success(mock_renault_client):
    headers = {
        "x-renault-email": "test@example.com",
        "x-renault-password": "password"
    }
    response = client.get(
        "/api/v1/vehicles", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["vin"] == "VF1234567890"
    assert data[0]["brand"] == "Renault"
    assert data[0]["model"] == "Zoe"
    assert data[0]["registrationNumber"] == "AB-123-CD"
    assert data[0]["energy"] == "ELEC"
    assert data[0]["picture"] == "http://example.com/pic.jpg"
