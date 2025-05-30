from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
