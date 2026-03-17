import telebot
from telebot import types
import os, socket, threading
from flask import Flask

# الإعدادات
TOKEN = '8776995293:AAEST4B_UAV5D2Ct8El-YNDiynM9Axao770'
WHATSAPP_NUM = "+963964645316"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# نظام البيانات (ملاحظة: تصفّر عند إعادة تشغيل السيرفر في النسخة المجانية)
user_data = {}

@app.route('/')
def index(): return "Syria 2026 Mega System is Active!"

# --- الأوامر الأساسية ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if uid not in user_data:
        user_data[uid] = {'points': 10, 'is_vip': False}
    bot.reply_to(message, "🛡️ **مرحباً بك في Syria 2026 PRO**\nأدخل كلمة السر للاستمرار:")

@bot.message_handler(func=lambda message: message.text == "Syria_2026")
def main_menu(message):
    uid = message.from_user.id
    pts = user_data[uid]['points']
    status = "👑 VIP" if user_data[uid]['is_vip'] else "عادي"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # الفئات الضخمة
    btn_net = types.InlineKeyboardButton("🌐 أدوات الشبكة", callback_data='cat_net')
    btn_sec = types.InlineKeyboardButton("🔒 أدوات الحماية", callback_data='cat_sec')
    btn_vip = types.InlineKeyboardButton("💎 أدوات VIP (مدفوعة)", callback_data='cat_vip')
    
    # نظام الحساب
    btn_pts = types.InlineKeyboardButton(f"💰 نقاطك: {pts}", callback_data='none')
    btn_wa = types.InlineKeyboardButton("💳 شراء اشتراك VIP", url=f"https://wa.me/{WHATSAPP_NUM}")
    
    markup.add(btn_net, btn_sec)
    markup.add(btn_vip)
    markup.add(btn_pts, btn_wa)
    
    bot.send_message(message.chat.id, f"👤 الحساب: {status}\n💰 الرصيد: {pts}\n\nاختر القسم المطلوب:", reply_markup=markup)

# --- معالجة الضغطات ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    uid = call.from_user.id
    
    if call.data == 'cat_net':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📍 استخراج IP", callback_data='tool_ip'),
            types.InlineKeyboardButton("🔙 عودة للقائمة الرئيسية", callback_data='back_main')
        )
        bot.edit_message_text("🌐 **قسم أدوات الشبكة:**", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == 'cat_sec':
        bot.answer_callback_query(call.id, "🛠️ جاري برمجة أدوات الحماية في التحديث القادم!", show_alert=True)

    elif call.data == 'cat_vip':
        if not user_data[uid]['is_vip']:
            bot.answer_callback_query(call.id, "🛑 هذا القسم للمشتركين فقط! تواصل مع المطور.", show_alert=True)
        else:
            bot.send_message(call.message.chat.id, "🔓 أهلاً بك في المنطقة المحظورة VIP!")

    elif call.data == 'back_main':
        main_menu(call.message)

    elif call.data == 'tool_ip':
        msg = bot.send_message(call.message.chat.id, "🔍 أرسل رابط الموقع (مثال: google.com):")
        bot.register_next_step_handler(msg, perform_ip_extraction)

# --- وظائف الأدوات ---
def perform_ip_extraction(message):
    try:
        url = message.text.replace("https://", "").replace("http://", "").split('/')[0]
        ip = socket.gethostbyname(url)
        bot.reply_to(message, f"✅ **تم الاستخراج!**\n🌐 الموقع: {url}\n📍 الـ IP: `{ip}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ خطأ في الرابط!")

# --- التشغيل ---
if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(timeout=20)).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
