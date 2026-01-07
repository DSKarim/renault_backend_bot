# Plan Simplifié : Application Android Basic Renault

Ce plan vise à créer une application Android minimale et fonctionnelle permettant de se connecter, voir les infos essentielles et envoyer des commandes.

## Architecture Simplifiée
*   **Langage** : Kotlin
*   **UI** : Jetpack Compose (une seule Activity)
*   **Réseau** : Retrofit + OkHttp

## Étapes de Développement

### 1. Configuration du Projet
*   Créer un projet "Empty Compose Activity".
*   Ajouter les dépendances dans `build.gradle` :
    *   `retrofit` & `converter-gson` (pour l'API)
    *   `okhttp` & `logging-interceptor`
    *   `androidx.security:security-crypto` (pour stocker le mot de passe localement)

### 2. Écran de Login (Authentification)
*   Créer un écran avec deux champs texte : `Email` et `Password`.
*   Ajouter un champ texte pour le `VIN` (Vehicle Identification Number) ou le coder en dur pour commencer.
*   Au clic sur "Connexion" :
    *   Sauvegarder les identifiants de manière sécurisée (EncryptedSharedPreferences).
    *   Naviguer vers l'écran principal.
*   *Note : L'API ne fournit pas de token, l'appli doit renvoyer l'email/password dans le header de chaque requête.*

### 3. Couche Réseau (API Client)
*   Définir une interface Retrofit `RenaultService` correspondant à `API.md`.
*   Configurer un `OkHttpClient` avec un `Interceptor` qui ajoute automatiquement les headers :
    *   `x-renault-email`
    *   `x-renault-password`
    (récupérés depuis les préférences sécurisées).

### 4. Écran Principal (Dashboard)
*   Afficher les informations textuelles simples (appels GET) :
    *   **Batterie** : Pourcentage et Autonomie (Endpoint `/battery`).
    *   **Cockpit** : Kilométrage total (Endpoint `/cockpit`).
    *   **Localisation** : Latitude/Longitude (texte simple) (Endpoint `/location`).
*   Ajouter un bouton "Actualiser" pour relancer les requêtes.

### 5. Commandes (Actions)
*   Ajouter des boutons simples en bas de l'écran principal pour les appels POST :
    *   [Démarrer Clim] / [Arrêter Clim]
    *   [Démarrer Charge] / [Arrêter Charge]
    *   [Phares] / [Klaxon]
*   Afficher un "Toast" (message temporaire) pour confirmer le succès ou l'échec de la commande.
