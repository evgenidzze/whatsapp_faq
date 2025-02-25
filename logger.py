import logging
import json
from logging.handlers import RotatingFileHandler
import os

log_directory = '/app/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, 'chatbot_logs.json')

log_formatter = logging.Formatter('%(message)s')

log_handler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("chatbot")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


async def log_message(sender_id, text, response, send_status):
    """Логування повідомлення у JSON (вхідне + вихідне)"""
    log_entry = {
        "sender_id": sender_id,
        "received_text": text,
        "response_text": response,
        "whatsapp_api_response": send_status
    }
    logger.info(json.dumps(log_entry, ensure_ascii=False))
