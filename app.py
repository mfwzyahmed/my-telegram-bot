import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# هذا السطر مهم جداً لمنصة Vercel لتقرأ الكود
app.debug = True

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if update and "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]
        
        # رد تلقائي سريع للتجربة وعزل المشكلة
        reply = f"تم الاتصال بنجاح! رسالتك هي: {text}"
            
        telegram_url = f"https://telegram.org{TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": chat_id, "text": reply})
        
    return jsonify({"status": "success"})

@app.route('/')
def home():
    return "Bot Server is Active!"
