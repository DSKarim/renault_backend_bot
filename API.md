# Documentation de l'API Renault Wrapper

API passerelle (wrapper) vers les services MyRenault. Gere l'authentification de session a chaque requete de maniere stateless.

## Base URL

Developpement local : `http://localhost:8000`

## Authentification

Aucun endpoint de login persistant. Chaque requete vers `/api/v1/*` doit inclure les identifiants dans les headers HTTP.

**Headers requis :**

| Header | Description |
|---|---|
| `x-renault-email` | Adresse email du compte MyRenault |
| `x-renault-password` | Mot de passe du compte MyRenault |

**Fallback :** Si les headers sont absents, les variables d'environnement `RENAULT_EMAIL` et `RENAULT_PASSWORD` sont utilisees.

## Endpoints

### Liste des vehicules

Retourne tous les vehicules associes au compte utilisateur (parcours de tous les comptes Renault).

- **URL** : `GET /api/v1/vehicles`
- **Headers** : Auth headers requis

**Reponse** (`200 OK`) :
```json
[
  {
    "vin": "VF1XXXXXXXXXX",
    "brand": "RENAULT",
    "model": "ZOE",
    "registrationNumber": "AB-123-CD",
    "energy": "ELEC",
    "picture": "https://..."
  }
]
```

### Statut de la batterie

Retourne le niveau de charge, l'autonomie, le statut de branchement et la puissance de charge.

- **URL** : `GET /api/v1/vehicle/{vin}/battery`
- **Parametre URL** : `vin` - Vehicle Identification Number
- **Headers** : Auth headers requis

**Reponse** (`200 OK`) :
```json
{
  "batteryLevel": 75,
  "batteryAutonomy": 180,
  "chargingStatus": 0,
  "plugStatus": 0,
  "batteryTemperature": 20,
  "chargingInstantaneousPower": null,
  "timestamp": "2026-03-23T10:30:00Z"
}
```

| Champ | Type | Description |
|---|---|---|
| `batteryLevel` | int | Niveau de batterie en % |
| `batteryAutonomy` | int | Autonomie estimee en km |
| `chargingStatus` | int | 0 = pas en charge, 1 = en charge |
| `plugStatus` | int | 0 = debranche, 1 = branche |
| `batteryTemperature` | int | Temperature batterie en C |
| `chargingInstantaneousPower` | float | Puissance de charge instantanee en kW |
| `timestamp` | str | Horodatage de la derniere mise a jour |

### Cockpit

Retourne le kilometrage total du vehicule.

- **URL** : `GET /api/v1/vehicle/{vin}/cockpit`
- **Parametre URL** : `vin`
- **Headers** : Auth headers requis

**Reponse** (`200 OK`) :
```json
{
  "totalMileage": 45230.5
}
```

### Localisation

Retourne les coordonnees GPS du vehicule.

- **URL** : `GET /api/v1/vehicle/{vin}/location`
- **Parametre URL** : `vin`
- **Headers** : Auth headers requis

**Reponse** (`200 OK`) :
```json
{
  "latitude": 48.8566,
  "longitude": 2.3522,
  "timestamp": "2026-03-23T10:30:00Z"
}
```

---

### Commandes a distance

#### Demarrer la climatisation (HVAC)

Lance la pre-climatisation du vehicule a la temperature specifiee.

- **URL** : `POST /api/v1/vehicle/{vin}/hvac-start`
- **Parametre URL** : `vin`
- **Query params** :
  - `temp` (float, optionnel) : Temperature cible en C (defaut: 21.0)
- **Headers** : Auth headers requis

#### Arreter la climatisation (HVAC)

- **URL** : `POST /api/v1/vehicle/{vin}/hvac-stop`
- **Parametre URL** : `vin`
- **Headers** : Auth headers requis

#### Demarrer la charge

- **URL** : `POST /api/v1/vehicle/{vin}/charge-start`
- **Parametre URL** : `vin`
- **Headers** : Auth headers requis

#### Arreter la charge

Utilise un payload personnalise avec l'action `cancel` (au lieu de `stop`) pour assurer la compatibilite avec certains vehicules (Zoe Phase 2).

- **URL** : `POST /api/v1/vehicle/{vin}/charge-stop`
- **Parametre URL** : `vin`
- **Headers** : Auth headers requis

#### Clignoter les phares

Permet de localiser le vehicule en faisant clignoter les phares.

- **URL** : `POST /api/v1/vehicle/{vin}/lights`
- **Parametre URL** : `vin`
- **Headers** : Auth headers requis

#### Klaxonner

Permet de localiser le vehicule en actionnant le klaxon.

- **URL** : `POST /api/v1/vehicle/{vin}/honk`
- **Parametre URL** : `vin`
- **Headers** : Auth headers requis

---

### Interface web

- **URL** : `GET /`
- Sert la page `static/index.html` permettant de tester tous les endpoints depuis un navigateur

## Gestion des erreurs

| Code HTTP | Signification | Cause |
|---|---|---|
| `401 Unauthorized` | Identifiants invalides | Credentials refuses par l'API Renault (HTTP 401/403) |
| `404 Not Found` | VIN introuvable | Le VIN n'existe dans aucun compte associe |
| `422 Unprocessable Entity` | Headers manquants | Les headers `x-renault-email` ou `x-renault-password` sont absents |
| `500 Internal Server Error` | Erreur interne | Exception non prevue |
| `502 Bad Gateway` | Erreur API Renault | `RenaultException` ou erreur HTTP upstream |
| `504 Gateway Timeout` | Timeout | La requete vers l'API Renault a depasse 30 secondes |

Le corps de la reponse JSON contient un champ `detail` expliquant l'erreur :

```json
{
  "detail": "Vehicle with VIN XXXXX not found in any account. Found: [...]"
}
```
