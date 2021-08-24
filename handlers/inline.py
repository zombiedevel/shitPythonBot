import logging

from aiogram import types, Dispatcher

import api
from handlers.convertor import available_bank_symbols


async def inline_handler(query: types.InlineQuery):
    q = query.query.split(" ", 1)
    if len(q) != 2:
        return

    try:
        count = float(q[1])
    except ValueError:
        return

    print("Ok")
    if not q[0].upper() in available_bank_symbols:
        print("Wrong symbol")
        return

    d = api.getTopSymbols(q[0].upper(), 19)
    symbols = [types.InlineQueryResultArticle(
        id=item["CoinInfo"]["Id"],
        title=item["CoinInfo"]["FullName"],
        description=f"{count} {q[0].upper()} = "
                    f"{round(float(count / item['RAW'][q[0].upper()]['PRICE']), 4)} {item['CoinInfo']['Name']}",
        thumb_url=f"https://www.cryptocompare.com{item['CoinInfo']['ImageUrl']}",
        input_message_content=types.InputTextMessageContent(
            message_text=f"{count} {q[0].upper()} = {float(count / item['RAW'][q[0].upper()]['PRICE'])} {item['CoinInfo']['Name']}",
            parse_mode="HTML"
        ),
    ) for item in d["Data"]]

    await query.answer(symbols, cache_time=60, is_personal=True,
                       switch_pm_text="Другие направления >>>", switch_pm_parameter="convert")

def register_inline(dp: Dispatcher):
    dp.register_inline_handler(inline_handler)
