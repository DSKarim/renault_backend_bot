# Guide d'utilisation Backend / API pour Application Android

Ce guide explique comment transformer le code Python existant (initialement conçu pour un bot Telegram) en un backend API robuste pour servir une application Android (ou iOS), en utilisant par exemple Firebase.

## Cote de Réalisabilité : 8/10

**Pourquoi 8/10 ?**
*   **Points forts (+)** : La logique métier (`MyRenaultClient`) est déjà isolée dans le package `myrenault`. Elle gère les connexions, les retries et le formatage des données. La réutilisation de ce code est directe.
*   **Points d'attention (-)** : Le code actuel est conçu pour un *utilisateur unique* (variables d'environnement statiques). Pour une application mobile publique, il faut modifier la classe pour gérer dynamiquement les identifiants de chaque utilisateur connecté.

---

## Architecture Recommandée

Plutôt que d'implémenter la logique Renault directement dans l'application Android (complexe à maintenir), il est recommandé d'utiliser une architecture **Backend-for-Frontend (BFF)**.

1.  **Application Android** : Gère l'UI et l'authentification utilisateur (via Firebase Auth).
2.  **Firebase Auth** : Gère l'inscription/connexion des utilisateurs.
3.  **Backend Python (API)** : Héberge le code `myrenault`, exposé via FastAPI ou Flask.
4.  **Base de Données (Firestore)** : Stocke les liens entre l'UID Firebase et les identifiants Renault (chiffrés).

### Schéma de flux
```mermaid
Android App -> (Token Firebase) -> API Python
API Python -> (Vérifie Token) -> Firebase Admin
API Python -> (Récupère crédentials Renault) -> Firestore
API Python -> (Commandes/Status) -> Serveurs Renault
```

---

## Guide d'Implémentation (Étape par Étape)

### 1. Adapter `MyRenaultClient` pour le Multi-utilisateurs

Actuellement, `myrenault/client.py` charge les identifiants depuis `os.environ`. Il faut modifier `__init__` pour accepter les identifiants dynamiquement.

**Modification suggérée dans `myrenault/client.py` :**

```python
class MyRenaultClient:
    def __init__(self, email=None, password=None, websession=None):
        # On accepte les crédentials en paramètres
        self.email = email
        self.password = password

        # Fallback sur l'environnement si non fourni (pour compatibilité bot)
        if not self.email:
            self.email = os.environ.get("RENAULT_EMAIL")
        if not self.password:
            self.password = os.environ.get("RENAULT_PASSWORD")

        if not self.email or not self.password:
             raise ValueError("Email and Password must be provided.")

        # Réutilisation de la session si fournie (optimisation API)
        self.websession = websession
        # ... le reste du code reste inchangé ...
```

### 2. Créer une API avec FastAPI

Créez un fichier `api.py` à la racine pour exposer les fonctions.

```python
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from myrenault.client import MyRenaultClient
import aiohttp

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
```

### 3. Intégration Firebase (Optionnelle mais recommandée)

Pour ne pas faire transiter les mots de passe Renault à chaque requête :

1.  L'utilisateur se connecte sur Android via Firebase Auth.
2.  L'utilisateur entre ses identifiants Renault **une seule fois**.
3.  L'app les envoie au backend Python qui les chiffre et les stocke dans Firestore (associés à l'UID Firebase).
4.  Pour les requêtes suivantes, l'app envoie juste le token Firebase. Le backend vérifie le token, récupère les identifiants déchiffrés en base, et appelle Renault.

### 4. Déploiement

Vous pouvez déployer cette API sur **Google Cloud Run** ou tout serveur supportant Docker.

**Exemple de `Dockerfile.api` :**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt fastapi uvicorn
COPY . .
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Résumé

L'idée est **très réalisable**. Le cœur du travail (la communication avec Renault) est déjà fait. Le travail restant consiste principalement à créer "l'enveloppe" Web (API) autour de ce cœur pour qu'il puisse servir plusieurs utilisateurs simultanément.
