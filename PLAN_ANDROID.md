# Plan de Développement : Application Android & Wear OS pour Renault (Google Jules)

Ce document décrit le plan à suivre pour transformer le bot Telegram actuel en une application mobile Android native indépendante, avec une extension pour Wear OS (Google Watch). L'objectif est de permettre à chaque utilisateur de se connecter avec son propre compte Renault, de choisir son véhicule et d'interagir avec lui.

## Architecture

*   **Langage** : Kotlin (Standard Android actuel).
*   **UI** : Jetpack Compose (Moderne, déclaratif, compatible Wear OS).
*   **Architecture** : MVVM (Model-View-ViewModel) + Clean Architecture.
*   **Modularisation** :
    *   `app` (Application téléphone)
    *   `wear` (Application montre)
    *   `shared` (Logique métier commune : API Renault, Authentification, Modèles de données)

---

## Étapes de Développement

### 1. Initialisation du Projet Android
*   Créer un nouveau projet Android dans Android Studio.
*   Configurer deux modules : `app` (Phone) et `wear` (Watch).
*   Créer un module `shared` (Kotlin Multiplatform ou simple module Android Library) pour partager le code critique entre le téléphone et la montre.
*   Configurer Git et l'intégration continue.

### 2. Implémentation de la Couche de Données (Module `shared`)
*   **API Client** : Implémenter les appels HTTP vers l'API Renault (Kamereon/Gigya) en utilisant **Retrofit** et **OkHttp**.
*   **Authentification** : Porter la logique d'authentification Python (`renault-api`) vers Kotlin.
    *   Gestion du flux de login (Email/Mot de passe).
    *   Récupération des tokens (Cookie, PersonID, AccountID).
    *   Stockage sécurisé des tokens avec **EncryptedSharedPreferences**.
*   **Modèles** : Créer les data classes Kotlin pour `BatteryStatus`, `Cockpit`, `Location`, etc.

### 3. Gestion des Comptes et Véhicules
*   Développer l'écran de connexion (Login Screen) dans l'application téléphone.
*   Récupérer la liste des comptes associés à l'utilisateur (`get_api_accounts`).
*   Récupérer la liste des véhicules (`get_vehicles`) et leurs VINs.
*   Permettre à l'utilisateur de sélectionner son véhicule "actif" et sauvegarder ce choix localement.

### 4. Tableau de Bord Principal (Téléphone)
*   Créer l'interface utilisateur (UI) principale affichant :
    *   Niveau de batterie (%) et autonomie (km).
    *   Statut de charge (branché, en charge, etc.).
    *   Kilométrage total.
    *   Dernière mise à jour des données.
*   Implémenter le "Pull-to-refresh" pour actualiser les données.

### 5. Actions à Distance (Commandes)
*   Ajouter des boutons d'action pour piloter le véhicule :
    *   **Climatisation** : Démarrer (`hvac-start`) / Arrêter.
    *   **Charge** : Démarrer / Arrêter.
    *   **Avertisseurs** : Clignotants et Klaxon.
*   Gérer les états de chargement et les retours d'erreur API (Toast/Snackbars).

### 6. Géolocalisation
*   Intégrer **Google Maps SDK** (ou OSMDroid pour une solution libre).
*   Afficher la position du véhicule sur la carte en utilisant les coordonnées GPS (`gpsLatitude`, `gpsLongitude`).

### 7. Préparation et Module Wear OS (App Sœur)
*   Dans le module `wear`, réutiliser la logique du module `shared` pour l'authentification (ou synchroniser le token depuis le téléphone via la **Data Layer API**).
*   Créer une UI simplifiée pour les petits écrans (Tiles & Complications) :
    *   Vue simple : Jauge de batterie + Autonomie.
    *   Actions rapides : Bouton "Clim", Bouton "Ouvrir port de charge" (si dispo).

### 8. Synchronisation et Background Tasks
*   Utiliser **WorkManager** pour actualiser les données périodiquement en arrière-plan (ex: vérifier la batterie toutes les 15 min).
*   Envoyer des notifications locales si la charge est terminée ou si la batterie est faible (remplaçant la logique du bot Telegram).

### 9. Tests et Qualité
*   Écrire des tests unitaires pour la logique API (MockWebServer).
*   Tests UI (Instrumented Tests) pour les parcours critiques (Login, Sélection véhicule).
*   Vérifier la consommation batterie de l'application elle-même.

### 10. Finalisation et Déploiement
*   Générer les APKs/App Bundles signés.
*   Préparer les fiches Play Store (Phone et Watch).
*   Lancement en canal Alpha/Bêta pour tests utilisateurs.
