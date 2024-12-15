import asyncio
import os
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile
from googletrans import Translator  # Для перевода текста
from config import TOKEN

# Создаем объект бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Убедимся, что папка img существует
if not os.path.exists("img"):
    os.makedirs("img")

# Обработка команды /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот и готов помочь.")

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Доступные команды:\n"
                         "/start - Запуск бота\n"
                         "/help - Список команд\n"
                         "/photo - Отправить случайное фото\n"
                         "/joke - Рассказать анекдот\n"
                         "/motivation - Мотивационная цитата\n"
                         "/game - Угадай число\n"
                         "/voice - Отправить голосовое сообщение\n"
                         "Просто отправьте текст, чтобы перевести его на английский.")

# Обработка фото: сохранение и ответ фразой
@dp.message(F.photo)
async def handle_photo(message: Message):
    # Убедимся, что папка img существует
    if not os.path.exists("img"):
        os.makedirs("img")

    # Сохраняем фото
    file_id = message.photo[-1].file_id
    file_path = f"img/{file_id}.jpg"

    # Скачиваем файл
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, destination=file_path)

    # Отправляем подтверждение пользователю
    await message.answer("Ваше фото успешно сохранено!")

# Обработка команды /voice
@dp.message(Command("voice"))
async def send_voice(message: Message):
    voice_file = FSInputFile("sample.ogg")
    await message.answer_voice(voice_file)

# Обработка перевода текста на английский язык
@dp.message(F.text)
async def translate_text(message: Message):
    translator = Translator()
    translated = translator.translate(message.text, src="ru", dest="en")
    await message.answer(f"Перевод: {translated.text}")

# Главная асинхронная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
