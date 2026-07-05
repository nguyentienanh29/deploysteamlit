from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv('OPEN_AI_KEY')
_client = None

def get_client():
    global _client

    if _client is None:
        _client = OpenAI(api_key=api_key)

    return _client

def chatbot_response(user_input:str):
    try:
        response = get_client().chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {
                'role': 'system',
                'content': 'Bạn là 1 trợ lý AI hữu ích, dễ thương'
            },
            {
                'role': 'user',
                'content': user_input
            }
        ])
        bot_response = response.choices[0].message.content
        return bot_response.strip()
    except Exception as e:
        return f'Đã xảy ra lỗi : {str(e)}'

def save_chat_history(chat_history, file_path="chat_history.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, ensure_ascii=False, indent=2)

def load_chat_history(file_path="chat_history.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
