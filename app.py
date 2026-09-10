import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USERS = os.getenv("TELEGRAM_ALLOWED_USERS", "")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

ALLOWED_IDS = [id.strip() for id in ALLOWED_USERS.split(",") if id.strip()]

def ask_hermes(user_message):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "nousresearch/hermes-3-llama-3.1-8b:free",
        "messages": [{"role": "user", "content": user_message}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices']['message']['content']
    except Exception:
        return "Error connecting to Hermes AI."

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if update and "message" in update and "text" in update["message"]:
        chat_id = str(update["message"]["chat"]["id"])
        text = update["message"]["text"]
        
        if ALLOWED_IDS and chat_id not in ALLOWED_IDS:
            return jsonify({"status": "ignored"})
            
        if text == "/start":
            reply = "Welcome! I am Hermes Agent, your AI assistant."
        else:
            reply = ask_hermes(text)
            
        telegram_url = f"https://telegram.org{TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": chat_id, "text": reply})
        
    return jsonify({"status": "success"})

@app.route('/')
def home():
    return "Hermes Bot is Active and Healthy!"
