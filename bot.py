import telebot
from telebot import types
import os, threading
from flask import Flask

# الإعدادات الأساسية
TOKEN = '8776995293:AAEST4B_UAV5D2Ct8El-YNDiynM9Axao770'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# قاعدة بيانات وهمية للمستخدمين
user_data = {}

@app.route('/')
def index(): return "Syria 2026 PRO is Live!"

# دالة الترحيب
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if uid not in user_data:
        user_data[uid] = {'points': 10, 'is_vip': False}
    bot.reply_to(message, "🛡️ **مرحباً بك في Syria 2026 PRO**\nأدخل كلمة السر للاستمرار:")

# التحقق من كلمة السر وإظهار الأزرار
@bot.message_handler(func=lambda message: message.text == "Syria_2026")
def show_menu(message):
    uid = message.from_user.id
    pts = user_data[uid]['points']
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🌐 أدوات الشبكة (5)", callback_data='cat_net')
    btn2 = types.InlineKeyboardButton("🔒 أدوات الحماية (5)", callback_data='cat_sec')
    btn3 = types.InlineKeyboardButton("💎 أدوات VIP (10)", callback_data='cat_vip')
    btn4 = types.InlineKeyboardButton(f"💰 نقاطك: {pts}", callback_data='points_info')
    btn5 = types.InlineKeyboardButton("💳 شراء VIP", url="https://wa.me/+963964645316")
    
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, "📊 حالتك: عادي | رصيدك: 10\nاختر الفئة المطلوبة:", reply_markup=markup)

# --- الجزء الأهم: معالجة ضغطات الأزرار ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'cat_net':
        # تحديث الرسالة بدلاً من إرسال واحدة جديدة ليظهر كأنه تطبيق
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📍 استخراج IP", callback_data='tool_ip'))
        markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data='back_to_main'))
        bot.edit_message_text("🌐 **أدوات الشبكة المتاحة:**", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == 'back_to_main':
        # العودة للقائمة الرئيسية
        show_menu(call.message)
        
    elif call.data == 'cat_vip' or call.data == 'cat_sec':
        bot.answer_callback_query(call.id, "🛑 هذا القسم مغلق حالياً، تواصل مع المطور لتفعيله!", show_alert=True)

# تشغيل البوت مع الويب سيرفر
def run_bot():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
