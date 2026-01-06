# Guide de Déploiement Docker

Ce guide explique comment déployer le bot MyRenault sur un serveur utilisant Docker et Docker Compose.

## Prérequis

*   [Docker](https://docs.docker.com/get-docker/) installé.
*   [Docker Compose](https://docs.docker.com/compose/install/) installé.
*   Un compte Renault valide.
*   Un bot Telegram créé via [@BotFather](https://t.me/BotFather) (Token).
*   Votre ID utilisateur Telegram (vous pouvez l'obtenir via [@userinfobot](https://t.me/userinfobot)).
*   Le VIN (Vehicle Identification Number) de votre véhicule.

## Étape 1 : Préparation des fichiers

1.  Clonez ce dépôt ou copiez les fichiers sur votre serveur.
2.  Assurez-vous d'avoir les fichiers suivants dans le même dossier :
    *   `Dockerfile`
    *   `docker-compose.yml`
    *   `bot.py`
    *   `requirements.txt`
    *   Le dossier `myrenault/`

## Étape 2 : Configuration

1.  Créez un fichier `.env` à la racine du projet (vous pouvez copier `.env.example` s'il existe) :
    ```bash
    cp .env.example .env
    ```
2.  Ouvrez le fichier `.env` et remplissez les variables :
    ```env
    TELEGRAM_TOKEN=votre_token_telegram
    AUTHORIZED_USER_ID=votre_id_telegram
    VEHICLE_VIN=votre_vin
    RENAULT_EMAIL=votre_email_renault
    RENAULT_PASSWORD=votre_mot_de_passe_renault
    ```

## Étape 3 : Lancement

Utilisez Docker Compose pour construire et lancer le conteneur en arrière-plan.

```bash
docker-compose up -d --build
```

## Commandes utiles

*   **Voir les logs :**
    ```bash
    docker-compose logs -f
    ```

*   **Arrêter le bot :**
    ```bash
    docker-compose down
    ```

*   **Redémarrer le bot :**
    ```bash
    docker-compose restart
    ```

*   **Mettre à jour :**
    Si vous modifiez le code, reconstruisez l'image :
    ```bash
    docker-compose up -d --build
    ```
