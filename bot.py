import telebot
from telebot import types
import os
import requests

# ضع التوكن الخاص بك هنا
TOKEN = 'ضع_التوكن_هنا'
bot = telebot.TeleBot(TOKEN)

# دالة الترحيب وكلمة السر
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🛡️ **مرحباً بك في سوريا 2026**\nأدخل كلمة السر للاستمرار:")

@bot.message_handler(func=lambda message: message.text == "Syria_2026")
def check_pass(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # تعريف الأزرار
    btn1 = types.InlineKeyboardButton("🌐 استخراج IP", callback_data='extract_ip')
    btn2 = types.InlineKeyboardButton("🚀 فحص السرعة", callback_data='speed_test')
    btn3 = types.InlineKeyboardButton("🧠 تحليل Gemini", callback_data='gemini_analysis')
    
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "✅ تم التحقق! اختر أداتك:", reply_markup=markup)

# معالجة ضغطات الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "extract_ip":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🔍 أرسل الرابط لاستخراج الـ IP منه:")
    
    elif call.data == "speed_test":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "⚡ جاري فحص سرعة السيرفر... انتظر لحظة.")
        # هنا تضع كود الفحص لاحقاً
    
    elif call.data == "gemini_analysis":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🤖 أرسل النص الذي تريد تحليله:")

# الجزء الأهم لعمل الأزرار في Render (حل مشكلة الـ Port)
if __name__ == "__main__":
    # هذا الجزء يخبر Render أن البوت يعمل كخادم ويب بسيط
    # مما يمنع رسالة "No open ports detected" ويجعل الأزرار تستجيب
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Bot is running!"

    # تشغيل البوت في الخلفية
    import threading
    threading.Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5)).start()
    
    # تشغيل "خادم وهمي" لاستقبال طلبات Render على الـ Port
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
