import telebot
from flask import Flask
import threading

# بياناتك
TOKEN = '8774372608:AAEeBHtIwrtMhck96ftRGPJJlRlSps5aq9w'
ADMIN_ID = '8405924856'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# مسار وهمي عشان موقع UptimeRobot يزوره وميفصلش السيرفر
@app.route('/')
def home():
    return "Bot is awake and running! 🚀"

# رسالة الترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! 🌟\nابعتلي أي صورة هنا، وهتوصل للمسؤول فوراً.")

# استقبال الصور
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.reply_to(message, "تم استلام الصورة وإرسالها بنجاح! 🚀")
    except Exception as e:
        bot.reply_to(message, "عذراً، حدث خطأ أثناء إرسال الصورة.")
        print(f"Error: {e}")

# دالة تشغيل البوت
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل البوت في مسار منفصل (Thread) عشان ما يعطلش الويب
    threading.Thread(target=run_bot).start()
    # تشغيل سيرفر فلاسك
    app.run(host="0.0.0.0", port=8080)
