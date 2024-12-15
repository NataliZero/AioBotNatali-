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

# Обработка команды /photo
@dp.message(Command("photo"))
async def send_random_photo(message: Message):
    photo_urls = [
        "https://example.com/photo1.jpg",
        "https://example.com/photo2.jpg",
        "https://example.com/photo3.jpg",
    ]
    random_photo = random.choice(photo_urls)  # Выбираем случайное фото
    await message.answer_photo(photo=random_photo, caption="Это супер крутая картинка!")

# Обработка команды /joke
@dp.message(Command("joke"))
async def tell_joke(message: Message):
    jokes = [
        "Почему у слона большие уши? Потому что маленькие плохо слышат!",
        "Почему кошки хорошие программисты? Потому что у них лапы вместо багов.",
        "Почему утки такие хорошие танцоры? Потому что у них ритм в крови — кря-кря!",
        "Почему огурец смеётся? Потому что упал в солёную компанию!"
    ]
    random_joke = random.choice(jokes)
    await message.answer(random_joke)

# Обработка команды /motivation
@dp.message(Command("motivation"))
async def send_motivation(message: Message):
    quotes = [
        "Вернись к своей цели. Ты уже так близко к успеху!",
        "Величие достигается упорным трудом и верой в себя.",
        "Каждый день — это новый шанс изменить свою жизнь к лучшему.",
        "Не бойся неудач, бойся бездействия. Начни двигаться прямо сейчас!",
        "У тебя больше силы, чем ты думаешь. Просто сделай это!"
    ]
    random_quote = random.choice(quotes)
    await message.answer(random_quote)

# Обработка команды /game
@dp.message(Command("game"))
async def start_game(message: Message):
    secret_number = random.randint(1, 10)  # Генерируем случайное число
    await message.answer(
        f"Я загадал число от 1 до 10. Попробуй угадать! Напиши число в ответ."
    )
    # Сохраняем число в пользовательских данных
    dp["secret_number"] = secret_number

# Обработка ответа пользователя
@dp.message(F.text.regexp(r"^\d+$"))  # Проверяем, что пользователь отправил число
async def check_number(message: Message):
    guessed_number = int(message.text)
    secret_number = dp.get("secret_number")  # Получаем загаданное число

    if guessed_number == secret_number:
        await message.answer("Поздравляю! Ты угадал! 🎉")
        # Сбрасываем загаданное число, чтобы начать заново
        dp["secret_number"] = random.randint(1, 10)
        await message.answer("Давай сыграем ещё раз! Я загадал новое число.")
    else:
        await message.answer("Не угадал! Попробуй ещё раз.")

import os  # Для работы с файловой системой

# Убедимся, что папка img существует
if not os.path.exists("img"):
    os.makedirs("img")

# Обработка и сохранение фото
@dp.message(F.photo)
async def save_photo(message: Message):
    file_id = message.photo[-1].file_id
    file_path = f"img/{file_id}.jpg"
    await bot.download(file=message.photo[-1], destination=file_path)
    await message.answer("Фото сохранено!")

# Главная асинхронная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
