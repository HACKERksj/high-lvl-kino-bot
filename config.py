import os

# =============================================
# 🔧 CONFIGURATION — config.py
# =============================================

# Bot token (@BotFather dan oling)
BOT_TOKEN = "8574253263:AAFcCyuC__4qwao0lBOOGl9f0G9cNmWBRvM"
# Sizning Telegram ID (admin)
ADMIN_ID = int(os.getenv("ADMIN_ID", "7779605930"))

# Kino saqlanadigan channel username yoki ID
# Masalan: "@mymoviechannel" yoki -1001234567890
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1004299804429")

# SQLite database fayl nomi
DATABASE_PATH = os.getenv("DATABASE_PATH", "database.sqlite")

# Premium kino kodlari prefix (masalan: "P001")
PREMIUM_PREFIX = "P"

# Referral bonus (nechta taklif qilsa premium oladi)
REFERRAL_THRESHOLD = 5

# Cache yangilanish vaqti (soniyalarda)
CACHE_TTL = 3600  # 1 soat

# Reklama xabari (bo'sh qoldiring agar kerak bo'lmasa)
AD_MESSAGE = ""  # Masalan: "🔥 @our_channel ga obuna bo'ling!"
