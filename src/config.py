import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
AUTONOMY_LEVEL = os.getenv("AUTONOMY_LEVEL", "assisted")

if not GEMINI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("⚠️ Faltan variables de entorno requeridas: GEMINI_API_KEY o TELEGRAM_BOT_TOKEN.")