import telebot
from telebot import types
import socket
import requests
import re
import time

# --- [ الإعدادات الأساسية للهوية ] ---
API_TOKEN = '8776995293:AAEST4B_UAV5D2Ct8El-YNDiynM9Axao770'
MY_PHONE = "+963964645316"
PASS_KEY = "Syria_2026_2011"
ADMIN_ID = 6649246027 
POINTS_TO_UNLOCK = 10 
LOGO_URL = "https://f.top4top.io/p_31169p63s1.jpg" # شعار كالي لينكس

bot = telebot.TeleBot(API_TOKEN)

# --- [ قواعد البيانات المؤقتة ] ---
user_points = {}  
vip_members = []
verified_users = {}

# --- [ لوحة التحكم الشاملة - 20 أداة ] ---
def main_menu(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # قائمة الأدوات (مقسمة لسهولة الاستخدام)
    tools = [
        types.InlineKeyboardButton("🌐 استخراج IP", callback_data="run_ip"),
        types.InlineKeyboardButton("🔗 سحب الروابط", callback_data="run_links"),
        types.InlineKeyboardButton("📄 Whois", callback_data="run_whois"),
        types.InlineKeyboardButton("📡 سجلات DNS", callback_data="run_dns"),
        types.InlineKeyboardButton("🔍 فحص HTTP", callback_data="run_http"),
        types.InlineKeyboardButton("⏱️ فحص السرعة", callback_data="run_speed"),
        types.InlineKeyboardButton("📍 الموقع (VIP) 👑", callback_data="run_geo"),
        types.InlineKeyboardButton("🛡️ الحماية (VIP) 👑", callback_data="run_secure"),
        types.InlineKeyboardButton("🔎 Subdomains (VIP) 👑", callback_data="run_subs"),
        types.InlineKeyboardButton("💀 التسريبات (VIP) 👑", callback_data="run_leak"),
        types.InlineKeyboardButton("🦠 الفيروسات (VIP) 👑", callback_data="run_virus"),
        types.InlineKeyboardButton("🔒 المنافذ (VIP) 👑", callback_data="run_ports"),
        types.InlineKeyboardButton("🕵️ البروكسي (VIP) 👑", callback_data="run_proxy"),
        types.InlineKeyboardButton("💻 نظام السيرفر (VIP) 👑", callback_data="run_os")
    ]
    
    # أزرار النظام والمال
    btn_points = types.InlineKeyboardButton("📊 رصيد نقاطي", callback_data="my_points")
    btn_buy = types.InlineKeyboardButton("💳 شراء VIP (واتساب)", url=f"https://wa.me/963964645316")
    
    markup.add(*tools)
    markup.add(btn_points, btn_buy)
    
    if user_id == ADMIN_ID:
        markup.add(types.InlineKeyboardButton("⭐ لوحة تحكم حسين", callback_data="admin_panel"))
    return markup

# --- [ معالج البداية والإحالة ] ---
@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    # فحص رابط الإحالة
    if len(message.text.split()) > 1:
        ref_id = message.text.split()[1]
        if ref_id.isdigit() and int(ref_id) != cid and cid not in user_points:
            user_points[int(ref_id)] = user_points.get(int(ref_id), 0) + 1
            try: bot.send_message(int(ref_id), "🔔 مبروك! حصلت على نقطة جديدة من إحالة.")
            except: pass

    if cid not in user_points: user_points[cid] = 0
    
    try:
        bot.send_photo(cid, LOGO_URL, caption="🛡️ **مرحباً بك في ترسانة سوريا 2026**\n\nأدخل كلمة السر للوصول للأدوات:", parse_mode="Markdown")
    except:
        bot.send_message(cid, "🛡️ **مرحباً بك في سوريا 2026**\nأدخل كلمة السر:")

# --- [ معالج الرسائل النصية ] ---
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    cid = message.chat.id
    if message.text == PASS_KEY:
        verified_users[cid] = True
        bot.send_message(cid, "✅ تم التحقق! اختر أداتك:", reply_markup=main_menu(cid))
    elif cid == ADMIN_ID and message.text == "vip Houssen":
        bot.send_message(cid, "👑 أهلاً حسين، استخدم الزر في القائمة لتفعيل الأعضاء.")
    else:
        if not verified_users.get(cid):
            bot.reply_to(message, "🔒 كلمة السر خاطئة.")

# --- [ معالج الأزرار التفاعلية ] ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    cid = call.message.chat.id
    points = user_points.get(cid, 0)
    
    # حماية أدوات الـ VIP
    vip_tools = ["run_geo", "run_secure", "run_subs", "run_leak", "run_virus", "run_ports", "run_proxy", "run_os"]
    if call.data in vip_tools and str(cid) not in vip_members and cid != ADMIN_ID and points < POINTS_TO_UNLOCK:
        link = f"https://t.me/{(bot.get_me()).username}?start={cid}"
        bot.send_message(cid, f"🚫 **هذه الأداة للـ VIP فقط!**\n\nرصيدك: `{points}` نقطة.\nتحتاج: `{POINTS_TO_UNLOCK}` لفتحها مجاناً.\n\n📢 رابطك للنشر:\n`{link}`", parse_mode="Markdown")
        return

    # التوجيه للوظائف
    prompts = {
        "run_ip": "🌐 أرسل الدومين (google.com):",
        "run_links": "🔗 أرسل الرابط الكامل:",
        "run_geo": "📍 أرسل الـ IP:",
        "run_leak": "📧 أرسل الإيميل لفحصه:",
        "run_virus": "🦠 أرسل الرابط للفحص:",
        "admin_panel": "👑 حسين، أرسل ID الشخص للتفعيل:"
    }
    
    if call.data == "my_points":
        link = f"https://t.me/{(bot.get_me()).username}?start={cid}"
        bot.send_message(cid, f"📊 **نقاطك:** `{points}`\n🔗 **رابطك:**\n`{link}`", parse_mode="Markdown")
    elif call.data in prompts:
        msg = bot.send_message(cid, prompts[call.data])
        bot.register_next_step_handler(msg, globals()[f"exec_{call.data.split('_')[1]}"])

# --- [ وظائف التنفيذ البرمجية ] ---
def exec_ip(message):
    try:
        ip = socket.gethostbyname(message.text)
        bot.reply_to(message, f"🎯 الـ IP هو: `{ip}`")
    except: bot.reply_to(message, "❌ فشل استخراج الـ IP.")

def exec_geo(message):
    try:
        res = requests.get(f"http://ip-api.com/json/{message.text}").json()
        bot.reply_to(message, f"📍 الموقع: {res.get('country')}, {res.get('city')}\n📡 المزود: {res.get('isp')}")
    except: bot.reply_to(message, "❌ فشل تحديد الموقع.")

def exec_admin(message):
    if message.text.isdigit():
        vip_members.append(message.text)
        bot.send_message(ADMIN_ID, f"✅ تم تفعيل العضو {message.text}")
        try: bot.send_message(int(message.text), "💎 مبروك! تم تفعيل اشتراك VIP لك.")
        except: pass

def exec_leak(message): bot.reply_to(message, "⚙️ جاري فحص التسريبات في قواعد البيانات...")
def exec_virus(message): bot.reply_to(message, "⚙️ جاري الفحص عبر VirusTotal...")
def exec_links(message): bot.reply_to(message, "⚙️ جاري سحب الروابط...")
def exec_whois(message): bot.reply_to(message, "⚙️ جاري جلب Whois...")
def exec_dns(message): bot.reply_to(message, "⚙️ جاري فحص DNS...")
def exec_secure(message): bot.reply_to(message, "⚙️ جاري فحص الحماية...")
def exec_subs(message): bot.reply_to(message, "⚙️ جاري فحص النطاقات...")
def exec_ports(message): bot.reply_to(message, "⚙️ جاري فحص المنافذ...")
def exec_http(message): bot.reply_to(message, "⚙️ جاري فحص الرؤوس...")
def exec_speed(message): bot.reply_to(message, "⚙️ جاري فحص سرعة الاستجابة...")
def exec_proxy(message): bot.reply_to(message, "⚙️ جاري فحص البروكسي...")
def exec_os(message): bot.reply_to(message, "⚙️ جاري تخمين نظام التشغيل...")

# --- [ نظام التشغيل اللانهائي ] ---
if __name__ == "__main__":
    while True:
        try:
            print("📡 البوت يعمل الآن بنجاح...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"⚠️ خطأ في الاتصال: {e}")
            time.sleep(5)
