import json
import aiohttp
import asyncio
from datetime import datetime

async def send_offers():
    try:
        with open("contacts.json", "r", encoding="utf-8") as f:
            contacts = json.load(f)
    except FileNotFoundError:
        contacts = []

    success, failed = 0, 0

    for contact in contacts:
        chat_id = contact.get("chat_id")
        if not chat_id:
            continue

        try:
            async with aiohttp.ClientSession() as session:
                # Тут должно быть взаимодействие с Telegram Bot API — заглушка:
                print(f"📨 Отправлено предложение: {chat_id}")
                await asyncio.sleep(1)  # Имитация задержки
                success += 1
        except Exception as e:
            print(f"❌ Не удалось отправить {chat_id}: {e}")
            failed += 1

    log = {
        "time": datetime.now().isoformat(),
        "sent": success,
        "failed": failed
    }

    with open("promotion_log.json", "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(log, ensure_ascii=False) + "\n")

    print(f"✅ Завершено: отправлено — {success}, ошибок — {failed}")
