
import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Carregar variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Prompt fixo do agente
AGENT_CONTEXT = (
    "Você é um especialista em criptomoedas. Seu conhecimento cobre Bitcoin (BTC), Ethereum (ETH), Solana (SOL), "
    "stablecoins como Tether (USDT) e USDC, uso de cold wallets, análise de métricas como MVRV e oportunidades como airdrops. "
    "Responda sempre com clareza, evite jargões desnecessários e traga exemplos reais sempre que possível."
)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Eu sou o seu bot cripto.
"
        "Use o comando /help para ver como interagir comigo."
    )

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Comandos disponíveis:
"
        "/start - Mensagem de boas-vindas
"
        "/help - Lista de comandos

"
        "Ou envie uma mensagem com sua dúvida sobre criptomoedas, como por exemplo:
"
        "- O que é MVRV?
"
        "- Qual a diferença entre USDT e USDC?
"
        "- Como proteger meus ativos em cold wallet?"
    )

# Mensagem de análise
async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": AGENT_CONTEXT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=300,
        temperature=0.7
    )
    await update.message.reply_text(response.choices[0].message.content)

# Inicialização
def main():
    app = Application.builder().token(TELEGRAM_API_KEY).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyse))
    app.run_polling()

if __name__ == '__main__':
    main()
