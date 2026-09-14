import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is missing.")