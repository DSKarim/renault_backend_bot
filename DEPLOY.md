# 🚀 Guide de Déploiement et Démarrage

Ce guide vous explique comment configurer, déployer et utiliser le bot Renault Telegram.

## 1. Créer le Bot Telegram

1.  Ouvrez Telegram et cherchez l'utilisateur **@BotFather**.
2.  Lancez la conversation avec `/start`.
3.  Envoyez la commande `/newbot`.
4.  Suivez les instructions :
    *   Donnez un nom à votre bot (ex: "Mon Renault Bot").
    *   Choisissez un nom d'utilisateur (doit finir par `bot`, ex: `MaRenaultZE_bot`).
5.  **BotFather** vous donnera un **Token** (ex: `123456789:ABCdefGHIjklMNOpqrSTUvwxyz`). **Gardez-le précieusement**, c'est votre `TELEGRAM_TOKEN`.

## 2. Trouver votre ID Telegram (`AUTHORIZED_USER_ID`)

Pour sécuriser le bot et empêcher d'autres personnes de contrôler votre voiture, vous devez autoriser uniquement votre ID Telegram.

1.  Cherchez le bot **@userinfobot** sur Telegram.
2.  Envoyez n'importe quel message (ou `/start`).
3.  Il vous répondra avec votre `Id` (ex: `123456789`). C'est votre `AUTHORIZED_USER_ID`.

## 3. Installation sur un Serveur (VPS, Raspberry Pi, PC Local)

### Pré-requis
*   Python 3.9 ou supérieur.
*   Accès internet.

### Installation

1.  **Récupérez le code** :
    ```bash
    git clone <votre-repo-url>
    cd <dossier-du-repo>
    ```

2.  **Créez un environnement virtuel** (recommandé) :
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Sur Linux/Mac
    # venv\Scripts\activate   # Sur Windows
    ```

3.  **Installez les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration** :
    Copiez le fichier d'exemple et éditez-le :
    ```bash
    cp .env.example .env
    nano .env  # ou utilisez votre éditeur préféré
    ```
    Remplissez les champs :
    *   `TELEGRAM_TOKEN` : Le token reçu de BotFather.
    *   `AUTHORIZED_USER_ID` : Votre ID Telegram.
    *   `RENAULT_EMAIL` : Votre email de compte My Renault.
    *   `RENAULT_PASSWORD` : Votre mot de passe My Renault.
    *   `VEHICLE_VIN` : Le numéro de série (VIN) de votre voiture (dispo dans l'app My Renault ou sur la carte grise).

## 4. Démarrage

### Lancement manuel
```bash
python bot.py
```
Si tout va bien, le terminal affichera `🤖 Bot démarré...`.

### Lancement en arrière-plan (Linux/Mac)
Pour que le bot continue de tourner après la fermeture du terminal :
```bash
nohup python bot.py > bot.log 2>&1 &
```

### Lancement automatique (Systemd - Linux/Raspberry Pi)
Pour que le bot se lance au démarrage du serveur :

1.  Créez un fichier de service :
    ```bash
    sudo nano /etc/systemd/system/renaultbot.service
    ```

2.  Collez le contenu suivant (adaptez les chemins `User` et `WorkingDirectory`) :
    ```ini
    [Unit]
    Description=Renault Telegram Bot
    After=network.target

    [Service]
    User=pi  # Votre nom d'utilisateur linux
    WorkingDirectory=/home/pi/renault-bot
    ExecStart=/home/pi/renault-bot/venv/bin/python bot.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

3.  Activez et lancez le service :
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable renaultbot
    sudo systemctl start renaultbot
    ```

## 5. Utilisation

Ouvrez votre bot dans Telegram et envoyez `/start` ou `/help` pour voir les commandes.

*   `/etat` : Vérifier la batterie.
*   `/clim_on` : Allumer la clim.
*   `/map` : Voir où est la voiture.

## ❓ Problèmes courants

*   **Erreur d'authentification** : Vérifiez email/mot de passe. Renault bloque parfois les comptes après trop de tentatives échouées.
*   **Pas de réponse** : Vérifiez que le bot tourne (`ps aux | grep python`). Vérifiez les logs.
*   **"Missing environment variables"** : Vous avez oublié de remplir le fichier `.env` ou de le renommer.
