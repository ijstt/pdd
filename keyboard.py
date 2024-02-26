from aiogram import types

menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
profile = types.KeyboardButton("Профиль")
test = types.KeyboardButton("Тест")
info = types.KeyboardButton("Справочник")
menu.add(profile, test, info)

txt1 = types.InlineKeyboardMarkup(row_width=1)
next = types.InlineKeyboardButton("Дальше", callback_data="next")
txt1.add(next)

txt2 = types.InlineKeyboardMarkup(row_width=1)
back = types.InlineKeyboardButton("Назад", callback_data="back")
txt2.add(back)