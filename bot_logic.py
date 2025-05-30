import os



from aiogram import Bot



from news_fetcher import fetch_latest_news



from annotator import generate_annotation



from config import CHANNEL_USERNAME







async def post_news():



    try:



        TOKEN = os.getenv("BOT_TOKEN")



        bot = Bot(token=TOKEN)







        news_items = fetch_latest_news()



        if not news_items:



            print('Нет новостей для публикации.')



            return







        news = news_items[0]



        print("news:", news)



        print("Ключи в news:", list(news.keys()))







        summary = news.get('summary') or news.get('description') or news.get('text') or ''



        annotation = generate_annotation(news.get('title', ''), summary)



        if not annotation:



            annotation = news.get('title', 'Без заголовка')







        channel_username = CHANNEL_USERNAME







        title = news.get('title', '')        summary = news.get('summary') or news.get('description') or news.get('text') or ''        text = f"""📰 <b>{annotation}</b>\n\n🧠 {title}\n\n📌 {summary}\n\n📡 {channel_username}"""

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url="https://t.me/fastnewsrussian")],
            [InlineKeyboardButton(text="📤 Поделиться", switch_inline_query="")]
        ])






        if annotation:



            text += f"<b>{annotation}</b>\n"







        if summary:



            text += f"{summary}\n\n"







        text += f"📰 {channel_username}"











        image_url = news.get('image', '')







        if image_url:



            try:



        await bot.send_photo(chat_id=channel_username, photo=image_url, caption=text, parse_mode="HTML", reply_markup=keyboard)



                print(f"Пост опубликован с фото в @{channel_username}")



            except Exception as e:



                print(f"Не удалось отправить фото, ошибка: {e}. Пробую отправить только текст.")






                print(f"Пост опубликован без фото в @{channel_username}")



        else:






            print(f"Пост опубликован без фото в @{channel_username}")







    except Exception as e:



        print(f"Ошибка при автопостинге: {e}")