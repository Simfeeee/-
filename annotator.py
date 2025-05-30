import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_annotation(title, summary):
    try:
        prompt = f"""Придумай ироничную, короткую, оригинальную аннотацию к новости:

Заголовок: {title}

Краткое содержание: {summary}"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=50
        )
        return response.choices[0].message["content"].strip()
    except Exception:
        return ""