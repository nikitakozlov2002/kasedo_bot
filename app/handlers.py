import gspread
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, BotCommandScopeDefault
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()


class Register(StatesGroup):
    name = State()
    tg_id = State()
    brand = State()
    model = State()
    size = State()
    city = State()

@router.message(F.text == 'О нас')
@router.message(Command("about"))
async def cmd_about(message: Message):
    await message.answer('Информация о магаизине...', reply_markup=kb.after_about)

@router.message(Command("reglament"))
async def cmd_reglament(message: Message):
    reglament_pdf = FSInputFile("reglament_master.pdf")
    await message.answer_document(reglament_pdf,  caption="Высылаем Вам для ознакомления реглмаент работы мастера", reply_markup=kb.after_start)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Приветствуем! Это наш телеграм бот заявок. Укажите параметры интересующей Вас модели, чтобы получить возможные варианты. Через некоторое время с Вами свяжется менеджер!', reply_markup=kb.main)


@router.message(F.text == 'Оставить заявку')
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Напишите, пожалуйста, Ваше имя', reply_markup=kb.after_start)


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.brand)
    data = await state.get_data()
    await message.answer(f'{data["name"]}, укажите интересующий Вас бренд бутс', reply_markup=kb.brand)

@router.message(Register.brand)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(brand=message.text)
    await state.set_state(Register.model)
    data = await state.get_data()
    await message.answer(f'Теперь укажите интересующую Вас модель бутс бренда {data["brand"]}', reply_markup=kb.brand)


# @router.message(Register.age)
# async def register_age(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.set_state(Register.tel)
#     await message.answer('Введите Ваш номер телефона')


# @router.message(Register.tel)
# async def register_tel(message: Message, state: FSMContext):
#     await state.update_data(tel=message.text)
#     await state.set_state(Register.nationality)
#     await message.answer('Какое у Вас гражданство?')


# @router.message(Register.nationality)
# async def register_nationality(message: Message, state: FSMContext):
#     await state.update_data(nationality=message.text)
#     await state.set_state(Register.type_work)
#     await message.answer('Напишите какие бытовые работы вы умеете выполнять')


# @router.message(Register.type_work)
# async def register_type_work(message: Message, state: FSMContext):
#     await state.update_data(type_work=message.text)
#     await state.set_state(Register.experience)
#     await message.answer('Какой у Вас опыт работы в сфере бытовых работ?', reply_markup=kb.experience)


# @router.message(Register.experience)
# async def register_experience(message: Message, state: FSMContext):
#     await state.update_data(experience=message.text)
#     await state.set_state(Register.instrument)
#     await message.answer('Есть ли у Вас свой инструмент?', reply_markup=kb.yes_or_not)


# @router.message(Register.instrument)
# async def register_instrument(message: Message, state: FSMContext):
#     await state.update_data(instrument=message.text)
#     await state.set_state(Register.car)
#     await message.answer('Есть ли у Вас собственный автомобиль?', reply_markup=kb.yes_or_not)


# @router.message(Register.car)
# async def register_car(message: Message, state: FSMContext):
#     await state.update_data(car=message.text)

#     data = await state.get_data()  # get data master
#     gc = gspread.service_account(filename='creds.json')
#     wks = gc.open("Заявка на трудоустройство на мастера").sheet1

#     array__row = [data["name"], data["age"],
#                   data["tel"], data["nationality"],
#                   data["type_work"], data["experience"],
#                   data["instrument"], data["car"], "Новая заявка"]

#     wks.append_row(array__row)
#     reglament_pdf = FSInputFile("reglament_master.pdf")
#     await message.answer_document(reglament_pdf,  caption="Cпасибо большое за оставленную заявку.\nВ течении часа с Вами свяжется наш специалист, чтобы рассказать про нас еще больше и уточнить еще кое-какую информацию!\nА пока что высылаем Вам для ознакомления реглмаент работы мастера", reply_markup=kb.after_start)