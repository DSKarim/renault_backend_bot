from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from myrenault.client import MyRenaultClient
import aiohttp
import os

app = FastAPI()

# Modèle de requête pour le login (simplifié)
class LoginRequest(BaseModel):
    renault_email: str
    renault_password: str

@app.post("/api/v1/vehicle/{vin}/battery")
async def get_battery(vin: str, x_renault_email: str = Header(...), x_renault_password: str = Header(...)):
    """
    Exemple simple sans base de données intermédiaire.
    L'app Android envoie les crédentials Renault dans les headers (via HTTPS uniquement !).
    """
    try:
        # On instancie le client pour CET utilisateur spécifique
        async with aiohttp.ClientSession() as session:
            client = MyRenaultClient(email=x_renault_email, password=x_renault_password, websession=session)
            data = await client.battery_status(vin)
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
