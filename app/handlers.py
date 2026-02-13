import gspread
import re
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, BotCommandScopeDefault, ReplyKeyboardRemove, CallbackQuery  
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.keyboards import get_brand_keyboard
from app.keyboards import get_model_keyboard
from app.keyboards import application
from app.keyboards import main_keyboard
from app.keyboards import after_catalog_keyboadrd
from app.keyboards import choice

router = Router()

def find_by_artikul(items, articul):
    """Найти товар по артикулу"""
    for item in items:
        if str(item.get("Артикул")) == articul: 
            return item
    return {}

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
    
    def get_product_by_articul(articul):
        gc = gspread.service_account(filename='creds.json')
        wks = gc.open("База данных KASEDO").sheet1
        all_data = wks.get_all_records()

        result = find_by_artikul(all_data, articul)

        return result
    

class Register(StatesGroup):
    name = State()
    tg_id = State()
    brand = State()
    model = State()
    choice = State()
    result_catalog = State()
    username = State()
    message_to_admin = State()
    application = State()
    application_find_articul = State()
    another_thing_application = State()
    another_thing = State()


@router.callback_query(F.data == "question")
@router.message(Command("question"))
@router.message(F.text == 'Задать вопрос')
async def register_question_user(event: CallbackQuery | Message, state: FSMContext):
    nickname = event.from_user.username
    await state.update_data(username=nickname)

    await state.set_state(Register.message_to_admin)

    if isinstance(event, CallbackQuery):
        await event.message.answer('Напишите свой вопрос. Мы перенаправим его менеджеру, который в течении часа Вам ответит!')
        await event.answer()
    else:
        await event.answer('Напишите свой вопрос. Мы перенаправим его менеджеру, который в течении часа Вам ответит!')

@router.message(Register.message_to_admin)
async def register_send_message(message: Message, state: FSMContext):
    await state.set_state(None)

    data_message = message.text

    data = await state.get_data()

    admin_message = f"ВОПРОС КЛИЕНТА:\n📞 Username: {data.get('username', 'не указано')}\n📅 Question: {data_message}"

    admin_id = 8244538876
    # admin_id = 530775145

    bot = message.bot
    await bot.send_message(chat_id=admin_id, text=admin_message, parse_mode="HTML")

    await message.answer('Ваш вопрос успешно переадресован менеджеру. В самое ближайшее время он Вам ответит!', reply_markup=application)


    
@router.callback_query(F.data == "about")
@router.message(F.text == 'О нас')
@router.message(Command("about"))
async def cmd_about(event: Message | CallbackQuery):
    if isinstance(event, CallbackQuery):
        await event.message.answer('KASEDO — ТВОЙ НАДЕЖНЫЙ ПАРТНЕР НА ПОЛЕ.\n\nМы обеспечиваем профессионалов надежной экипировкой.\n\nПОЧЕМУ СТОИТ ВЫБРАТЬ НАС?\n\n🔥 ШИРОКИЙ ВЫБОР АССОРТИМЕНТА В НАЛИЧИИ И НА ЗАКАЗ\n• Все топ-бренды: Nike, Adidas, Puma, New Balance и другие.\n• Полные размерные сетки, включая редкие и полные размеры.\n• Модели для любого покрытия: FG, SG, AG, TF/TT.\n\n💸 ДОСТУПНЫЕ ЦЕНЫ БЕЗ ЛИШНИХ НАЦЕНОК\n\n• Честные и прозрачные цены.\n• Регулярные поставки напрямую от официальных дистрибьюторов.\n• Акции, скидки, и специальные условия для клубов и постоянных клиентов.\n\n🤝 ЭКСПЕРТНАЯ ПОМОЩЬ В ВЫБОРЕ\n\n• Подскажем с размером и полнотой, чтобы бутсы сели идеально.\n• Поможем подобрать модель под ваш стиль игры, амплуа и тип покрытия.\n\n🚀 БЫСТРЫЙ И НАДЕЖНЫЙ СЕРВИС\n\n• Тщательная проверка и подготовка каждой пары перед отправкой.\n• Гарантия качества.\n\nВАША ИДЕАЛЬНАЯ ПАРА — ВСЕГО В 3 ШАГА:\n\nНаписать в direct → Подобрать модель → Получить заказ\n\n🏆 ДОВЕРЬТЕСЬ ПРОФЕССИОНАЛАМ — ИГРАЙТЕ С УВЕРЕННОСТЬЮ!', reply_markup=application)
        await event.answer() 
    else:
        await event.answer('KASEDO — ТВОЙ НАДЕЖНЫЙ ПАРТНЕР НА ПОЛЕ.\n\nМы обеспечиваем профессионалов надежной экипировкой.\n\nПОЧЕМУ СТОИТ ВЫБРАТЬ НАС?\n\n🔥 ШИРОКИЙ ВЫБОР АССОРТИМЕНТА В НАЛИЧИИ И НА ЗАКАЗ\n• Все топ-бренды: Nike, Adidas, Puma, New Balance и другие.\n• Полные размерные сетки, включая редкие и полные размеры.\n• Модели для любого покрытия: FG, SG, AG, TF/TT.\n\n💸 ДОСТУПНЫЕ ЦЕНЫ БЕЗ ЛИШНИХ НАЦЕНОК\n\n• Честные и прозрачные цены.\n• Регулярные поставки напрямую от официальных дистрибьюторов.\n• Акции, скидки, и специальные условия для клубов и постоянных клиентов.\n\n🤝 ЭКСПЕРТНАЯ ПОМОЩЬ В ВЫБОРЕ\n\n• Подскажем с размером и полнотой, чтобы бутсы сели идеально.\n• Поможем подобрать модель под ваш стиль игры, амплуа и тип покрытия.\n\n🚀 БЫСТРЫЙ И НАДЕЖНЫЙ СЕРВИС\n\n• Тщательная проверка и подготовка каждой пары перед отправкой.\n• Гарантия качества.\n\nВАША ИДЕАЛЬНАЯ ПАРА — ВСЕГО В 3 ШАГА:\n\nНаписать в direct → Подобрать модель → Получить заказ\n\n🏆 ДОВЕРЬТЕСЬ ПРОФЕССИОНАЛАМ — ИГРАЙТЕ С УВЕРЕННОСТЬЮ!', reply_markup=application)

