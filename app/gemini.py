
# app/gemini.py
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-pro")

def generate_response(context_messages, user_input):
    messages = [f"Usuário: {u}\nBot: {b}" for u, b in context_messages]
    prompt = "\n".join(messages + [f"Usuário: {user_input}\nBot:"])
    try:
        response = model.generate_content(prompt, generation_config={
            "temperature": 0.7,
            "max_output_tokens": 500
        })
        return response.text
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"
