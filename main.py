import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()

telegram_app = Application.builder().token(BOT_TOKEN).build()

# ---- Handlers ----
async def start(update: Update, context):
    await update.message.reply_text("Hello 👋 FastAPI + Docker + ngrok bot is running!")

async def echo(update: Update, context):
    await update.message.reply_text(f"You said: {update.message.text}")

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# ---- Webhook Endpoint ----
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}