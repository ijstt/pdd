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

quiz = types.InlineKeyboardMarkup(row_width=1)
yes = types.InlineKeyboardButton("Продолжить", callback_data="quiz")
quiz.add(yes)

ans = types.InlineKeyboardMarkup(row_width=4)
a = types.InlineKeyboardButton("А", callback_data="А")
b = types.InlineKeyboardButton("Б", callback_data="Б")
v = types.InlineKeyboardButton("В", callback_data="В")
g = types.InlineKeyboardButton("Г", callback_data="Г")
ans.add(a, b, v, g)

end = types.InlineKeyboardMarkup()
btn = types.InlineKeyboardButton("Завершить викторину", callback_data="end")
end.add(btn)
