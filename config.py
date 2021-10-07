import os

from aiogram.bot.api import TelegramAPIServer

TOKEN = os.getenv("BOT_TOKEN", "")
API_SERVER = TelegramAPIServer.from_base(os.getenv("API_SERVER", "https://api.telegram.org"))

# Database configuration

DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "docker")
DB_PASS = os.getenv("DB_PASS", "docker")
DB_NAME = os.getenv("DB_NAME", "cryptdb")


