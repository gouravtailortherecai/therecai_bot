import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from database import engine, AsyncSessionLocal
from models import Base, Chat
from sqlalchemy import insert

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()

telegram_app = Application.builder().token(BOT_TOKEN).build()
is_initialized = False


# ---- Handlers ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working 🚀")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username
    text = update.message.text

    # Store in DB
    async with AsyncSessionLocal() as session:
        stmt = insert(Chat).values(
            user_id=user_id,
            username=username,
            message=text,
        )
        await session.execute(stmt)
        await session.commit()

    # Resume detection (simple logic)
    if "experience" in text.lower() or "education" in text.lower():
        await update.message.reply_document(document=open("resume.pdf", "rb"))
    else:
        await update.message.reply_text("Message saved ✅")


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
# ---- Webhook Endpoint ----
@app.post("/webhook")
async def webhook(request: Request):
    global is_initialized

    if not is_initialized:
        await telegram_app.initialize()
        await telegram_app.start()
        is_initialized = True

    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)

    return {"ok": True}

