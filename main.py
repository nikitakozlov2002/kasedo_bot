import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from app.handlers import router

async def set_default_commands(bot: Bot):
    """Функция для установки команд меню. Вызовите её при старте бота."""
    commands = [
        BotCommand(command="start", description="🚀 Начать работу"),
        BotCommand(command="menu", description="🏠 Меню"),
        BotCommand(command="about", description="📋 О нас"),
        BotCommand(command="bonus", description="🎁 Бонусы"),
        BotCommand(command="question", description="❓ Задать вопрос")
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())

async def main():
    bot = Bot(token = '8335551745:AAG6N_8290FNuOJtyvlr7590vqs1M7O3HUw')
    dp = Dispatcher()
    dp.include_router(router)
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        print("Бот по KASEDO начал работать!")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот по KASEDO выключен!")