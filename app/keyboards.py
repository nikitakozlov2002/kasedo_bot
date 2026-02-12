from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

application = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 Каталог", callback_data="catalog"), InlineKeyboardButton(text="⭐ Отзывы", url="https://t.me/kasedofc/54")]
        ]
    ) 

after_catalog_keyboadrd = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Задать вопрос')], [KeyboardButton(text='Оформить заказ')]], resize_keyboard=True)

def get_brand_keyboard(brands: list):
    result = []
    for brand in brands:
        result.append([KeyboardButton(text=brand)])
    
    keyboard_res = ReplyKeyboardMarkup(keyboard=result)

    return keyboard_res

def get_model_keyboard(models: list):
    result = []
    for model in models:
        result.append([KeyboardButton(text=model)])
    
    keyboard_res = ReplyKeyboardMarkup(keyboard=result)

    return keyboard_res

main_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 О нас", callback_data="about"),  InlineKeyboardButton(text="🎁 Бонусы", callback_data="bonus")],
            [InlineKeyboardButton(text="📦 Каталог", callback_data="catalog"), InlineKeyboardButton(text="⭐ Отзывы", url="https://t.me/kasedofc/54")],
            [InlineKeyboardButton(text="❓ Задать вопрос", callback_data="question")]
        ]
    )

choice = InlineKeyboardMarkup(
        inline_keyboard=[
           [InlineKeyboardButton(text="👟 Бутсы", callback_data="boots")],
            [InlineKeyboardButton(text="🧤 Другая вещь", callback_data="another_thing")]
        ]
    ) 