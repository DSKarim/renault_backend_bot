import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from myrenault.client import MyRenaultClient
from myrenault.monitor import BatteryMonitor
from myrenault.utils import get_progress_bar

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

# Verify environment variables
required_env = ["TELEGRAM_TOKEN", "AUTHORIZED_USER_ID", "VEHICLE_VIN", "RENAULT_EMAIL", "RENAULT_PASSWORD"]
missing_env = [key for key in required_env if key not in os.environ]
if missing_env:
    raise EnvironmentError(f"Missing environment variables: {', '.join(missing_env)}")

TOKEN = os.environ["TELEGRAM_TOKEN"]
USER_ID = int(os.environ["AUTHORIZED_USER_ID"])
VIN = os.environ["VEHICLE_VIN"].strip()

client = MyRenaultClient()

def restricted(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != USER_ID:
            return
        return await func(update, context)
    return wrapper

@restricted
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🔄 Récupération des données...")

        # Ensure vehicle is cached to avoid race conditions in parallel fetching
        await client.get_vehicle(VIN)

        # Fetch data in parallel to reduce wait time
        bat, cockpit = await asyncio.gather(
            client.battery_status(VIN),
            client.cockpit(VIN)
        )

        # Format response
        level = bat.get('batteryLevel', '?')
        range_km = bat.get('batteryAutonomy', '?')
        charging = bat.get('chargingStatus', '?')
        plugged = bat.get('plugStatus', '?')
        temp = bat.get('batteryTemperature', '?')
        power = bat.get('chargingInstantaneousPower', '?')
        total_km = cockpit.get('totalMileage', '?')
        timestamp = bat.get('timestamp', '')

        # Format timestamp if available
        time_str = ""
        if timestamp:
            try:
                # Basic ISO format handling or string display
                # If it's a string like '2023-10-27T10:00:00Z', we can make it prettier
                # For now, just displaying it as is or replacing T with space
                time_str = f"\n🕒 <b>Date:</b> {timestamp.replace('T', ' ')}"
            except Exception:
                time_str = f"\n🕒 <b>Date:</b> {timestamp}"

        # Visual progress bar for battery
        bar = get_progress_bar(level)

        msg = (
            f"🔋 <b>Batterie:</b> {bar} {level}%\n"
            f"🚗 <b>Autonomie:</b> {range_km} km\n"
            f"🌡️ <b>Temp. Batterie:</b> {temp}°C\n"
            f"🛣️ <b>Kilométrage:</b> {total_km} km\n"
            f"⚡ <b>Charge:</b> {charging} (Plug: {plugged})\n"
            f"⚡ <b>Puissance:</b> {power}"
            f"{time_str}"
        )
        await update.message.reply_text(msg, parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

@restricted
async def clim_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🌡️ Lancement de la climatisation (21°C)...")
        await client.hvac_start(VIN, 21)
        await update.message.reply_text("✅ Commande envoyée.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

@restricted
async def clim_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("❄️ Arrêt de la climatisation...")
        await client.hvac_stop(VIN)
        await update.message.reply_text("✅ Commande envoyée.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

@restricted
async def charge_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("⚡ Démarrage de la charge...")
        await client.charge_start(VIN)
        await update.message.reply_text("✅ Commande envoyée.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

@restricted
async def charge_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🛑 Arrêt de la charge...")
        await client.charge_stop(VIN)
        await update.message.reply_text("✅ Commande envoyée.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

@restricted
async def lights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("💡 Faire clignoter les phares...")
        await client.blink_lights(VIN)
        await update.message.reply_text("✅ Commande envoyée.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

@restricted
async def horn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🔊 Klaxonner...")
        await client.honk(VIN)
        await update.message.reply_text("✅ Commande envoyée.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

@restricted
async def map_loc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        loc = await client.location(VIN)
        lat = loc.get("latitude")
        lon = loc.get("longitude")
        if lat and lon:
            await update.message.reply_location(lat, lon)
        else:
            await update.message.reply_text("📍 Position inconnue.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")

@restricted
async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = client.get_stats()
    current_ver, latest_ver = await client.check_api_version()

    msg = (
        "📊 <b>Statistiques du bot</b>\n"
        f"⏱️ <b>Uptime:</b> {stats['uptime']}\n"
        f"🔢 <b>Requêtes totales:</b> {stats['requests_total']}\n"
        f"✅ <b>Succès:</b> {stats['requests_success']}\n"
        f"❌ <b>Échecs:</b> {stats['requests_failed']}\n"
        f"💾 <b>Cache véhicules:</b> {stats['cache_size']}\n\n"
        "📦 <b>Renault API</b>\n"
        f"🔹 Installée: {current_ver}\n"
        f"🔸 Disponible: {latest_ver}"
    )
    await update.message.reply_text(msg, parse_mode="HTML")

@restricted
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🤖 <b>Commandes disponibles :</b>

🚗 <b>Contrôle du véhicule :</b>
/etat - État de la batterie et kilométrage
/clim_on - Démarrer la clim (21°C)
/clim_off - Arrêter la clim
/charge_on - Démarrer la charge
/charge_off - Arrêter la charge
/lights - Faire clignoter les phares
/horn - Klaxonner
/map - Position GPS du véhicule

ℹ️ <b>Information :</b>
/debug - Statistiques techniques
/help - Afficher ce message
    """
    await update.message.reply_text(help_text, parse_mode="HTML")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("etat", status))
    app.add_handler(CommandHandler("clim_on", clim_on))
    app.add_handler(CommandHandler("clim_off", clim_off))
    app.add_handler(CommandHandler("charge_on", charge_on))
    app.add_handler(CommandHandler("charge_off", charge_off))
    app.add_handler(CommandHandler("lights", lights))
    app.add_handler(CommandHandler("horn", horn))
    app.add_handler(CommandHandler("map", map_loc))
    app.add_handler(CommandHandler("debug", debug))
    app.add_handler(CommandHandler("start", help_cmd))
    app.add_handler(CommandHandler("help", help_cmd))

    # Monitor Job
    monitor = BatteryMonitor(client, VIN, USER_ID)
    # Check every 5 minutes (300s)
    app.job_queue.run_repeating(monitor.check_battery, interval=300, first=10)

    print("🤖 Bot démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
