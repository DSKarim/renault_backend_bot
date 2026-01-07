import os
import aiohttp
import logging
import datetime
import importlib.metadata
from functools import wraps
from renault_api.renault_client import RenaultClient

# Configure logger for this module
logger = logging.getLogger(__name__)


def monitor_request(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        self.stats["requests_total"] += 1
        try:
            result = await func(self, *args, **kwargs)
            self.stats["requests_success"] += 1
            return result
        except Exception:
            self.stats["requests_failed"] += 1
            raise
    return wrapper


class MyRenaultClient:
    def __init__(self, email=None, password=None, websession=None):
        self.email = email or os.environ.get("RENAULT_EMAIL")
        self.password = password or os.environ.get("RENAULT_PASSWORD")

        if not self.email or not self.password:
            raise ValueError(
                "Email and Password must be provided either as arguments or environment variables.")

        self.websession = websession
        self.client = None
        self.vehicle_cache = {}  # VIN -> vehicle object

        self.started_at = datetime.datetime.now()
        self.stats = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_failed": 0
        }

    def get_stats(self):
        return {
            "uptime": datetime.datetime.now() - self.started_at,
            "cache_size": len(self.vehicle_cache),
            **self.stats
        }

    async def get_session(self):
        if self.websession is None or self.websession.closed:
            self.websession = aiohttp.ClientSession()
            self.client = RenaultClient(
                websession=self.websession, locale="fr_FR")
            await self.client.session.login(self.email, self.password)
        return self.client

    async def get_vehicle(self, vin):
        # Clean VIN input
        vin = vin.strip().upper()

        if vin in self.vehicle_cache:
            if not self.websession or self.websession.closed:
                self.vehicle_cache = {}
            else:
                return self.vehicle_cache[vin]

        client = await self.get_session()

        # We need to find the account that has the vehicle.
        # client.get_api_accounts() returns a list of RenaultAccount
        try:
            accounts = await client.get_api_accounts()
        except Exception as e:
            logger.error(f"Failed to retrieve API accounts: {e}")
            raise

        logger.info(f"Found {len(accounts)} Renault accounts.")

        # Performance optimization:
        # If the user has only one account (common case), we skip listing all vehicles
        # and directly instantiate the vehicle object. This saves one API call per request.
        # If the VIN is invalid, the subsequent operation (e.g., battery_status) will fail.
        if len(accounts) == 1:
            account = accounts[0]
            logger.info(
                f"Single account detected ({account.account_id}). Optimistically returning vehicle.")
            api_vehicle = await account.get_api_vehicle(vin)
            self.vehicle_cache[vin] = api_vehicle
            return api_vehicle

        found_vins = []

        for account in accounts:
            try:
                # We need to list vehicles for this account to see if VIN matches.
                # account.get_vehicles() returns list of KamereonVehicleData
                vehicles_response = await account.get_vehicles()
                vehicles = vehicles_response.vehicleLinks or []

                for v in vehicles:
                    # Clean VIN from API just in case
                    v_vin = v.vin.strip().upper() if v.vin else ""
                    found_vins.append(v_vin)

                    if v_vin == vin:
                        logger.info(
                            f"Vehicle found in account {account.account_id}")
                        api_vehicle = await account.get_api_vehicle(vin)
                        self.vehicle_cache[vin] = api_vehicle
                        return api_vehicle
            except Exception as e:
                logger.error(
                    f"Error checking account {account.account_id}: {e}")
                continue

        logger.error(
            f"Vehicle with VIN {vin} not found. Available VINs: {found_vins}")
        raise ValueError(
            f"Vehicle with VIN {vin} not found in any account. Found: {found_vins}")

    @monitor_request
    async def battery_status(self, vin):
        vehicle = await self.get_vehicle(vin)
        status = await vehicle.get_battery_status()

        data = {
            "batteryLevel": status.batteryLevel,
            "batteryAutonomy": status.batteryAutonomy,
            "chargingStatus": status.chargingStatus,
            "plugStatus": status.plugStatus,
            "batteryTemperature": status.batteryTemperature,
            "chargingInstantaneousPower": status.chargingInstantaneousPower,
            "timestamp": status.timestamp
        }
        logger.info(f"Battery status collected: {data}")
        return data

    @monitor_request
    async def cockpit(self, vin):
        vehicle = await self.get_vehicle(vin)
        cockpit = await vehicle.get_cockpit()
        data = {
            "totalMileage": cockpit.totalMileage,
        }
        logger.info(f"Cockpit data collected: {data}")
        return data

    @monitor_request
    async def hvac_start(self, vin, t):
        vehicle = await self.get_vehicle(vin)
        return await vehicle.set_ac_start(t)

    @monitor_request
    async def hvac_stop(self, vin):
        vehicle = await self.get_vehicle(vin)
        return await vehicle.set_ac_stop()

    @monitor_request
    async def location(self, vin):
        vehicle = await self.get_vehicle(vin)
        loc = await vehicle.get_location()
        data = {
            "latitude": loc.gpsLatitude,
            "longitude": loc.gpsLongitude,
            "timestamp": loc.lastUpdateTime
        }
        logger.info(f"Location collected: {data}")
        return data

    @monitor_request
    async def charge_start(self, vin):
        vehicle = await self.get_vehicle(vin)
        return await vehicle.set_charge_start()

    @monitor_request
    async def charge_stop(self, vin):
        vehicle = await self.get_vehicle(vin)
        # Fix for 'invalid-body-format' on some vehicles (Zoe Phase 2)
        # The library default sends action='stop', but 'cancel' appears to be required or safer for the 'ChargingStart' type.
        # We perform a manual request here to override the body.
        try:
            # Retrieve the endpoint URL using the standard mechanism
            endpoint = await vehicle.get_full_endpoint("actions/charge-stop")

            # Construct the custom payload
            # We use "cancel" instead of "stop" which causes the error
            json_payload = {
                "data": {
                    "type": "ChargingStart",
                    "attributes": {
                        "action": "cancel",
                    },
                }
            }

            # Use the underlying session to send the request
            response = await vehicle.session.http_request("POST", endpoint, json_payload)
            return response
        except Exception:
            # If the manual fix fails, fallback to library method (or just re-raise if library method is same as failed)
            # But here we just assume the fix is better.
            raise

    @monitor_request
    async def blink_lights(self, vin):
        vehicle = await self.get_vehicle(vin)
        return await vehicle.start_lights()

    @monitor_request
    async def honk(self, vin):
        vehicle = await self.get_vehicle(vin)
        return await vehicle.start_horn()

    async def check_api_version(self):
        try:
            current_version = importlib.metadata.version('renault-api')

            async with aiohttp.ClientSession() as session:
                async with session.get('https://pypi.org/pypi/renault-api/json') as response:
                    if response.status == 200:
                        data = await response.json()
                        latest_version = data['info']['version']
                    else:
                        latest_version = "Unknown"
            return current_version, latest_version
        except Exception as e:
            logger.error(f"Failed to check version: {e}")
            return "Unknown", "Unknown"
