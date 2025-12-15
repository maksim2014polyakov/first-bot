from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command
from dotenv import load_dotenv
import os, asyncio

load_dotenv()
BOT_TOKEN=os.getenv("BOT_TOKEN")

bot=Bot(BOT_TOKEN)
dp=Dispatcher()

@dp.message(Command("start"))
async def start(msg: types.Message):
    print(msg.from_user.id, msg.from_user.full_name)
    await msg.answer("привет я бот")

@dp.message(Command("about"))
async def about(msg: types.Message):
    await msg.answer("этот бот может помочь тебе с учебой в школе")

async def main():
    await dp.start_polling(bot)


asyncio.run(main())