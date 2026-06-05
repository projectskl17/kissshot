import re
from os import environ

# -------------------------
# Helper
# -------------------------
def str_to_bool(val, default=False):
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes", "on")

# =========================================================
# 🤖 BOT BASIC INFORMATION
# =========================================================
API_ID = int(environ.get("API_ID", "21375775"))
API_HASH = environ.get("API_HASH", "24a8567a7fa9209f79d4643b191c1ae4")
BOT_TOKEN = environ.get("BOT_TOKEN", "8609992751:AAEOw3WiozEHifyDRb6ek5HsVKVvQhg8d0I")
PORT = int(environ.get("PORT", "8011"))
TIMEZONE = environ.get("TIMEZONE", "Asia/Kolkata")
OWNER_USERNAME = environ.get("OWNER_USERNAME", "BOT_OWNER26")

# =========================================================
# 💾 DATABASE CONFIGURATION
# =========================================================
DB_URL = environ.get("DATABASE_URI", "mongodb+srv://ksb1:ksb1@cluster0.wi4snno.mongodb.net/?appName=Cluster0")
DB_NAME = environ.get("DATABASE_NAME", "ksb1")

# =========================================================
# 📢 CHANNELS & ADMINS
# =========================================================
ADMINS = int(environ.get("ADMINS", "6561300746"))

LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1003987598694"))
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", "-1003987598694"))
VERIFIED_LOG = int(environ.get("VERIFIED_LOG", "-1003987598694"))

POST_CHANNEL = int(environ.get("POST_CHANNEL", "0"))
VIDEO_CHANNEL = int(environ.get("VIDEO_CHANNEL", "0"))
BRAZZER_CHANNEL = int(environ.get("BRAZZER_CHANNEL", "0"))

# Auth channels list
auth_channel_str = environ.get("AUTH_CHANNEL", "")
AUTH_CHANNEL = [int(x) for x in auth_channel_str.split() if x.strip().lstrip("-").isdigit()]

# =========================================================
# ⚙️ FEATURES & TOGGLES  (FIXED)
# =========================================================
FSUB = str_to_bool(environ.get("FSUB"), True)
IS_VERIFY = str_to_bool(environ.get("IS_VERIFY"), False)
POST_SHORTLINK = str_to_bool(environ.get("POST_SHORTLINK"), False)
SEND_POST = str_to_bool(environ.get("SEND_POST"), False)
PROTECT_CONTENT = str_to_bool(environ.get("PROTECT_CONTENT"), True)

# =========================================================
# 🔢 LIMITS
# =========================================================
DAILY_LIMIT = int(environ.get("DAILY_LIMIT", "15"))
VERIFICATION_DAILY_LIMIT = int(environ.get("VERIFICATION_DAILY_LIMIT", "20"))
PREMIUM_DAILY_LIMIT = int(environ.get("PREMIUM_DAILY_LIMIT", "50"))

# =========================================================
# 🔗 SHORTLINK & VERIFICATION
# =========================================================
SHORTLINK_URL = environ.get("SHORTLINK_URL", "")
SHORTLINK_API = environ.get("SHORTLINK_API", "")
POST_SHORTLINK_URL = environ.get("POST_SHORTLINK_URL", "")
POST_SHORTLINK_API = environ.get("POST_SHORTLINK_API", "")
VERIFY_EXPIRE = int(environ.get("VERIFY_EXPIRE", "3600"))
TUTORIAL_LINK = environ.get("TUTORIAL_LINK", "")

# =========================================================
# 💳 PAYMENT SETTINGS
# =========================================================
UPI_ID = environ.get("UPI_ID", "")
QR_CODE_IMAGE = environ.get("QR_CODE_IMAGE", "https://graph.org/file/681c4aec0905e108a3da1-030394aef130e14eba.jpg")

# =========================================================
# 🖼️ IMAGES
# =========================================================
START_PIC = environ.get("START_PIC", "https://graph.org/file/681c4aec0905e108a3da1-030394aef130e14eba.jpg")
AUTH_PICS = environ.get("AUTH_PICS", "https://graph.org/file/681c4aec0905e108a3da1-030394aef130e14eba.jpg")
VERIFY_IMG = environ.get("VERIFY_IMG", "https://graph.org/file/681c4aec0905e108a3da1-030394aef130e14eba.jpg")
NO_IMG = environ.get("NO_IMG", "https://graph.org/file/681c4aec0905e108a3da1-030394aef130e14eba.jpg")

# =========================================================
# 🌐 WEB APP
# =========================================================
WEB_APP_URL = environ.get("WEB_APP_URL", "")