@router.callback_query(F.data == "bonus")
@router.message(F.text == 'Бонусы')
@router.message(Command("bonus"))
async def cmd_about(event: Message | CallbackQuery):
    if isinstance(event, CallbackQuery):
        await event.message.answer('БОНУСНАЯ ПРОГРАММА 🎁\n\n1. ПОЛУЧАЙТЕ БОНУСЫ\nЗА КАЖДУЮ ПОКУПКУ МЫ НАЧИСЛЯЕМ НА ВАШ БОНУСНЫЙ СЧЕТ 7% ОТ ЕЕ суммы.\n\n2. КОПИТЕ И СПИСЫВАЙТЕ\nВЫ МОЖЕТЕ КОПИТЬ БОНУСЫ ДЛЯ КРУПНОЙ ПОКУПКИ ИЛИ ЧАСТИЧНО СПИСЫВАТЬ ИХ НА ОПЛАТУ СЛЕДУЮЩИХ ЗАКАЗОВ. РЕШАЕТЕ ВЫ!\n\n3. ИСПОЛЬЗУЙТЕ ВОВРЕМЯ\nБОНУСЫ НЕОБХОДИМО ПОТРАТИТЬ В ТЕЧЕНИЕ 6 МЕСЯЦЕВ С МОМЕНТА ПОКУПКИ, ПОСЛЕ ЧЕГО ОНИ СГОРАЮТ.\n\nВАША ИГРА - ВАША ВЫГОДА', reply_markup=application)
        await event.answer() 
    else:
        await event.answer('БОНУСНАЯ ПРОГРАММА 🎁\n\n1. ПОЛУЧАЙТЕ БОНУСЫ\nЗА КАЖДУЮ ПОКУПКУ МЫ НАЧИСЛЯЕМ НА ВАШ БОНУСНЫЙ СЧЕТ 7% ОТ ЕЕ суммы.\n\n2. КОПИТЕ И СПИСЫВАЙТЕ\nВЫ МОЖЕТЕ КОПИТЬ БОНУСЫ ДЛЯ КРУПНОЙ ПОКУПКИ ИЛИ ЧАСТИЧНО СПИСЫВАТЬ ИХ НА ОПЛАТУ СЛЕДУЮЩИХ ЗАКАЗОВ. РЕШАЕТЕ ВЫ!\n\n3. ИСПОЛЬЗУЙТЕ ВОВРЕМЯ\nБОНУСЫ НЕОБХОДИМО ПОТРАТИТЬ В ТЕЧЕНИЕ 6 МЕСЯЦЕВ С МОМЕНТА ПОКУПКИ, ПОСЛЕ ЧЕГО ОНИ СГОРАЮТ.\n\nВАША ИГРА - ВАША ВЫГОДА', reply_markup=application)

