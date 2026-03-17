import telebot
from telebot import types
import os, socket, threading
from flask import Flask

TOKEN = '8776995293:AAEST4B_UAV5D2Ct8El-YNDiynM9Axao770'
WHATSAPP_NUM = "+963964645316"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# قاعدة بيانات مؤقتة للمستخدمين
user_data = {} 

@app.route('/')
def index(): return "Syria 2026 Mega Bot is Online!"

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if uid not in user_data:
        user_data[uid] = {'points': 10, 'is_vip': False} # نعطي 10 نقاط هدية
    bot.reply_to(message, "🛡️ **مرحباً بك في Syria 2026 PRO**\nأدخل كلمة السر:")

@bot.message_handler(func=lambda message: message.text == "Syria_2026")
def main_menu(message):
    uid = message.from_user.id
    pts = user_data[uid]['points']
    status = "👑 VIP" if user_data[uid]['is_vip'] else "عادي"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # --- توزيع الأدوات الـ 20 على فئات ---
    btn_net = types.InlineKeyboardButton("🌐 أدوات الشبكة (5)", callback_data='cat_net')
    btn_sec = types.InlineKeyboardButton("🔒 أدوات الحماية (5)", callback_data='cat_sec')
    btn_vip = types.InlineKeyboardButton("💎 أدوات VIP (10)", callback_data='cat_vip')
    
    # --- أزرار الحساب ---
    btn_pts = types.InlineKeyboardButton(f"💰 نقاطك: {pts}", callback_data='none')
    btn_wa = types.InlineKeyboardButton("💳 شراء VIP", url=f"https://wa.me/{WHATSAPP_NUM}")
    
    markup.add(btn_net, btn_sec)
    markup.add(btn_vip)
    markup.add(btn_pts, btn_wa)
    
    bot.send_message(message.chat.id, f"📊 حالتك: {status} | رصيدك: {pts}\nاختر الفئة المطلوبة:", reply_markup=markup)

# معالجة الفئات والأدوات
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    uid = call.from_user.id
    
    if call.data == 'cat_net':
        markup = types.InlineKeyboardMarkup()
        # هنا تضع الـ 5 أدوات الخاصة بالشبكة
        markup.add(types.InlineKeyboardButton("📍 استخراج IP", callback_data='extract_ip'))
        markup.add(types.InlineKeyboardButton("🔙 عودة", callback_data='back_main'))
        bot.edit_message_text("🌐 **أدوات الشبكة:**", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'cat_vip':
        if not user_data[uid]['is_vip']:
            bot.answer_callback_query(call.id, "🛑 هذه الفئة للمشتركين فقط!", show_alert=True)
        else:
            bot.send_message(call.message.chat.id, "🔓 أهلاً بك في قسم الـ VIP الضخم!")

    elif call.data == 'back_main':
        main_menu(call.message)

# --- تشغيل البوت ---
if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(timeout=20)).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
