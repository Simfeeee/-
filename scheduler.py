from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot_logic import post_news
from aiogram import Bot

def start_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(post_news, "interval", minutes=30, args=[bot])
    scheduler.start()
