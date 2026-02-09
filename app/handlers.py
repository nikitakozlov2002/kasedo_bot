import gspread
import re
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, BotCommandScopeDefault, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.keyboards import get_brand_keyboard
from app.keyboards import get_model_keyboard
from app.keyboards import application

# import app.keyboards as kb

router = Router()

def convert_google_drive_link(original_url: str) -> str:
    """
    Конвертирует Google Drive ссылку для Telegram
    
    Из: https://drive.google.com/file/d/1G61yTSjEmBBe3-iSOBSqc6tkph7FLF6r/view?usp=drive_link
    В:  https://drive.google.com/uc?export=view&id=1G61yTSjEmBBe3-iSOBSqc6tkph7FLF6r
    """
    # Извлекаем ID файла из ссылки
    match = re.search(r'/d/([a-zA-Z0-9_-]+)', original_url)
    
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    
    return original_url  # Если не нашли ID, возвращаем как есть

class FootbalBase:
    def get_all_data_for_user(brand: str, model: str):
        gc = gspread.service_account(filename='creds.json')
        wks = gc.open("База данных KASEDO").sheet1
        all_data = wks.get_all_records()

        result = []
        for item in all_data:
            if item["Модель"] == model and item["Бренд"] == brand:  # проверяем, что значение ещё не добавлено
                result.append(item)
        
        return result
    
    def get_brand():
        gc = gspread.service_account(filename='creds.json')
        wks = gc.open("База данных KASEDO").sheet1
        brand_data_all = wks.col_values(2)
        brand_data = list(set(brand_data_all[1:]))
        return brand_data
    
    def get_model(brand: str):
        gc = gspread.service_account(filename='creds.json')
        wks = gc.open("База данных KASEDO").sheet1

        brand_data_all = wks.col_values(2)
        model_data_all = wks.col_values(1)

        brand_model = list(zip(brand_data_all, model_data_all))[1:]

        result = []
        for item in brand_model:
            if item[0] == brand: 
                result.append(item[1])

        # return brand_model
        res = list(set(result))
        return res
    

class Register(StatesGroup):
    name = State()
    tg_id = State()
    brand = State()
    model = State()
    username = State()

@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer('⚽ KASEDO FOOTBALL ⚽\n\nПриветствуем в мире профессиональных футбольных бутс!\nМы — команда энтузиастов, которая знает о футболе всё. Наша миссия — обеспечить каждого игрока идеальной парой бутс для побед на поле.\n\nПочему мы?\n✅ Только оригинальные бутсы от ведущих брендов\n✅ Экспертная помощь в подборе размера и модели\n✅ Выгодные цены и регулярные акции\n✅ Быстрая доставка по всей стране\n\nЗабудьте о мозолях и дискомфорте — с нами вы играете на максимум!\n\nВаши победы начинаются с правильных бутс! 🏆', reply_markup=application)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Register.name)

    await message.answer('Приветствуем! Это наш телеграм бот заявок. Укажите параметры интересующих Вас бутс и мы вышлем, чтобы получить возможные варианты в нашем магазине. Через некоторое время после оставления заявки с Вами свяжется менеджер!')

    await message.answer('Как Вас зовут?')

@router.message(F.text == 'Оставить заявку')
async def register_name(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Как Вас зовут?')

@router.message(Register.name)
async def register_brand(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    nickname = message.from_user.username
    await state.update_data(username=nickname)

    await state.set_state(Register.brand)

    about_user_data = await state.get_data()
    data = FootbalBase.get_brand()
    
    kb = get_brand_keyboard(data)
    
    await message.answer(f'{about_user_data["name"]}, какой бренд бутс Вас интересует?', reply_markup=kb)

@router.message(Register.brand)
async def register_model(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await state.set_state(Register.model)

    about_user_data = await state.get_data()
    brand = about_user_data["brand"]

    data = FootbalBase.get_model(brand)

    kb = get_model_keyboard(data)

    await message.answer(f"Отлично, Вы выбрали {brand}!")
    await message.answer(f'Теперь укажите интересующую Вас модель бутс бренда {brand}', reply_markup=kb)

@router.message(Register.model)
async def register_result_for_user(message: Message, state: FSMContext):
    await state.update_data(model=message.text)

    about_user_data = await state.get_data()
    brand = about_user_data["brand"]
    model = about_user_data["model"]

    await message.answer("Подождите, подбираем для Вас наилучшие варианты...", reply_markup=ReplyKeyboardRemove())
    
    data = FootbalBase.get_all_data_for_user(brand, model)

    for item in data:
        model_item = item["Модель"]
        brand_item = item["Бренд"]
        size = item["EUR"]
        length = item["Длина стопы, см"]
        color = item["Цвет"]
        availability = item["Количество пар в наличии"]
        price = item["Цена"]
        photo = item["Фото"]
        sole = item["Тип подошвы"]

        caption = ""

        if availability != "под заказ":
            caption = (
                "❗В НАЛИЧИИ❗\n"
                f"⚡{model_item}⚡\n"
                f"Цена: {price} руб.\n"
                f"Размер: {size} EUR\n"
                f"Длина стопы: {length}\n"
                f"Цвет: {color}\n"
                f"Тип подошвы: {sole}"
            )
        else:
            caption = (
                "❗ПОД ЗАКАЗ❗\n"
                f"⚡{model_item}⚡\n"
                f"Цена: {price} руб.\n"
                f"Цвет: {color}\n"
                f"Тип подошвы: {sole}"
            )
        
        link = convert_google_drive_link(photo)

        
        await message.answer_photo(
            photo=link,  
            caption=caption,
            parse_mode="HTML"
        )
    
    data = await state.get_data()  
    gc = gspread.service_account(filename='creds.json')
    wks = gc.open("Заявки клиентов").sheet1

    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    array__row = [formatted_time, data["username"], data["name"],
                  data["brand"], data["model"]]

    wks.append_row(array__row)

    admin_message = f"Информация по заявке:\n👤 Имя: {data.get('name', 'не указано')}\n📞 Username: {data.get('username', 'не указано')}\n🏠 Бренд: {data.get('brand', 'не указано')}\n📅 Модель: {data.get('model', 'не указано')}"

    admin_id = 8244538876

    bot = message.bot
    await bot.send_message(chat_id=admin_id, text=admin_message, parse_mode="HTML")

