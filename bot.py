import os
from dotenv import load_dotenv
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Load .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Agente cripto (prompt fixo)
AGENTE_PROMPT = """
Você é um especialista em criptomoedas com conhecimento avançado sobre:
- Bitcoin, Ethereum, Solana
- Stablecoins (USDT, USDC, DAI)
- Cold wallets e segurança de custódia
- Airdrops e estratégias para aproveitá-los
- Análise on-chain (MVRV, NUPL, SOPR)
- Tokenomics, DeFi, NFTs e regulação
Responda de forma clara, com profundidade técnica e tom educado.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Sou seu bot cripto. Me pergunte sobre BTC, ETH, MVRV, airdrops, cold wallets e mais!\n"
        "Exemplos:\n"
        "- O que é MVRV?\n"
        "- Como aproveitar airdrops retroativos?\n"
        "- Qual a diferença entre USDT e USDC?"
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = update.message.text
    try:
        resposta = await gerar_resposta(pergunta)
        await update.message.reply_text(resposta)
    except Exception as e:
        print(f"Erro: {e}")
        await update.message.reply_text("⚠️ Ocorreu um erro ao consultar o ChatGPT.")

async def gerar_resposta(pergunta):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": AGENTE_PROMPT},
            {"role": "user", "content": pergunta}
        ],
        max_tokens=600,
        temperature=0.7
    )
    return resposta.choices[0].message.content.strip()

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("🚀 Bot cripto ativo.")
    app.run_polling()
