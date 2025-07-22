import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MAX_TOKENS = 400

COMMANDS = {
    "/start": "Exibe mensagem inicial",
    "/help": "Exibe comandos disponíveis",
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou um bot de cripto com Gemini. Use /help para ver comandos.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_list = "\n".join([f"{cmd}: {desc}" for cmd, desc in COMMANDS.items()])
    await update.message.reply_text(f"Comandos disponíveis:\n{commands_list}")

def call_gemini_api(prompt):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = { "Content-Type": "application/json" }
    contexto_do_agente = """
    Você é um agente especialista em criptomoedas. Seu foco está em ativos como Bitcoin (BTC), Ethereum (ETH), Solana (SOL), stablecoins como USDT (Tether) e USDC. 
    Você entende de segurança com cold wallets e hot wallets, e tem profundo conhecimento sobre análises on-chain, incluindo indicadores como MVRV, NUPL, SOPR e dominância do BTC. 
    Você também está sempre atualizado sobre airdrops relevantes, utilidades das blockchains, L2s como Arbitrum e Optimism, além de DEXs, yield farming, staking e regulamentações globais. 
    Ao responder, seja didático e objetivo, sempre com foco educativo e informativo. Utilize exemplos reais e dados recentes quando possível.
    """

    data = {
        "contents": [
            {"role": "user", "parts": [{"text": contexto_do_agente}]},
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        logging.error(f"Erro Gemini: {response.status_code} - {response.text}")
        return "Erro ao gerar resposta com Gemini."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.startswith("/"):
        await update.message.reply_text("Use um comando. Veja /help")
        return

    if text == "/start":
        await start(update, context)
    elif text == "/help":
        await help_command(update, context)
    elif text.startswith("/ask"):
        prompt = text.replace("/ask", "").strip()
        if not prompt:
            await update.message.reply_text("Use /ask seguido da sua pergunta.")
            return
        await update.message.reply_text("Pensando...")
        reply = call_gemini_api(prompt)
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text("Comando não reconhecido. Use /help.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ask", handle_message))
    app.run_polling()
