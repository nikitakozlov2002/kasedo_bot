from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Оставить заявку')],
    [KeyboardButton(text='Помощь')]
    ], 
    resize_keyboard=True,
    input_field_placeholder = 'Скорее оставляйте заявку!')

after_start = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='О нас')]], resize_keyboard=True)

after_about = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Оставить заявку')]], resize_keyboard=True)

brand = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Nike')], 
    [KeyboardButton(text='Adidas')],
    [KeyboardButton(text='Puma')], 
    [KeyboardButton(text='Mizuno')],
    [KeyboardButton(text='Joma')]
], 
resize_keyboard=True,
input_field_placeholder = 'Какой бренд Вас интересует?')

model_nike = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Phantom')], 
    [KeyboardButton(text='Mercurial')],
    [KeyboardButton(text='Tiempo')],
], 
resize_keyboard=True,
input_field_placeholder = 'Какая модель Вас интересует?')

model_adidas = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Predator')], 
    [KeyboardButton(text='X')],
    [KeyboardButton(text='Copa')],
], 
resize_keyboard=True,
input_field_placeholder = 'Какая модель Вас интересует?')

size = ReplyKeyboardMarkup(keyboard=[
    [[KeyboardButton(text='40-41')], [KeyboardButton(text='42-43')]],
    [[KeyboardButton(text='41-42')], [KeyboardButton(text='43-44')]],
    [KeyboardButton(text='Больше 44')]
], 
resize_keyboard=True,
input_field_placeholder = 'Укажите в каком диапозоне интересующий Вас размер')

# yes_or_not = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text='Да')],
#     [KeyboardButton(text='Нет')]
# ], 
# resize_keyboard=True,
# input_field_placeholder = 'Выберите один из предложенных вариантов')