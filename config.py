import os

from aiogram.bot.api import TelegramAPIServer

TOKEN = os.getenv("BOT_TOKEN", "")
API_SERVER = TelegramAPIServer.from_base(os.getenv("API_SERVER", "https://api.telegram.org"))

# Database configuration

DB_HOST = 'mysql'
DB_USER = 'docker'
DB_PASS = 'docker'
DB_NAME = 'cryptodb'


