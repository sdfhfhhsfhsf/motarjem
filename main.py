import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)
from deep_translator import GoogleTranslator

TOKEN = "8588183259:AAEO38uYwX6_rzafp3wKKCxDfa_7HXTJNPc"

app = FastAPI()

# راه‌اندازی اپلیکیشن تلگرام
telegram_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "🦇 **به ربات مترجم پیشرفته خوش آمدید!**\n\n"
        "من آماده‌ام تا متن‌های شما را از هر زبانی به **فارسی** روان ترجمه کنم.\n\n"
        "🛠 **راهنما در گروه‌ها و پی‌وی:** کافیست روی پیامی که می‌خواهید ترجمه شود ریپلی بزنید و دستور `/farsi` را ارسال کنید.\n\n"
        "👨‍💻 **سازنده:** @batman1792"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def translate_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    
    # بررسی ریپلی روی پیام متنی
    if message.reply_to_message and message.reply_to_message.text:
        text_to_translate = message.reply_to_message.text
        try:
            # ترجمه خودکار از هر زبانی به فارسی
            translated = GoogleTranslator(source='auto', target='fa').translate(text_to_translate)
            response_text = f"🌐 **ترجمه به فارسی:**\n\n{translated}"
            await message.reply_to_message.reply_text(response_text, parse_mode="Markdown")
        except Exception as e:
            await message.reply_text("❌ متأسفانه در فرآیند ترجمه خطایی رخ داد. لطفاً دوباره تلاش کنید.")
    else:
        await message.reply_text("⚠️ لطفاً روی یک پیام متنی ریپلی بزنید و دستور `/farsi` را بفرستید.")

# ثبت دستورات
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("farsi", translate_reply))

@app.on_event("startup")
async def startup():
    await telegram_app.initialize()

@app.post("/webhook")
async def process_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "Bot is running!"}
