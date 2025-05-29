from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot_logic import post_news

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(post_news, "interval", minutes=15)
    scheduler.start()
