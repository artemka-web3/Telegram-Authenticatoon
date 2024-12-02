import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
LT_URL = 'https://shaggy-crabs-stick.loca.lt'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(Command("start"))
async def start(message: types.Message):
    args = message.get_args()
    token = args if args else None
    if not token:
        await message.reply("Токен отсутствует.")
        return

    chat_id = message.chat.id
    username = message.from_user.username
    url = f"{LT_URL}/telegram-callback/?token={token}&telegram_id={chat_id}&username={username}"
    await message.reply(f"Нажмите сюда, чтобы завершить авторизацию: {url}", parse_mode=ParseMode.HTML)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)