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


@dp.message_handler(text=['Тест'])
async def quiz(message: types.Message):
    id = message.from_user.id

    if int(db.get_ans(id)) == 0:
        await bot.send_message(id,
                               text="Вы хотите начать тест? У вас будет 1 попытка",
                               reply_markup=kb.quiz)
        await bot.delete_message(message.from_user.id, message.message_id)
    else:
        await bot.send_message(id,
                               text="Вы уже прошли викторину, с вашими баллами вы можете ознакомиться в личном кабинете")


@dp.callback_query_handler(lambda x: x.data == "quiz")
async def quiz(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id

    data = db.get_ques()
    num = int(db.get_tb(id))

    for k, v in data[0].items():
        for j, i in v.items():
            text = f"{k} {j}"
    await bot.send_message(id,
                           text=text,
                           reply_markup=kb.ans)

    db.set_tb(num + 1, callback_query.from_user.id)


@dp.callback_query_handler(lambda x: x.data in "АБВГ")
async def check_quiz(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    s = int(db.get_tb(id))
    data = db.get_ques()
    ans = callback_query.data

    for k, v in data[s].items():
        for j, i in v.items():
            if ans == i:
                db.set_ans(db.get_ans(id) + 1, id)
            text = f"{k} {j}"

        if len(data) != s:
            await bot.send_message(id,
                                   text=text,
                                   reply_markup=kb.ans)
        else:
            await bot.send_message(id,
                                   text="Завершить тест",
                                   reply_markup=kb.end)

    db.set_tb(s + 1, callback_query.from_user.id)


@dp.callback_query_handler(lambda x: x.data == "end")
async def end_que(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    current_ball = db.get_ans(id)
    if current_ball * 100 // 8 >= 66:
        await bot.send_message(callback_query.from_user.id,
                               text="Поздравляем! У вас отличный результат")
    elif 40 <= current_ball * 100 // 8 < 66:
        await bot.send_message(callback_query.from_user.id,
                               text="Неплохой результат, но еще есть к чему стремиться :)")
    else:
        await bot.send_message(callback_query.from_user.id,
                               text="Советуем вам зайди в раздел справочника и изучить теорию по ПДД")
    await bot.send_message(callback_query.from_user.id,
                           text=f"Вы набрали - {current_ball} из 8 баллов")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
