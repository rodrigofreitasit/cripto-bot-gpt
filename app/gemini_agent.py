import google.generativeai as genai
from app.config import GEMINI_API_KEY, MAX_TOKENS

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if len(text) > MAX_TOKENS:
            return text[:MAX_TOKENS] + "..."
        return text
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"
