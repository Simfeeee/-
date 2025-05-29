import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_annotation(title, text):
    prompt = f"""Прочитай заголовок и текст новости и составь краткую ироничную аннотацию, затем выдели основные факты (кто, где, что произошло). Не указывай источник.

Заголовок: {title}
Текст: {text}

Ответ в формате:

📝 Аннотация: ...
📌 Факты: ..."""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Аннотация временно недоступна: {e}"
