from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

application = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Оставить заявку')]], resize_keyboard=True)

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
