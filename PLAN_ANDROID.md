# Plan : Application Android Renault

Application Android native pour interagir avec le backend MyRenault API.

## Architecture

| Composant | Technologie |
|---|---|
| Langage | Kotlin |
| UI | Jetpack Compose (single Activity) |
| Reseau | Retrofit + OkHttp |
| Stockage securise | EncryptedSharedPreferences |
| Architecture | MVVM + StateFlow |

## Ecrans prevus

### 1. Ecran de login
- Champs : email, mot de passe, VIN
- Stockage securise des identifiants (EncryptedSharedPreferences)
- Les identifiants sont renvoyes dans les headers de chaque requete (API stateless)

### 2. Dashboard principal
- **Batterie** : niveau (%), autonomie (km), statut de charge, statut prise
- **Cockpit** : kilometrage total
- **Localisation** : latitude/longitude (texte)
- Bouton "Actualiser" pour relancer les requetes

### 3. Commandes a distance
- Boutons d'action en bas de l'ecran :
  - Demarrer / Arreter climatisation
  - Demarrer / Arreter charge
  - Clignoter phares
  - Klaxonner
- Toast de confirmation succes/echec

## Etapes de developpement

### Phase 1 : Configuration du projet
- Creer un projet "Empty Compose Activity"
- Dependances `build.gradle` :
  - `retrofit` + `converter-gson`
  - `okhttp` + `logging-interceptor`
  - `androidx.security:security-crypto`

### Phase 2 : Couche reseau
- Interface Retrofit `RenaultService` mappant les endpoints de [API.md](API.md) :
  - `GET /api/v1/vehicles`
  - `GET /api/v1/vehicle/{vin}/battery`
  - `GET /api/v1/vehicle/{vin}/cockpit`
  - `GET /api/v1/vehicle/{vin}/location`
  - `POST /api/v1/vehicle/{vin}/hvac-start`
  - `POST /api/v1/vehicle/{vin}/hvac-stop`
  - `POST /api/v1/vehicle/{vin}/charge-start`
  - `POST /api/v1/vehicle/{vin}/charge-stop`
  - `POST /api/v1/vehicle/{vin}/lights`
  - `POST /api/v1/vehicle/{vin}/honk`
- `OkHttpClient` avec `Interceptor` ajoutant automatiquement les headers auth

### Phase 3 : Ecran de login
- UI Compose avec champs texte et bouton connexion
- Sauvegarde des identifiants dans EncryptedSharedPreferences
- Navigation vers le dashboard

### Phase 4 : Dashboard et donnees
- Appels GET au demarrage (batterie, cockpit, localisation)
- Affichage des donnees avec gestion des etats (loading, success, error)
- Pull-to-refresh

### Phase 5 : Commandes
- Boutons POST pour les actions a distance
- Feedback utilisateur (Toast / Snackbar)
- Confirmation avant actions critiques (klaxon)

### Phase 6 (future) : Ameliorations
- Selection du vehicule si plusieurs VINs
- Widget home screen (batterie + autonomie)
- Notifications push (batterie faible, charge terminee)
- Support Wear OS
- Carte interactive pour la localisation
- Theme sombre
