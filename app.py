import os
import urllib.request
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# سطر إجباري لجعل السيرفر مرئياً لمنصة Vercel
app.debug = True

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

@app.route('/webhook', methods=['POST'])
def telegram_webhook_handler():
    try:
        data = request.get_json(force=True)
        message = data.get("message", {})
        text = message.get("text")
        chat_id = message.get("chat", {}).get("id")
        
        if chat_id and text:
            # رد تلقائي ثابت ومباشر
            reply_text = f"تم استقبال رسالتك بنجاح! لقد كتبت لي: {text}"
            url = f"https://telegram.org{TOKEN}/sendMessage"
            
            payload = {"chat_id": chat_id, "text": reply_text}
            
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass
        
    return jsonify({"status": "success"}), 200

@app.route('/')
def index():
    return "Bot Server is Active and Running!"

# السطر الذهبي لتشغيل التطبيق كـ WSGI على Vercel
if __name__ == '__main__':
    app.run()
