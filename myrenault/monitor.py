from telegram.ext import ContextTypes
from myrenault.utils import get_progress_bar

class BatteryMonitor:
    def __init__(self, client, vin, user_id):
        self.client = client
        self.vin = vin
        self.user_id = user_id
        self.last_level = None

    async def check_battery(self, context: ContextTypes.DEFAULT_TYPE):
        try:
            d = await self.client.battery_status(self.vin)

            lvl = d.get("batteryLevel")

            # Simple logic
            if lvl is None:
                return

            if self.last_level is not None:
                # Notify if drops below 20
                if lvl <= 20 and self.last_level > 20:
                    bar = get_progress_bar(lvl)
                    await context.bot.send_message(chat_id=self.user_id, text=f"⚠️ Batterie faible : {bar} {lvl}%")

                # Notify if reaches 80 while charging (assuming status != 0 means charging, or we track increase)
                if lvl >= 80 and self.last_level < 80:
                     bar = get_progress_bar(lvl)
                     await context.bot.send_message(chat_id=self.user_id, text=f"✅ Batterie chargée à {bar} {lvl}%")

            self.last_level = lvl

        except Exception as e:
            print(f"Monitor Error: {e}")
