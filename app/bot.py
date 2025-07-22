
# app/bot.py
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from app.gemini import generate_response
from app.context_cache import get_context, add_to_context

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Use os comandos:\n/start - Reiniciar conversa\n/help - Ver comandos")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Comandos disponíveis:\n/start - Reiniciar conversa\n/help - Ver comandos")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = str(update.message.chat_id)

    context_messages = get_context(chat_id)
    response = generate_response(context_messages, user_input)
    add_to_context(chat_id, user_input, response)
    await update.message.reply_text(response)

def run_bot():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
