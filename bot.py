
import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Prompt de contexto do agente
AGENT_CONTEXT = (
    "Você é um especialista em criptomoedas. Seu conhecimento cobre Bitcoin (BTC), "
    "Ethereum (ETH), Solana (SOL), stablecoins como Tether (USDT) e USDC, uso de cold wallets, "
    "análise de métricas como MVRV e também oportunidades como airdrops. "
    "Responda sempre com clareza, evite jargões desnecessários e traga exemplos reais sempre que possível."
)

logging.basicConfig(level=logging.INFO)

async def pergunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = " ".join(context.args)
    if not user_message:
        await update.message.reply_text("Use o comando assim: /pergunta Qual a diferença entre BTC e ETH?")
        return

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=300,
        messages=[
            {"role": "system", "content": AGENT_CONTEXT},
            {"role": "user", "content": user_message}
        ]
    )

    await update.message.reply_text(response["choices"][0]["message"]["content"])

async def analise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = " ".join(context.args)
    if not user_message:
        await update.message.reply_text("Use o comando assim: /analise Faça uma análise do token SOL hoje")
        return

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=300,
        messages=[
            {"role": "system", "content": AGENT_CONTEXT},
            {"role": "user", "content": f"Faça uma análise cripto sobre: {user_message}"}
        ]
    )

    await update.message.reply_text(response["choices"][0]["message"]["content"])

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("pergunta", pergunta))
    app.add_handler(CommandHandler("analise", analise))
    app.run_polling()

if __name__ == "__main__":
    main()
