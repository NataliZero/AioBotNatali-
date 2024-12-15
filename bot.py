import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart  # Импортируем фильтры команд
from aiogram.types import Message
from config import TOKEN

# Создаем объект бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработка команды /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Приветики, я бот!")

# Обработка команды /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start - Запуск бота\n/help - Помощь и список команд")

from aiogram import F  # Добавляем новый импорт для обработки текста

# Обработка текстового сообщения "что такое ИИ?"
@dp.message(F.text == "что такое ИИ?")
async def ai_question(message: Message):
    await message.answer(
        "Искусственный интеллект — это свойство искусственных систем выполнять творческие функции, "
        "которые традиционно считаются прерогативой человека."
    )

import random  # Импортируем модуль random для выбора случайной фразы

# Обработка фото
@dp.message(F.photo)
async def react_to_photo(message: Message):
    responses = [
        "Ого, какая фотка!",
        "Непонятно, что это такое.",
        "Не отправляй мне такое больше!",
    ]
    random_response = random.choice(responses)  # Выбираем случайную фразу
    await message.answer(random_response)

# Главная асинхронная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
