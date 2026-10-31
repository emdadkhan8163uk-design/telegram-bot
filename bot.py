import telebot
from telebot import types
import requests
import threading

# আপনার বটের টোকেন এবং এডমিন আইডি
TOKEN = '9205333490:AAEEFUCbfbmISAPHmaGxG2qSR7HvJ7PrR3U'  
ADMIN_ID = 8502631459      

bot = telebot.TeleBot(TOKEN)

# পেমেন্ট নম্বর
PAYMENT_NUMBER = "01742103310"

# ইউজারের সিলেক্ট করা প্যাকেজ মনে রাখার জন্য
user_selected_package = {}

# ফ্রিতে টিকটক ভিডিওতে ভিউজ পাঠানোর ফাংশন
def send_tiktok_views(video_url, count):
    def boost():
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        success = 0
        for _ in range(int(count)):
            try:
                response = requests.get(video_url, headers=headers, timeout=5)
                if response.status_code == 200:
                    success += 1
            except:
                pass
        print(f"Target: {video_url} | Views Sent: {success}/{count}")

    threading.Thread(target=boost).start()

@bot.message_handler(commands=['start'])
def start_msg(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🔥 প্যাকেজ ও প্রাইসিং", callback_data="packages"),
        types.InlineKeyboardButton("🎁 ফ্রি লাইক/ভিউজ", callback_data="free"),
        types.InlineKeyboardButton("📞 হেল্প ও যোগাযোগ", callback_data="help")
    )
    bot.send_message(message.chat.id, "স্বাগতম! আপনার টিকটক ভিডিওর ভিউজ ও লাইক বাড়াতে নিচের অপশনগুলো দেখুন:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    chat_id = call.message.chat.id
    
    if call.data == "packages":
        text = (
            "📦 **আমাদের আকর্ষণীয় প্যাকেজসমূহ:**\n\n"
            "💎 **প্যাকেজ ১:** ১০০০ ভিউজ + ১০০ লাইক = **৫০ টাকা**\n"
            "💎 **প্যাকেজ ২:** ৫০০০ ভিউজ + ৫০০ লাইক = **২০০ টাকা**\n"
            "💎 **প্যাকেজ ৩:** ১০০০ টিকটক ফলোয়ার = **১৫০ টাকা**\n"
            "💎 **প্যাকেজ ৪:** মেগা প্যাক (১০,০০০ ভিউজ + ১,০০০ লাইক) = **৩৫০ টাকা**\n\n"
            "আপনার পছন্দের প্যাকেজটি নিচে থেকে সিলেক্ট করুন:"
        )
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("প্যাকেজ ১ (৫০ ৳)", callback_data="pkg_1"),
            types.InlineKeyboardButton("প্যাকেজ ২ (২০০ ৳)", callback_data="pkg_2"),
            types.InlineKeyboardButton("প্যাকেজ ৩ (১৫০ ৳)", callback_data="pkg_3"),
            types.InlineKeyboardButton("প্যাকেজ ৪ (৩৫০ ৳)", callback_data="pkg_4"),
            types.InlineKeyboardButton("🔙 মূল মেনু", callback_data="main_menu")
        )
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        
    elif call.data.startswith("pkg_"):
        pkg_no = call.data.split("_")[1]
        
        # প্যাকেজ অনুযায়ী নাম ও মূল্য সেট করা
        if pkg_no == "1":
            pkg_name = "প্যাকেজ ১ (১০০০ ভিউজ + ১০০ লাইক)"
            price = "50"
        elif pkg_no == "2":
            pkg_name = "প্যাকেজ ২ (৫০০০ ভিউজ + ৫০০ লাইক)"
            price = "200"
        elif pkg_no == "3":
            pkg_name = "প্যাকেজ ৩ (১০০০ ফলোয়ার)"
            price = "150"
        else:
            pkg_name = "প্যাকেজ ৪ (মেগা প্যাক: ১০,০০০ ভিউজ + ১০০০ লাইক)"
            price = "350"
            
        user_selected_package[chat_id] = pkg_name
        
        text = (
            f"🛒 আপনি **{pkg_name}** সিলেক্ট করেছেন যার মূল্য **{price} টাকা**।\n\n"
            f"💳 এখন পেমেন্ট করার জন্য নিচের মাধ্যমগুলো থেকে একটি সিলেক্ট করুন:"
        )
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup.add(
            types.InlineKeyboardButton("বিকাশ (bKash)", callback_data=f"pay_bkash_{price}"),
            types.InlineKeyboardButton("নগদ (Nagad)", callback_data=f"pay_nagad_{price}"),
            types.InlineKeyboardButton("উপায় (Upay)", callback_data=f"pay_upay_{price}")
        )
        markup.add(types.InlineKeyboardButton("🔙 প্যাকেজ মেনুতে যান", callback_data="packages"))
        bot.edit_message_text(text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        
    elif call.data.startswith("pay_"):
        parts = call.data.split("_")
        method = parts[1].capitalize()
        price = parts[2]
        
        instruct = (
            f"📲 **{method} পেমেন্ট নির্দেশিকা**\n\n"
            f"দয়া করে আমাদের নিচের পার্সোনাল নম্বরে **{price} টাকা** `Send Money` বা `Cash Out` করুন:\n"
            f"👉 `{PAYMENT_NUMBER}` (Personal)\n\n"
            f"টাকা পাঠানো সফল হলে আপনার **TrxID** এবং যে ভিডিওতে ভিউজ নিতে চান তার **TikTok Link** একসাথে এই চ্যাটে লিখে পাঠান!\n\n"
            f"✍️ *উদাহরণ:* `TrxID987654 https://vm.tiktok.com/...`"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 প্যাকেজে ফিরে যান", callback_data="packages"))
        bot.edit_message_text(instruct, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "free":
        text = "🎁 ফ্রি লাইক ও ভিউজ ফিচারটি খুব শীঘ্রই চালু করা হবে। সাথেই থাকুন!"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনু", callback_data="main_menu"))
        bot.edit_message_text(text, chat_id, call.message.message_id, reply_markup=markup)

    elif call.data == "help":
        help_text = (
            "📞 **সাহায্য ও সাপোর্ট**\n\n"
            "পেমেন্ট বা অর্ডার সংক্রান্ত যে কোনো সমস্যায় সরাসরি আমাদের সাথে WhatsApp-এ যোগাযোগ করুন:\n\n"
            "📱 WhatsApp নম্বর: `01926410259`"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 মূল মেনু", callback_data="main_menu"))
        bot.edit_message_text(help_text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "main_menu":
        start_msg(call.message)

@bot.message_handler(func=lambda message: True)
def get_user_submission(message):
    chat_id = message.chat.id
    user_text = message.text
    user_name = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    
    if chat_id != ADMIN_ID:
        pkg_name = user_selected_package.get(chat_id, "নির্দিষ্ট প্যাকেজ সিলেক্ট করেনি")
        
        forward_text = (
            f"🔔 **নতুন অর্ডার এসেছে!**\n\n"
            f"👤 ইউজারের নাম: {user_name}\n"
            f"🆔 টেলিগ্রাম আইডি: `{chat_id}`\n"
            f"📦 সিলেক্টকৃত প্যাকেজ: **{pkg_name}**\n"
            f"✍️ ইউজারের তথ্য (TrxID ও লিংক): \n`{user_text}`\n\n"
            f"⚙️ ভিউজ পাঠানোর কমান্ড:\n"
            f"`/send {chat_id} [ভিডিও_লিংক] [পরিমাণ]`"
        )
        bot.send_message(ADMIN_ID, forward_text, parse_mode="Markdown")
        bot.reply_to(message, "✅ আপনার পেমেন্ট তথ্য এবং লিংকটি সফলভাবে জমা হয়েছে। চেক করে দ্রুত আপনার অর্ডারের কাজ শুরু করে দেওয়া হবে!")
        
    elif chat_id == ADMIN_ID and user_text.startswith("/send"):
        try:
            parts = user_text.split()
            target_chat_id = parts[1]
            video_url = parts[2]
            amount = parts[3]
            
            send_tiktok_views(video_url, amount)
            
            bot.send_message(
                target_chat_id, 
                f"🎉 সুখবর! আপনার অর্ডারের কাজ শুরু হয়ে গেছে।\n"
                f"✅ পাঠানো হচ্ছে: {amount} ভিউজ।"
            )
            bot.send_message(ADMIN_ID, f"✅ সফল! {amount} টি ভিউজ পাঠানোর প্রসেস শুরু হয়েছে।")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"❌ ভুল ফরম্যাট! সঠিক নিয়মে লিখুন:\n`/send chat_id video_url amount`")

if __name__ == "__main__":
    print("Bot is running smoothly...")
    bot.infinity_polling()