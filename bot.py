import asyncio
import json
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import Command
from scheduler import start_scheduler
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
from aiogram.client.default import DefaultBotProperties
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

MAX_LOGS = 30
PREFS_FILE = "user_prefs.json"

def get_user_lang(user_id):
    try:
        with open(PREFS_FILE, "r", encoding="utf-8") as f:
            prefs = json.load(f)
        return prefs.get(str(user_id), "ru")
    except:
        return "ru"

def set_user_lang(user_id, lang):
    try:
        with open(PREFS_FILE, "r", encoding="utf-8") as f:
            prefs = json.load(f)
    except:
        prefs = {}
    prefs[str(user_id)] = lang
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("🤖 Бот запущен и работает!\nИспользуйте /log чтобы посмотреть статистику продвижения.")

@router.message(Command("lang"))
async def lang_handler(msg: Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇬🇧 English")]
    ], resize_keyboard=True)
    await msg.answer("🌍 Выберите язык / Select your language:", reply_markup=kb)

@router.message(F.text.in_(["🇷🇺 Русский", "🇬🇧 English"]))
async def lang_choice(msg: Message):
    lang = "ru" if "Рус" in msg.text else "en"
    set_user_lang(msg.from_user.id, lang)
    response = "✅ Язык установлен: Русский" if lang == "ru" else "✅ Language set to: English"
    await msg.answer(response, reply_markup=types.ReplyKeyboardRemove())

@router.message(F.text.lower() == "/log")
async def handle_log_request(message: types.Message):
    user_lang = get_user_lang(message.from_user.id)

    try:
        with open("promotion_log.json", "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) > MAX_LOGS:
            with open("promotion_log.json", "w", encoding="utf-8") as f:
                f.writelines(lines[-MAX_LOGS:])
            lines = lines[-MAX_LOGS:]

        latest = lines[-3:]
        text = "📈 Recent promotion logs:\n\n" if user_lang == "en" else "📈 Последние логи автопродвижения:\n\n"

        for line in latest:
            entry = json.loads(line)
            timestamp = entry["timestamp"]
            sent = entry["summary"]["sent"]
            failed = entry["summary"]["failed"]
            if user_lang == "en":
                text += f"🕒 {timestamp}\n✅ Sent: {sent}\n❌ Failed: {failed}\n\n"
            else:
                text += f"🕒 {timestamp}\n✅ Отправлено: {sent}\n❌ Ошибок: {failed}\n\n"
    except Exception as e:
        text = f"⚠️ Couldn't read logs: {e}" if user_lang == "en" else f"⚠️ Не удалось получить лог: {e}"

    await message.answer(text)

async def main():
    start_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
