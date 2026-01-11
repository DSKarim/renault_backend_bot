# Documentation de l'API Renault Wrapper

Cette API sert de passerelle (wrapper) vers les services MyRenault. Elle simplifie l'interaction en gérant l'authentification de session à chaque requête.

## Base URL
L'URL de base dépend du déploiement. Pour le développement local :
`http://localhost:8000`

## Authentification
L'API ne possède pas d'endpoint de "login" persistent qui retourne un token. Au lieu de cela, chaque requête vers les endpoints protégés (`/api/v1/*`) doit inclure les identifiants Renault de l'utilisateur dans les headers HTTP.

**Headers Requis :**
*   `x-renault-email`: L'adresse email du compte MyRenault.
*   `x-renault-password`: Le mot de passe du compte MyRenault.

## Endpoints

### 0. Liste des Véhicules

#### Obtenir la liste des véhicules
Retourne la liste des véhicules associés au compte utilisateur.

*   **URL** : `/api/v1/vehicles`
*   **Méthode** : `GET`
*   **Headers** : Auth headers requis.

### 1. Informations Véhicule

#### Obtenir le statut de la batterie
Retourne le niveau de charge, l'autonomie, et le statut de branchement.

*   **URL** : `/api/v1/vehicle/{vin}/battery`
*   **Méthode** : `GET`
*   **URL Params** : `vin` (Vehicle Identification Number)
*   **Headers** : Auth headers requis.

#### Obtenir les infos du cockpit
Retourne le kilométrage total et le niveau de carburant (si hybride).

*   **URL** : `/api/v1/vehicle/{vin}/cockpit`
*   **Méthode** : `GET`
*   **URL Params** : `vin`
*   **Headers** : Auth headers requis.

#### Obtenir la localisation
Retourne les coordonnées GPS du véhicule.

*   **URL** : `/api/v1/vehicle/{vin}/location`
*   **Méthode** : `GET`
*   **URL Params** : `vin`
*   **Headers** : Auth headers requis.

---

### 2. Commandes à Distance (Actions)

#### Démarrer la climatisation (HVAC)
Lance la pré-climatisation du véhicule.

*   **URL** : `/api/v1/vehicle/{vin}/hvac-start`
*   **Méthode** : `POST`
*   **URL Params** : `vin`
*   **Query Params** :
    *   `temp` (float, optionnel) : La température cible (défaut: 21.0).
*   **Headers** : Auth headers requis.

#### Arrêter la climatisation (HVAC)
*   **URL** : `/api/v1/vehicle/{vin}/hvac-stop`
*   **Méthode** : `POST`
*   **URL Params** : `vin`
*   **Headers** : Auth headers requis.

#### Démarrer la charge
*   **URL** : `/api/v1/vehicle/{vin}/charge-start`
*   **Méthode** : `POST`
*   **URL Params** : `vin`
*   **Headers** : Auth headers requis.

#### Arrêter la charge
*   **URL** : `/api/v1/vehicle/{vin}/charge-stop`
*   **Méthode** : `POST`
*   **URL Params** : `vin`
*   **Headers** : Auth headers requis.

#### Faire clignoter les phares
*   **URL** : `/api/v1/vehicle/{vin}/lights`
*   **Méthode** : `POST`
*   **URL Params** : `vin`
*   **Headers** : Auth headers requis.

#### Klaxonner
*   **URL** : `/api/v1/vehicle/{vin}/honk`
*   **Méthode** : `POST`
*   **URL Params** : `vin`
*   **Headers** : Auth headers requis.

## Gestion des Erreurs
L'API utilise les codes HTTP standards pour indiquer le type d'erreur :

*   **401 Unauthorized** : Identifiants invalides ou refusés par l'API Renault.
*   **404 Not Found** : Le VIN spécifié est introuvable.
*   **502 Bad Gateway** : Erreur provenant de l'API Renault (ex: service indisponible, réponse inattendue).
*   **504 Gateway Timeout** : La requête vers l'API Renault a expiré (timeout).
*   **500 Internal Server Error** : Erreur interne inattendue.

Le corps de la réponse JSON contient généralement un champ `detail` expliquant l'erreur.
