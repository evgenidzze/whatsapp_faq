import json
import faiss
import aiohttp
import redis
import numpy as np

from sentence_transformers import SentenceTransformer
from config import PHONE_NUMBER_ID, ACCESS_TOKEN, REDIS_HOST

model = SentenceTransformer("all-MiniLM-L6-v2")
r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)


async def load_responses():
    """Дістає варіанти відповідей з кешу або файлу, якщо немає в кеші"""
    cached_responses = r.get("responses")
    if cached_responses:
        return json.loads(cached_responses)
    else:
        with open('responses.json', 'r', encoding='utf-8') as f:
            responses = json.load(f)
            r.set("responses", json.dumps(responses), ex=3600)  # Кешування на 1 годину
            return responses


async def send_whatsapp_message(to, text):
    """Надсилає користувачу відповідь"""
    access_token = ACCESS_TOKEN
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as res:
            response_json = await res.json()
            return response_json


async def find_best_answer(query):
    """Знаходить найбільш підходящу відповідь користувачу"""
    responses = await load_responses()  # Перевіряємо оновлення перед кожним запитом
    questions = list(responses.keys())
    question_vectors = np.array([model.encode(q) for q in questions]).astype("float32")

    index = faiss.IndexFlatL2(question_vectors.shape[1])
    index.add(question_vectors)

    query_vector = model.encode(query).astype("float32").reshape(1, -1)
    _, top_match = index.search(query_vector, 1)

    best_match = questions[top_match[0][0]]
    confidence = _[0][0]
    return responses[best_match] if confidence < 0.5 else "Вибач, я не розумію цього питання."

