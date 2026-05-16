import os
import telebot

TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "أهلاً بك في بوت قناة Min Al-Sifr Tech! 🚀\n"
        "أرسل لي سكرين شوت أو صورة الإيموجيز المخفية للمشاركة في السحب.",
    )


@bot.message_handler(content_types=['photo', 'document'])
def handle_docs_photo(message):
    try:
        bot.forward_message(ADMIN_CHAT_ID, message.chat.id, message.message_id)
        bot.reply_to(message, "تم استلام الصورة بنجاح! 🎯 بالتوفيق في الجيف أواي.")
    except Exception as e:
        print(f"Error forwarding message: {e}")
        bot.reply_to(message, "عذراً، حدث خطأ أثناء الإرسال. تأكد من إرسال الصورة بشكل صحيح.")


if __name__ == "__main__":
    print("البوت يعمل الآن ومستعد لاستقبال الصور...")
    bot.infinity_polling(none_stop=True, timeout=60, long_polling_timeout=60)
