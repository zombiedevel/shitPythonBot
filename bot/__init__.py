import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN, API_SERVER
from handlers.admin import register_handlers_admin

from handlers.convertor import register_handlers_convertor

from handlers.inline import register_inline

from datetime import datetime
# Configure logging
now = datetime.now()
dt = now.strftime("%d-%m-%Y %H:%M:%S")
logging.basicConfig(level=logging.INFO,
                    #filename=f"logs/{dt}.log",
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p'
                    )

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, server=API_SERVER)
dp = Dispatcher(bot, storage=MemoryStorage())

register_handlers_convertor(dp)

register_inline(dp)

