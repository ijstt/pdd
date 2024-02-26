import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import keyboard as kb
from db import Database

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()

bot = Bot(token=config.API)
dp = Dispatcher(bot, storage=storage)
db = Database("pdd.db")


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    id = message.from_user.id
    if not db.user_exists(id):
        db.add_user(id)
        db.set_nickname(id, message.from_user.full_name)
        db.set_ans("0", id)
        await bot.send_message(id,
                               "Привет, я твой чат-бот по Правилам Дорожного Движения!",
                               reply_markup=kb.menu)
    else:
        await bot.send_message(id,
                               f"Привет {db.get_nickname(id)}!",
                               reply_markup=kb.menu)


@dp.message_handler(text=['Профиль'])
async def profile(message: types.Message):
    id = message.from_user.id
    await bot.send_message(id,
                           text=f"Ваш ник - {db.get_nickname(id)}\n"
                                f"Количество правильных ответов - {db.get_ans(id)}/8")


@dp.message_handler(text=['Справочник'])
async def info(message: types.Message):
    id = message.from_user.id
    text = db.get_info()
    await bot.send_message(id,
                           "\n\n".join(text[:5]),
                           reply_markup=kb.txt1)


@dp.callback_query_handler(lambda x: x.data == "next")
async def next(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await bot.delete_message(id, callback_query.message.message_id)
    text = db.get_info()
    await bot.send_message(id,
                           "\n\n".join(text[5:]),
                           reply_markup=kb.txt2)


@dp.callback_query_handler(lambda x: x.data == "back")
async def back(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await bot.delete_message(id, callback_query.message.message_id)
    text = db.get_info()
    await bot.send_message(id,
                           "\n\n".join(text[:5]),
                           reply_markup=kb.txt1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