@router.message(CommandStart())
@router.message(Command("menu"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Register.brand)

    await message.answer('Здравствуйте! 👋\nВас приветствует Telegram-бот магазина Футбольной атрибутики - KASEDO.\nЯ помогу вам узнать всё о нас и подобрать то, о чём давно мечтали ❤️', reply_markup=main_keyboard)


@router.callback_query(F.data == "catalog")
async def register_brand(event: Message | CallbackQuery, state: FSMContext):
    nickname = event.from_user.username
    await state.update_data(username=nickname)
    await event.message.answer('Что вы хотите найти?', reply_markup=choice)
    await event.answer() 

@router.callback_query(F.data == "another_thing")
async def register_brand(event: Message | CallbackQuery, state: FSMContext):
    await state.set_state(Register.another_thing_application)
    await event.message.answer('Напишите в ответном сообщении конкретно какая вещь Вас интересует?', reply_markup=None)
    
@router.message(Register.another_thing_application)
async def register_brand(event: Message, state: FSMContext):
    await state.set_state(None)

    another_thing = event.text
    nickname = event.from_user.username

    result_row = []

    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    result_row = [formatted_time, nickname, another_thing]

    gc = gspread.service_account(filename='creds.json')
    wks = gc.open("Оформленные заявки").sheet1

    wks.append_row(result_row)

    await event.answer("Спасибо за оформленный заказ, менеджер напишет Вам в течении часа для уточнения деталей!", reply_markup=main_keyboard)
    

@router.callback_query(F.data == "boots")
@router.message(Register.brand)
async def register_brand(event: Message | CallbackQuery, state: FSMContext):
    nickname = event.from_user.username
    await state.update_data(username=nickname)

    await state.set_state(Register.model)

    data = FootbalBase.get_brand()

    kb = get_brand_keyboard(data)
    
    if isinstance(event, CallbackQuery):
        await event.message.answer('Какой бренд бутс Вас интересует?', reply_markup=kb)
        await event.answer() 
    else:
        await event.answer('Какой бренд бутс Вас интересует?', reply_markup=kb)

@router.message(Register.model)
async def register_model(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await state.set_state(Register.result_catalog)

    about_user_data = await state.get_data()
    brand = about_user_data["brand"]

    data = FootbalBase.get_model(brand)

    kb = get_model_keyboard(data)

    await message.answer(f"Отлично, Вы выбрали {brand}!")
    await message.answer(f'Теперь укажите интересующую Вас модель бутс бренда {brand}', reply_markup=kb)

@router.message(Register.result_catalog)
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
        articul = item["Артикул"]

        caption = ""

        if availability != "под заказ":
            caption = (
                f"🔍 АРТИКУЛ №: {articul}\n\n"
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
                f"🔍 АРТИКУЛ №: {articul}\n\n"
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

    array__row = [formatted_time, data["username"],
                  data["brand"], data["model"]]

    wks.append_row(array__row)

    admin_message = f"Информация по заявке:\n📞 Username: {data.get('username', 'не указано')}\n🏠 Бренд: {data.get('brand', 'не указано')}\n📅 Модель: {data.get('model', 'не указано')}"

    admin_id = 8244538876
    # admin_id = 530775145

    bot = message.bot
    await bot.send_message(chat_id=admin_id, text=admin_message, parse_mode="HTML")

    user_response = (
        f"✅ Спасибо за ваш запрос!\n\n"
        f"Мы передали менеджеру информацию о поиске:\n"
        f"📌 {data.get('model', 'НЕ УКАЗАНО')}\n\n"
        f"⏳ В ближайшее время с вами свяжутся для уточнения наличия и оформления заказа.\n\n"
        f"💬 Если у вас есть дополнительные вопросы - нажмите кнопку ниже"
    )

    await state.set_state(Register.application_find_articul)

    await message.answer(user_response, reply_markup=after_catalog_keyboadrd)

@router.message(Register.application_find_articul)
@router.message(F.text == 'Оформить заказ')
async def register_application(message: Message, state: FSMContext):
    await state.set_state(Register.application)

    await message.answer("Напишите номер артикула модели, которую Вы, хотите заказать", eply_markup=None)

@router.message(Register.application)
async def register_application(message: Message, state: FSMContext):
    await state.set_state(None)

    articul = str(message.text).strip()
    nickname = message.from_user.username

    data = FootbalBase.get_product_by_articul(articul)

    result_row = []

    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    result_row = [formatted_time, nickname, articul, data.get('Бренд', 'Не известно - не верный артикул'), data.get('Модель', 'Не известно - не верный артикул')]

    gc = gspread.service_account(filename='creds.json')
    wks = gc.open("Оформленные заявки").sheet1

    wks.append_row(result_row)

    await message.answer("Спасибо за оформленный заказ, менеджер напишет Вам в течении часа для уточнения деталей!", reply_markup=main_keyboard)