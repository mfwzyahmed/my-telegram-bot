import os
import urllib.request
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

@app.route('/api/webhook', methods=['POST'])
def telegram_webhook_handler():
    try:
        data = request.get_json(force=True) or {}
        message = data.get("message", {})
        text = message.get("text")
        chat_id = message.get("chat", {}).get("id")
        
        if chat_id and text and TOKEN:
            reply_text = f"تم استقبال رسالتك بنجاح! لقد كتبت لي: {text}"
            
            # تصحيح الرابط الرسمي لـ Telegram API
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            
            payload = {
                "chat_id": chat_id, 
                "text": reply_text
            }
            
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=8)
            
    except Exception as e:
        print(f"Error handling webhook: {e}")
        
    return jsonify({"status": "success"}), 200

@app.route('/')
def index():
    return "Hermes Bot Server is Active and Running!"
