from fastapi import FastAPI, HTTPException, Header, status
from fastapi.staticfiles import StaticFiles
from myrenault.client import MyRenaultClient
import aiohttp
import asyncio
from renault_api.exceptions import RenaultException
from pydantic import BaseModel

app = FastAPI()

# Mount static files to serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration
DEFAULT_TIMEOUT = 30  # seconds


class BatteryStatusResponse(BaseModel):
    batteryLevel: int
    batteryAutonomy: int
    chargingStatus: float
    plugStatus: int
    batteryTemperature: int
    chargingInstantaneousPower: float
    timestamp: str


class CockpitResponse(BaseModel):
    totalMileage: float


class LocationResponse(BaseModel):
    latitude: float
    longitude: float
    timestamp: str


@app.get("/")
async def read_root():
    from starlette.responses import FileResponse
    return FileResponse('static/index.html')


async def get_client_session():
    timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)
    return aiohttp.ClientSession(timeout=timeout)


# Helper to reduce boilerplate


async def handle_request(client_action, email, password, *args):
    try:
        async with await get_client_session() as session:
            client = MyRenaultClient(
                email=email,
                password=password,
                websession=session)
            return await client_action(client, *args)
    except ValueError as e:
        # Often raised when VIN not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RenaultException as e:
        # Renault API specific errors (e.g. auth failed usually raises
        # exceptions inside renault-api)
        # Checking exception types from renault-api would be better if we
        # imported them all.
        # Assuming RenaultException is base.
        # Note: Auth errors might be aiohttp.ClientResponseError if 401/403
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=f"Renault API error: {str(e)}")
    except aiohttp.ClientResponseError as e:
        if e.status == 401 or e.status == 403:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials or Renault API unauthorized"
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Upstream error: {str(e)}"
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail="Request to Renault API timed out")
    except Exception as e:
        # Fallback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/api/v1/vehicle/{vin}/battery", response_model=BatteryStatusResponse)
async def get_battery(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    return await handle_request(
        lambda c, v: c.battery_status(v),
        x_renault_email,
        x_renault_password,
        vin
    )


@app.get("/api/v1/vehicle/{vin}/cockpit", response_model=CockpitResponse)
async def get_cockpit(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    return await handle_request(
        lambda c, v: c.cockpit(v),
        x_renault_email,
        x_renault_password,
        vin
    )


@app.get("/api/v1/vehicle/{vin}/location", response_model=LocationResponse)
async def get_location(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    return await handle_request(
        lambda c, v: c.location(v),
        x_renault_email,
        x_renault_password,
        vin
    )


@app.post("/api/v1/vehicle/{vin}/hvac-start")
async def hvac_start(
        vin: str,
        temp: float = 21.0,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    return await handle_request(
        lambda c, v, t: c.hvac_start(v, t),
        x_renault_email,
        x_renault_password,
        vin,
        temp
    )


@app.post("/api/v1/vehicle/{vin}/hvac-stop")
async def hvac_stop(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    return await handle_request(
        lambda c, v: c.hvac_stop(v),
        x_renault_email,
        x_renault_password,
        vin
    )


@app.post("/api/v1/vehicle/{vin}/charge-start")
async def charge_start(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    return await handle_request(
        lambda c, v: c.charge_start(v),
        x_renault_email,
        x_renault_password,
        vin
    )


@app.post("/api/v1/vehicle/{vin}/charge-stop")
async def charge_stop(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    return await handle_request(
        lambda c, v: c.charge_stop(v),
        x_renault_email,
        x_renault_password,
        vin
    )


@app.post("/api/v1/vehicle/{vin}/lights")
async def lights(vin: str, x_renault_email: str = Header(...),
                 x_renault_password: str = Header(...)):
    return await handle_request(
        lambda c, v: c.blink_lights(v),
        x_renault_email,
        x_renault_password,
        vin
    )


@app.post("/api/v1/vehicle/{vin}/honk")
async def honk(vin: str, x_renault_email: str = Header(...),
               x_renault_password: str = Header(...)):
    return await handle_request(
        lambda c, v: c.honk(v),
        x_renault_email,
        x_renault_password,
        vin
    )
