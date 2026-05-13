import asyncio
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
import gspread

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_url('')
worksheet = sh.sheet1

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для сбора фидбека\n"
        "Напиши свою идею или предложение, и я передам их команде!"
    )

@dp.message(F.text)
async def process_feedback(message: types.Message):
    user = message.from_user
    username = f"@{user.username}" if user.username else user.first_name
    text = message.text
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        worksheet.append_row([date, username, "Фидбек", text])
        await message.answer("Спасибо! Записали твой отзыв")
    except Exception as e:
        await message.answer("Упс, что-то пошло не так. Попробуй позже")
        print(f"Ошибка БД: {e}. Обратись к администратору: @kilokeks")

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())