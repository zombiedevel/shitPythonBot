import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup
from sqlalchemy.exc import IntegrityError

import api
from database import session
from database.models.directions import Directions, SaveDirection
from database.models.user import User
from handlers.admin import register_handlers_admin

available_crypto_symbols = ['BTC', 'ETH', 'DOGE', 'ADA', 'XRP']
available_bank_symbols = ['USD', 'EUR', 'RUB', 'GBP', 'UAH']


class Convertor(StatesGroup):
    waiting_crypto_symbol = State()
    waiting_bank_symbol = State()
    waiting_count = State()


def inline_directions_buttons():
    result = session.query(Directions).all()
    keyboard = types.InlineKeyboardMarkup()
    for item in result[:10]:
        keyboard.add(types.InlineKeyboardButton(text=item.Direction, callback_data=item.Direction))
    return keyboard


def keyboard_symbols():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons_crypto = [symbol for symbol in available_crypto_symbols]
    buttons_bank = [symbol for symbol in available_bank_symbols]
    keyboard.add(*buttons_crypto)
    keyboard.add(*buttons_bank)
    return keyboard


def keyboard_number():
    keyboard: ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for number in [100, 200, 300, 0.005]:
        keyboard.add(str(number))
    keyboard.add("На главную")
    return keyboard


async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[symbol for symbol in available_crypto_symbols])
    user = User(
        telegramId=message.from_user.id,
        username=message.from_user.username,
        firstName=message.from_user.first_name,
        lastName=message.from_user.last_name,
        status=True
    )

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        print("Duplicate user telegram id")
    finally:
        session.close()
    await message.answer("Выберите символ 1 на клавиатуре.", reply_markup=keyboard)
    await message.answer("Топ направлений", reply_markup=inline_directions_buttons())
    await Convertor.waiting_crypto_symbol.set()


async def convert(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sym_from = data["sym_from"]
    sym_to = data["sym_to"]
    SaveDirection(sym_from, sym_to)
    try:
        count = float(message.text)
    except ValueError:
        await message.answer("Вы точно отправили число? Попробуйте ещё раз.")
        await Convertor.waiting_count.set()
        return

    result = api.Convert(api.getCurrency(sym_from, sym_to), count)
    await message.answer(f"{sym_from} {sym_to} = {result} {sym_to}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


# Start bot and select crypto symbol
async def crypto_symbol_select(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[symbol for symbol in available_bank_symbols])
    if message.text.upper() not in available_crypto_symbols:
        await message.answer("Пожалуйста, выберите криптовалюту или введите символ.")
        await Convertor.waiting_crypto_symbol.set()
        return
    await message.answer("Пожалуйста, выберите валюту, используя клавиатуру ниже.", reply_markup=keyboard)
    await state.update_data(sym_from=message.text.upper())
    await Convertor.next()


async def bank_symbol_select(message: types.Message, state: FSMContext):
    if message.text.upper() not in available_bank_symbols:
        await message.answer("Пожалуйста, выберите валюту, используя клавиатуру ниже.",
                             reply_markup=keyboard_symbols())
        await Convertor.waiting_bank_symbol.set()
        return
    await state.update_data(sym_to=message.text.upper())

    await message.answer("Отправьте сумму конвертации (Пример: 0.005 или целое число):", reply_markup=keyboard_number())
    await Convertor.waiting_count.set()


async def inline_directions_handler(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("-", 1)
    await state.update_data(sym_from=data[0])
    await state.update_data(sym_to=data[1])
    await call.message.answer("Отправьте сумму конвертации (Пример: 0.005 или целое число):")
    await Convertor.waiting_count.set()
    await call.answer(call.data)


def register_handlers_convertor(dp: Dispatcher):
    register_handlers_admin(dp)
    # dp.register_message_handler(convert_ontext, regexp="^[\w]{3,4}\-[\w]{3,4}$")
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(convert, state=Convertor.waiting_count)
    dp.register_message_handler(crypto_symbol_select, state=Convertor.waiting_crypto_symbol)
    dp.register_message_handler(bank_symbol_select, state=Convertor.waiting_bank_symbol)
    dp.register_callback_query_handler(inline_directions_handler, regexp="^[\w]{3,4}\-[\w]{3,4}$", state="*")
