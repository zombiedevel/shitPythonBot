from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import ChatNotFound

from database.models.user import GetActiveCount, GetActiveUsers

admins = ["783510790", "861144347"]


class Admin(StatesGroup):
    waite_photo = State()
    waite_text = State()
    waite_button_text = State()
    waite_url = State()


async def admin_cmd(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Создать рассылку", "Статистика"]
    keyboard.add(*buttons)
    await message.answer("Admin mode", reply_markup=keyboard)


async def stat_cmd(message: types.Message):
    active_count = GetActiveCount()
    await message.answer(f"Статистика\nАктивные пользователи: {active_count}")


async def messaging_cmd(message: types.Message):
    await message.answer("Пожалуйста, отправьте изображение.")
    await Admin.waite_photo.set()


async def photo_handler(message: types.Message, state: FSMContext):
    await state.update_data(file_id=message.photo[-1].file_id)
    await message.answer("Пожалуйста, отправьте текст сообщения:")
    await Admin.waite_text.set()


async def text_handler(message: types.Message, state: FSMContext):
    await state.update_data(text_msg=message.text)
    await message.answer("Пожалуйста, отправьте название кнопки:")
    await Admin.waite_button_text.set()


async def text_button_handler(message: types.Message, state: FSMContext):
    await state.update_data(button_text=message.text)
    await message.answer("Пожалуйста, отправьте url кнопки:")
    await Admin.waite_url.set()


async def url_handler(message: types.Message, state: FSMContext):
    await state.update_data(button_url=message.text)
    data = await state.get_data()
    from bot import bot
    buttons = [
        types.InlineKeyboardButton(text=data["button_text"], url=data["button_url"]),
        types.InlineKeyboardButton(text="Начать рассылку", callback_data="start_messaging")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await bot.send_photo(message.from_user.id, data["file_id"], data["text_msg"], reply_markup=keyboard)


async def start_messaging_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Начинаю рассылку...")
    users = GetActiveUsers()

    for i, user in enumerate(users, start=1):
        print(f"{i} out of {len(users)}")
        await send_to_user(state, user)


    await call.message.answer("Рассылка завершена")


async def send_to_user(state: FSMContext, user):
    data = await state.get_data()
    from bot import bot
    buttons = [
        types.InlineKeyboardButton(text=data["button_text"], url=data["button_url"])
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    try:
        await bot.send_photo(user.telegramId, data["file_id"], data["text_msg"], reply_markup=keyboard)
    except ChatNotFound:
        print("ChatNotFound")
        return


def register_handlers_admin(dp: Dispatcher):
    is_admin = filters.IDFilter(user_id=admins)
    dp.register_message_handler(admin_cmd, is_admin, commands=["admin"])
    dp.register_message_handler(stat_cmd, filters.Text(equals="Статистика", ignore_case=True),
                                is_admin)
    dp.register_message_handler(messaging_cmd, filters.Text(equals="Создать рассылку", ignore_case=True),
                                is_admin)
    dp.register_message_handler(photo_handler, is_admin, content_types=['photo'], state=Admin.waite_photo)
    dp.register_message_handler(text_handler, is_admin, state=Admin.waite_text)
    dp.register_message_handler(text_button_handler, is_admin, state=Admin.waite_button_text)
    dp.register_message_handler(url_handler, is_admin, state=Admin.waite_url)
    dp.register_callback_query_handler(start_messaging_handler, is_admin, text="start_messaging", state="*")
