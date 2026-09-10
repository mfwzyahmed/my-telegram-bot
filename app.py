import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# جلب توكن البوت بأمان من البيئة السحابية
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://telegram.org{TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # قراءة الرسالة ومعرف الشات باحترافية وأمان
    message = data.get("message", {})
    text = message.get("text")
    chat_id = message.get("chat", {}).get("id")
    
    if chat_id and text:
        payload = {
            "chat_id": chat_id,
            "text": f"مرحباً! البوت يعمل الآن بكفاءة المحترفين 🚀\nرسالتك هي: {text}"
        }
        # إرسال الرسالة مع حماية السيرفر من الانهيار في حال فشل الطلب
        try:
            requests.post(TELEGRAM_API, json=payload, timeout=5)
        except requests.exceptions.RequestException:
            pass

    return jsonify({"status": "success"}), 200

@app.route('/')
def index():
    return "Bot Server is Online!", 200
