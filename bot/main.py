import asyncio
import os
from api_get_data import *
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message
from uuid import uuid4

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_id = uuid4()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("ASSALOMU ALAYKUM BIZNING BOTIMIZGA XUSH KELIBSIZ !")


@dp.message(Command("chat"))
async def chat(message: Message):
    request = message.text.removeprefix("/chat").strip()
    result = chat_ai(request=request, session_id=str(user_id))
    await message.answer(result)


async def main():
    await  dp.start_polling(bot)


if __name__ == '__main__':
    print("Bot started")
    asyncio.run(main())
