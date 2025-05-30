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
    results = []

    for contact in contacts:
        chat_id = contact.get("chat_id")
        if not chat_id:
            continue

        try:
            async with aiohttp.ClientSession() as session:
                # Здесь должна быть реальная отправка сообщения через Telegram API
                print(f"📨 Отправлено предложение: {chat_id}")
                await asyncio.sleep(1)  # Имитация задержки
                results.append({"chat_id": chat_id, "status": "sent"})
                success += 1
        except Exception as e:
            print(f"❌ Не удалось отправить {chat_id}: {e}")
            results.append({"chat_id": chat_id, "status": "failed", "error": str(e)})
            failed += 1

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "summary": {"sent": success, "failed": failed},
        "results": results
    }

    with open("promotion_log.json", "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    print(f"✅ Завершено: отправлено — {success}, ошибок — {failed}")
