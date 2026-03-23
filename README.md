# MyRenault API Backend

Backend FastAPI stateless pour le controle de vehicules electriques Renault (ZOE, Megane E-Tech, Twingo ZE, etc.) via l'API non officielle My Renault.

Ce projet encapsule la librairie [renault-api](https://github.com/hacf-fr/renault-api) dans une API RESTful, concue pour servir des applications mobiles (voir le [plan Android](PLAN_ANDROID.md)), des dashboards ou des systemes domotiques.

## Fonctionnalites implementees

### Consultation (GET)

| Endpoint | Description | Donnees retournees |
|---|---|---|
| `GET /api/v1/vehicles` | Liste des vehicules du compte | VIN, marque, modele, immatriculation, energie, photo |
| `GET /api/v1/vehicle/{vin}/battery` | Statut batterie | Niveau (%), autonomie (km), statut charge, statut prise, temperature, puissance instantanee |
| `GET /api/v1/vehicle/{vin}/cockpit` | Tableau de bord | Kilometrage total |
| `GET /api/v1/vehicle/{vin}/location` | Localisation GPS | Latitude, longitude, horodatage |

### Commandes a distance (POST)

| Endpoint | Description | Parametres |
|---|---|---|
| `POST /api/v1/vehicle/{vin}/hvac-start` | Demarrer la climatisation | `temp` (defaut: 21.0) |
| `POST /api/v1/vehicle/{vin}/hvac-stop` | Arreter la climatisation | - |
| `POST /api/v1/vehicle/{vin}/charge-start` | Demarrer la charge | - |
| `POST /api/v1/vehicle/{vin}/charge-stop` | Arreter la charge | - |
| `POST /api/v1/vehicle/{vin}/lights` | Clignoter les phares | - |
| `POST /api/v1/vehicle/{vin}/honk` | Klaxonner | - |

### Architecture et fonctions internes

- **Authentification stateless** : identifiants transmis par headers HTTP (`x-renault-email`, `x-renault-password`) a chaque requete, aucune session persistante
- **Fallback variables d'environnement** : `RENAULT_EMAIL` et `RENAULT_PASSWORD` utilises si les headers sont absents
- **Support multi-utilisateurs** : architecture sans etat permettant a plusieurs utilisateurs de se connecter simultanement
- **Support multi-comptes** : parcours automatique de tous les comptes Renault associes a l'utilisateur
- **Optimisation compte unique** : si un seul compte est detecte, le listing des vehicules est skippe (economie d'un appel API)
- **Cache vehicules** : les objets vehicule sont mis en cache par VIN pour eviter les appels redondants
- **Monitoring des requetes** : decorateur `@monitor_request` comptant les requetes totales, succes et echecs
- **Statistiques** : uptime, taille du cache, compteurs de requetes via `get_stats()`
- **Verification de version** : comparaison de la version locale de `renault-api` avec la derniere version PyPI
- **Fix charge-stop** : payload personnalise avec action `cancel` au lieu de `stop` pour compatibilite Zoe Phase 2
- **Barre de progression** : utilitaire texte pour visualiser un pourcentage (`get_progress_bar()`)
- **Gestion d'erreurs robuste** : mapping HTTP 401/404/502/504/500 selon le type d'exception
- **Interface web** : page HTML statique (`/static/index.html`) pour tester tous les endpoints depuis un navigateur
- **Modeles Pydantic** : validation des reponses (`BatteryStatusResponse`, `CockpitResponse`, `LocationResponse`, `VehicleResponse`)
- **Tests unitaires** : suite pytest avec mocks async (batterie, auth, headers manquants, liste vehicules)

## Stack technique

| Composant | Technologie |
|---|---|
| Framework web | FastAPI + Uvicorn |
| Langage | Python 3.12+ |
| API Renault | renault-api (non officielle) |
| HTTP async | aiohttp, httpx |
| Validation | Pydantic |
| Tests | pytest + unittest.mock |
| Config | python-dotenv |
| Conteneurisation | Docker + Docker Compose |
| Frontend | HTML5 / JavaScript vanilla |

## Demarrage rapide

### Prerequis

- Python 3.12+
- Un compte My Renault valide (email + mot de passe)
- Le VIN de votre vehicule

### Installation locale

```bash
git clone https://github.com/DSKarim/renault_backend_bot.git
cd renault_backend_bot
pip install -r requirements.txt
uvicorn api:app --reload
```

L'API est disponible sur `http://127.0.0.1:8000`.

### Docker

```bash
docker-compose up -d --build
docker-compose logs -f
```

## Utilisation

Chaque requete necessite les headers d'authentification :

```bash
curl -X GET 'http://127.0.0.1:8000/api/v1/vehicle/YOUR_VIN/battery' \
  -H 'x-renault-email: your.email@example.com' \
  -H 'x-renault-password: your_password'
```

```bash
curl -X POST 'http://127.0.0.1:8000/api/v1/vehicle/YOUR_VIN/hvac-start?temp=21' \
  -H 'x-renault-email: your.email@example.com' \
  -H 'x-renault-password: your_password'
```

Voir [API.md](API.md) pour la documentation complete des endpoints.

## Structure du projet

```
renault_backend_bot/
├── api.py                   # Application FastAPI (routes, modeles, gestion d'erreurs)
├── myrenault/
│   ├── __init__.py
│   ├── client.py            # MyRenaultClient (logique metier, cache, monitoring)
│   └── utils.py             # Utilitaires (barre de progression)
├── static/
│   └── index.html           # Interface web de test
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Tests unitaires pytest
├── Dockerfile               # Image Docker (Python 3.12-slim)
├── docker-compose.yml       # Orchestration Docker
├── requirements.txt         # Dependances Python
├── .env.example             # Template variables d'environnement
├── API.md                   # Documentation API detaillee
└── PLAN_ANDROID.md          # Plan application Android
```

## Roadmap

### Fonctionnalites a venir

- [ ] **Application Android** : app native Kotlin + Jetpack Compose (voir [PLAN_ANDROID.md](PLAN_ANDROID.md))
- [ ] **Wear OS** : app companion pour montres connectees
- [ ] **Programmation de charge** : definir des horaires de charge via l'API
- [ ] **Notifications push** : alertes batterie via Firebase
- [ ] **Historique de charge** : stocker et consulter l'historique des sessions de charge
- [ ] **Widget Android** : widget home screen affichant batterie et autonomie
- [ ] **Carte interactive** : affichage de la localisation sur une carte dans l'interface web

### Ameliorations techniques

- [ ] **Pipeline CI/CD** : GitHub Actions pour linting, tests et deploiement automatique
- [ ] **Couverture de tests** : tests supplementaires (timeouts, erreurs upstream, multi-comptes, cache)
- [ ] **Cache de sessions Renault** : reutiliser les sessions API pour reduire les appels login
- [ ] **Logs structures** : logging JSON pour meilleure observabilite
- [ ] **Rate limiting** : protection contre les abus et les appels excessifs
- [ ] **Documentation OpenAPI** : enrichir les schemas FastAPI avec descriptions et exemples
- [ ] **Health check endpoint** : `GET /health` pour monitoring et orchestration Docker
- [ ] **Support HTTPS** : configuration TLS pour deploiements production
- [ ] **Gestion des tokens** : mise en cache et refresh automatique des tokens Renault

### Fait

- [x] API REST stateless avec FastAPI
- [x] Authentification par headers HTTP
- [x] Fallback variables d'environnement
- [x] Liste des vehicules
- [x] Statut batterie
- [x] Cockpit (kilometrage)
- [x] Localisation GPS
- [x] Controle climatisation (start/stop avec temperature)
- [x] Controle charge (start/stop)
- [x] Alertes vehicule (phares, klaxon)
- [x] Support multi-comptes et multi-utilisateurs
- [x] Optimisation compte unique
- [x] Cache vehicules par VIN
- [x] Monitoring des requetes (decorateur)
- [x] Fix charge-stop pour Zoe Phase 2
- [x] Verification de version renault-api
- [x] Interface web de test
- [x] Modeles de reponse Pydantic
- [x] Conteneurisation Docker + Compose
- [x] Tests unitaires pytest
- [x] Documentation API (API.md)
- [x] Plan application Android (PLAN_ANDROID.md)

## Avertissement

Ce projet utilise une **API non officielle** de Renault. Elle peut changer ou cesser de fonctionner a tout moment sans preavis. Utilisation a vos risques et perils. Les developpeurs ne sont pas affilies a Renault.
