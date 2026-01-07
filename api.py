from fastapi import FastAPI, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from myrenault.client import MyRenaultClient
import aiohttp

app = FastAPI()

# Mount static files to serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    from starlette.responses import FileResponse
    return FileResponse('static/index.html')


@app.get("/api/v1/vehicle/{vin}/battery")
async def get_battery(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    try:
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(
                email=x_renault_email,
                password=x_renault_password,
                websession=session)
            return await client.battery_status(vin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/vehicle/{vin}/cockpit")
async def get_cockpit(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    try:
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(
                email=x_renault_email,
                password=x_renault_password,
                websession=session)
            return await client.cockpit(vin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/vehicle/{vin}/location")
async def get_location(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    try:
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(
                email=x_renault_email,
                password=x_renault_password,
                websession=session)
            return await client.location(vin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/vehicle/{vin}/hvac-start")
async def hvac_start(
        vin: str,
        temp: float = 21.0,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    try:
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(
                email=x_renault_email,
                password=x_renault_password,
                websession=session)
            return await client.hvac_start(vin, temp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/vehicle/{vin}/hvac-stop")
async def hvac_stop(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    try:
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(
                email=x_renault_email,
                password=x_renault_password,
                websession=session)
            return await client.hvac_stop(vin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/vehicle/{vin}/charge-start")
async def charge_start(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    try:
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(
                email=x_renault_email,
                password=x_renault_password,
                websession=session)
            return await client.charge_start(vin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/vehicle/{vin}/charge-stop")
async def charge_stop(
        vin: str,
        x_renault_email: str = Header(...),
        x_renault_password: str = Header(...)):
    try:
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(
                email=x_renault_email,
                password=x_renault_password,
                websession=session)
            return await client.charge_stop(vin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/vehicle/{vin}/lights")
async def lights(vin: str, x_renault_email: str = Header(...),
                 x_renault_password: str = Header(...)):
    try:
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(
                email=x_renault_email,
                password=x_renault_password,
                websession=session)
            return await client.blink_lights(vin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/vehicle/{vin}/honk")
async def honk(vin: str, x_renault_email: str = Header(...),
               x_renault_password: str = Header(...)):
    try:
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(
                email=x_renault_email,
                password=x_renault_password,
                websession=session)
            return await client.honk(vin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
