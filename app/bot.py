import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from app.gemini_agent import ask_gemini

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Olá! Sou um bot de cripto com Gemini AI. Use os comandos:\n/start\n/help")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Envie uma pergunta sobre criptomoedas (BTC, ETH, SOL, stablecoins, cold wallets, MVRV, airdrops, etc).")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text.startswith("/"):
        await update.message.reply_text("Comando não reconhecido.")
        return

    await update.message.reply_text("🔎 Processando sua pergunta...")
    answer = ask_gemini(text)
    await update.message.reply_text(answer)

def main() -> None:
    import os
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_TOKEN:
        raise ValueError("Token do bot Telegram não encontrado!")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot está rodando...")
    app.run_polling()
