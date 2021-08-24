from aiogram import executor

import api
from bot import dp
from database import engine, Base, users

if __name__ == '__main__':
    Base.create_all(engine)
    executor.start_polling(dp, skip_updates=True) # Run bot
