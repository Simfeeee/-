import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_annotation(title, summary):
    prompt = f"Новость: {title}\n\nСодержание: {summary}\n\nСделай краткую, оригинальную, живую аннотацию для Telegram-поста."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.7,
        max_tokens=80,
    )

    return response.choices[0].message["content"].strip()
