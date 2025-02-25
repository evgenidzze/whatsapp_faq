from fastapi import FastAPI, Request
from config import SECRET
from utils import send_whatsapp_message, find_best_answer
from logger import log_message

app = FastAPI()


@app.get("/webhook")
async def verify_webhook(request: Request):
    """Перевірка Webhook для WhatsApp (Meta вимагає цього)."""
    query = request.query_params
    if query.get("hub.mode") == "subscribe" and query.get("hub.verify_token") == SECRET:
        return int(query.get("hub.challenge", 0))
    return {"error": "Invalid token"}


@app.post("/webhook")
async def receive_message(request: Request):
    """Приймає повідомлення від WhatsApp та відповідає."""
    data = await request.json()

    if "entry" not in data:
        return {"status": "error", "message": "Invalid data format"}, 400

    try:
        message_info = data["entry"][0]["changes"][0]["value"]
        if "messages" not in message_info:
            return {"status": "error", "message": "No messages found"}, 400

        message = message_info["messages"][0]
        sender_id = message["from"]
        text = message.get("text", {}).get("body", "").lower()

        response_text = await find_best_answer(text)
        response_send = await send_whatsapp_message(sender_id, response_text)

        await log_message(sender_id, text, response_text, response_send)

        if "messages" in response_send:
            return {"status": "success", "message_id": response_send["messages"][0]["id"]}, 200
        else:
            return {"status": "error", "details": response_send}, 500

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
