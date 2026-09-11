import os
import json
import urllib.request
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

@app.route('/api/webhook', methods=['POST']) 
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True, silent=True) or {}
        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if chat_id and text and TOKEN:
            reply_text = f"تم استقبال رسالتك بنجاح! لقد كتبت لي: {text}"
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            
            payload = json.dumps({
                "chat_id": chat_id,
                "text": reply_text
            }).encode('utf-8')
            
            req = urllib.request.Request(
                url, 
                data=payload, 
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"Error: {e}")

    return jsonify({"status": "ok"}), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return "Hermes Bot Server is Active!", 200

if __name__ == '__main__':
    app.run()
