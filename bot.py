import telebot
from telebot import types
import os
import requests
import threading
from flask import Flask

# التوكن الجديد الخاص بك
TOKEN = '8776995293:AAEST4B_UAV5D2Ct8El-YNDiynM9Axao770'
bot = telebot.TeleBot(TOKEN)

# إنشاء تطبيق ويب بسيط لإرضاء سيرفر Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running perfectly!"

# دالة الترحيب
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🛡️ **مرحباً بك في سوريا 2026**\nأدخل كلمة السر للاستمرار:")

# التحقق من كلمة السر
@bot.message_handler(func=lambda message: message.text == "Syria_2026")
def check_pass(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🌐 استخراج IP", callback_data='extract_ip')
    btn2 = types.InlineKeyboardButton("🚀 فحص السرعة", callback_data='speed_test')
    btn3 = types.InlineKeyboardButton("🧠 تحليل Gemini", callback_data='gemini_analysis')
    
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "✅ تم التحقق! اختر أداتك من لوحة تحكم حسين:", reply_markup=markup)

# معالجة ضغطات الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "extract_ip":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🔍 أرسل الرابط الآن لاستخراج الـ IP منه:")
    
    elif call.data == "speed_test":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "⚡ جاري فحص سرعة السيرفر... يرجى الانتظار.")
    
    elif call.data == "gemini_analysis":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🤖 أنا جاهز للتحليل، أرسل نصك الآن.")

# تشغيل البوت والويب سيرفر معاً
if __name__ == "__main__":
    # تشغيل استماع البوت في خيط (Thread) منفصل
    bot_thread = threading.Thread(target=lambda: bot.infinity_polling(timeout=20, long_polling_timeout=10))
    bot_thread.start()
    
    # تشغيل خادم الويب على المنفذ الذي يطلبه Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
