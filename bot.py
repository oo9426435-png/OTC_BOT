import os
import telebot
from flask import Flask
from threading import Thread

# سحب التوكن تلقائياً من إعدادات البيئة في المنصة للأمان
TOKEN = "8542925328:AAEGzXEmJEQUUP9bKk7Pa6piO7ftBUn735k"
bot = telebot.TeleBot(TOKEN)

# سيرفر ويب بسيط لكي يبقى البوت نشطاً 24/7 ولا ينام
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# أوامر البوت الأساسية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك! البوت يعمل الآن على السحاب بنجاح تام 🚀")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, "تم استلام رسالتك، البوت شغال!")

if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    bot.infinity_polling()
