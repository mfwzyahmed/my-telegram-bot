import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# جلب المتغيرات البيئية التي قمت بإضافتها سابقاً
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
    # استخدام نموذج Hermes المجاني والمستقر عبر OpenRouter
    data = {
        "model": "nousresearch/hermes-3-llama-3.1-8b:free",
        "messages": [{"role": "user", "content": user_message}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except Exception:
        return "عذراً، حدث خطأ أثناء الاتصال بعقل الذكاء الاصطناعي Hermes."

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if "message" in update and "text" in update["message"]:
        chat_id = str(update["message"]["chat"]["id"])
        text = update["message"]["text"]
        
        # التحقق من أنك أنت فقط من يستخدم البوت للحماية
        if ALLOWED_IDS and chat_id not in ALLOWED_IDS:
            return jsonify({"status": "ignored"})
            
        if text == "/start":
            reply = "مرحباً بك! أنا Hermes Agent، عميلك الذكي الشخصي. كيف يمكنني مساعدتك اليوم؟"
        else:
            reply = ask_hermes(text)
            
        telegram_url = f"https://telegram.org{TOKEN}/sendMessage"
        requests.post(telegram_url, json={"chat_id": chat_id, "text": reply})
        
    return jsonify({"status": "success"})

@app.route('/')
def home():
    return "Hermes Bot is Running!"

if __name__ == '__main__':
    app.run(debug=True)
