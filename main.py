import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)
from deep_translator import GoogleTranslator

# توکن ربات
TOKEN = "8588183259:AAEO38uYwX6_rzafp3wKKCxDfa_7HXTJNPc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🦇 **به ربات مترجم پیشرفته خوش آمدید!**\n\n"
        "من آماده‌ام تا متن‌های شما را از هر زبانی به **فارسی** روان ترجمه کنم.\n\n"
        "🛠 **راهنما:** کافیست روی پیامی که می‌خواهید ترجمه شود ریپلی بزنید و دستور `/farsi` را ارسال کنید.\n\n"
        "👨‍💻 **سازنده:** @batman1792"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def translate_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    
    # بررسی اینکه آیا کاربر روی پیامی ریپلی زده است یا خیر
    if message.reply_to_message and message.reply_to_message.text:
        text_to_translate = message.reply_to_message.text
        
        try:
            # ترجمه خودکار از هر زبانی به فارسی (پشتیبانی از تمام زبان‌ها)
            translated = GoogleTranslator(source='auto', target='fa').translate(text_to_translate)
            
            response_text = f"🌐 **ترجمه به فارسی:**\n\n{translated}"
            await message.reply_to_message.reply_text(response_text, parse_mode="Markdown")
        except Exception as e:
            await message.reply_text("❌ متأسفانه در فرآیند ترجمه خطایی رخ داد. لطفاً دوباره تلاش کنید.")
    else:
        await message.reply_text("⚠️ لطفاً روی یک پیام متنی ریپلی بزنید و دستور `/farsi` را بفرستید.")

if __name__ == '__main__':
    # ساخت اپلیکیشن ربات
    app = ApplicationBuilder().token(TOKEN).build()

    # ثبت دستورات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("farsi", translate_reply))

    print("Bot is up and running...")
    app.run_polling()
