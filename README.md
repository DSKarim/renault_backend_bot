# 🚗 Renault Telegram Bot

Bot Telegram personnel pour piloter une Renault électrique (ZOE, Megane E-Tech, Twingo ZE, etc.)
via l'API non officielle My Renault.

Ce projet permet d'interagir avec votre véhicule directement depuis Telegram pour obtenir des informations en temps réel et lancer des actions à distance.

## ✨ Fonctions Actuelles
- **🔋 État batterie & autonomie** : Consultez le pourcentage de batterie, l'autonomie restante et le statut de charge (`/etat`).
- **🛣️ Kilométrage** : Affiche le kilométrage total du véhicule.
- **🌡️ Climatisation** :
    - Démarrage à distance (`/clim_on`) (préréglé à 21°C).
    - Arrêt (`/clim_off`) (annule la programmation).
- **📍 Localisation** : Affiche la position GPS du véhicule sur une carte (`/map`).
- **🔔 Monitoring** : Vérification automatique toutes les 5 minutes.
    - Alerte si batterie faible (< 20%).
    - Alerte si charge atteinte (>= 80%).

## 🚀 Prochaines Étapes
- [ ] **Programmation de charge** : Ajouter la possibilité de définir des plages horaires de charge.
- [ ] **Historique** : Sauvegarder les données de charge dans une base de données (SQLite/CSV).
- [ ] **Gestion Multi-véhicules** : Supporter plusieurs VINs sur le même compte.
- [ ] **Notifications plus fines** : Configurer les seuils d'alerte via Telegram.

## 📱 Développement Mobile / API
Vous souhaitez utiliser ce code comme backend pour une application Android ou iOS ?
Consultez le guide dédié : [README_BACKEND.md](README_BACKEND.md)

## 🛠️ Installation & Démarrage

Voir le guide de déploiement complet : [DEPLOY.md](DEPLOY.md)

### En résumé :

1.  **Cloner le repo**
2.  **Installer les dépendances** : `pip install -r requirements.txt`
3.  **Configurer** : Renommer `.env.example` en `.env` et remplir les infos.
4.  **Lancer** : `python bot.py`

## 📚 Fonctionnalités disponibles via la librairie `renault-api`

La librairie sous-jacente [renault-api](https://github.com/hacf-fr/renault-api) permet d'accéder à de nombreuses informations et actions. Voici une liste non exhaustive des capacités techniques offertes par l'API, indépendamment de ce qui est implémenté actuellement dans ce bot.

### Lecture de données
- **Batterie** : Niveau de charge (%), autonomie (km), statut de branchement, statut de charge (en cours, erreur, etc.), temps restant.
- **Cockpit** : Kilométrage total, autonomie carburant (pour hybrides).
- **Localisation** : Position GPS du véhicule (si activé dans le véhicule).
- **Climatisation (HVAC)** : Statut de la climatisation, température extérieure (selon modèles).
- **Charge** : Historique des charges, calendrier de charge, mode de charge.
- **Alertes** : Avertissements du tableau de bord (pression pneus, airbag, etc.).
- **Verrouillage** : État des portes et du coffre (ouvert/fermé/verrouillé) (selon modèles).
- **Pression des pneus** : Pression détaillée par pneu (selon modèles).

### Actions à distance
- **Charge** : Démarrer/Arrêter la charge, changer le mode (immédiat/programmé).
- **Climatisation** : Démarrer/Arrêter le pré-conditionnement, définir le planning.
- **Avertisseurs** : Faire clignoter les phares, faire clignoter les phares + klaxonner (pour retrouver le véhicule).

---

## 📌 Spécificités & Compatibilité Zoe Phase 2 (Zoe50 / Model X102VE)

La **Renault Zoe Phase 2 (produite après mi-2019)** dispose d'une architecture plus moderne que la Phase 1 (Zoe40), mais certaines remontées d'informations comportent des particularités ou limitations connues via l'API.

| Fonctionnalité | Support Zoe Ph2 | Notes spécifiques |
| :--- | :---: | :--- |
| **État Batterie** | ✅ | `batteryTemperature` remonte souvent des valeurs incorrectes. `chargingInstantaneousPower` (puissance instantanée) peut être erroné. |
| **Démarrage Charge** | ✅ | Supporté (`/charge_on`, `/charge_off`). |
| **Démarrage Clim** | ✅ | Supporté (`/clim_on`). Note : L'action "Annuler" (`/clim_off`) est envoyée mais souvent ignorée par le véhicule (limitation Renault). |
| **Statut Clim** | ❌ | Le endpoint `hvac-status` renvoie souvent une erreur ou n'est pas supporté. On ne peut pas facilement savoir si la clim tourne. |
| **Localisation** | ✅ | Fonctionne correctement. |
| **Kilométrage** | ✅ | Remonte via le module "Cockpit". |
| **Mode Charge** | ⚠️ | La lecture du mode remonte `always` ou `scheduled`, ce qui diffère légèrement des anciens modèles (`always_charging`). |
| **Klaxon & Phares** | ✅ | Supporté sur la plupart des Zoe50 (contrairement aux Zoe40). |
| **Verrouillage** | ❓ | Dépend de la version précise du véhicule et des options. Souvent non disponible sur Zoe. |

*Ces informations sont basées sur la documentation de la communauté open-source et peuvent évoluer avec les mises à jour des calculateurs Renault.*

## ⚠️ Avertissement
Ce projet utilise une **API non officielle** de Renault. Elle peut changer à tout moment sans préavis.
L'utilisation de ce bot est sous votre entière responsabilité.
