import telebot
from telebot import types
import os, threading, time, socket
from flask import Flask

# --- الإعدادات ---
TOKEN = '8776995293:AAEST4B_UAV5D2Ct8El-YNDiynM9Axao770'
WHATSAPP = "+963964645316"
bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=20)
app = Flask(__name__)

# قاعدة بيانات وهمية (تصفّر عند ريستارت السيرفر)
user_data = {}

@app.route('/')
def index(): return "Syria 2026 Ultimate System is Online!"

# --- دوال المساعدة ---
def get_user_info(uid):
    if uid not in user_data:
        user_data[uid] = {'points': 15, 'is_vip': False, 'name': ''}
    return user_data[uid]

# --- القائمة الرئيسية ---
def send_main_menu(message, edit=False):
    uid = message.from_user.id
    info = get_user_info(uid)
    status = "👑 VIP" if info['is_vip'] else "👤 عادي"
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # توزيع الـ 20 أداة في فئات ضخمة
    btn1 = types.InlineKeyboardButton("🌐 أدوات الشبكة (5)", callback_data='cat_net')
    btn2 = types.InlineKeyboardButton("🔒 أدوات الحماية (5)", callback_data='cat_sec')
    btn3 = types.InlineKeyboardButton("🤖 ذكاء اصطناعي (5)", callback_data='cat_ai')
    btn4 = types.InlineKeyboardButton("💎 أدوات VIP مخصصة (5)", callback_data='cat_vip')
    
    # نظام الحساب
    btn5 = types.InlineKeyboardButton(f"💰 نقاطك: {info['points']}", callback_data='check_points')
    btn6 = types.InlineKeyboardButton("💳 ترقية لـ VIP", url=f"https://wa.me/{WHATSAPP}")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    text = (f"🛡️ **لوحة تحكم سوريا PRO 2026**\n\n"
            f"📊 **حالة الحساب:** {status}\n"
            f"💰 **رصيد النقاط:** {info['points']}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"اختر الفئة التي تريد البدء بها يا بطل:")
    
    if edit:
        bot.edit_message_text(text, message.chat.id, message.message_id, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# --- معالجة الأوامر ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 **أهلاً بك في أقوى بوت خدمات لعام 2026**\n\n🔑 أرسل كلمة السر للدخول:")

@bot.message_handler(func=lambda message: message.text == "Syria_2026")
def access_granted(message):
    user_data[message.from_user.id] = get_user_info(message.from_user.id)
    send_main_menu(message)

# --- معالجة الأزرار (النظام الضخم) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    uid = call.from_user.id
    info = get_user_info(uid)
    
    # إخبار تليجرام باستلام الضغطة فوراً (هام جداً)
    bot.answer_callback_query(call.id)

    if call.data == "cat_net":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📍 استخراج IP موقع", callback_data='tool_ip'),
            types.InlineKeyboardButton("📡 فحص Ping السيرفر", callback_data='tool_ping'),
            types.InlineKeyboardButton("🔙 عودة للقائمة", callback_data='back_home')
        )
        bot.edit_message_text("🌐 **أدوات الشبكة المتاحة:**", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "cat_vip" or call.data == "cat_sec":
        if not info['is_vip']:
            bot.answer_callback_query(call.id, "❌ عذراً! هذه الفئة تتطلب اشتراك VIP مدفوع.", show_alert=True)
        else:
            bot.send_message(call.message.chat.id, "🔓 تم فتح الأدوات المتقدمة لك!")

    elif call.data == "back_home":
        send_main_menu(call.message, edit=True)

    elif call.data == "tool_ip":
        msg = bot.send_message(call.message.chat.id, "🔍 **أرسل رابط الموقع لاستخراج الـ IP:**\n(مثال: google.com)")
        bot.register_next_step_handler(msg, ip_tool_logic)

# --- منطق الأدوات ---
def ip_tool_logic(message):
    try:
        host = message.text.replace("https://", "").replace("http://", "").split('/')[0]
        ip = socket.gethostbyname(host)
        bot.reply_to(message, f"✅ **تم الاستخراج بنجاح!**\n\n🌐 **الموقع:** {host}\n📍 **الـ IP:** `{ip}`", parse_mode="Markdown")
    except:
        bot.reply_to(message, "❌ فشل الاستخراج، تأكد من الرابط.")

# --- تشغيل النظام ---
def run_polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except:
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_polling).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
