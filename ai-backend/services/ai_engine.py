# services/ai_engine.py

import requests
from services.memory import add_message, get_history

LLAMA_API_URL = "http://54.227.171.175:3000/chat"
API_KEY = "712825736aA$"


def detect_intent(text: str):
    text = text.lower()

    if "error" in text or "bug" in text or "خطأ" in text:
        return "DEBUG"

    if "solve" in text or "حل" in text:
        return "SOLVE"

    if "explain" in text or "اشرح" in text:
        return "TEACH"

    return "GENERAL"


def build_prompt(message: str, intent: str):

    return f"""You are an expert programming tutor.

RULES:
- Do NOT repeat the user message
- Do NOT write "User:" or "Assistant:"
- Do NOT ask questions back unless necessary
- Give direct answer only

TASK:
{message}

ANSWER:
"""


def call_llama(prompt: str, n_predict: int):

    response = requests.post(
        LLAMA_API_URL,
        json={
            "prompt": prompt,
            "n_predict": n_predict,
            "temperature": 0.2,
            
        },
        headers={
            "x-api-key": API_KEY
        }
    )

    return response.json()


def clean_output(text: str):
    if not text:
        return ""

    for token in ["Question:", "Answer:", "<|assistant|>"]:
        text = text.replace(token, "")

    return text.strip()


# 🔥 الدالة الرئيسية (العقل)
def generate_response(message: str, n_predict: int = 100):

    add_message("user", message)

    intent = detect_intent(message)
    prompt = build_prompt(message, intent)

    llama_response = call_llama(prompt, n_predict)

    raw = (
        llama_response.get("reply")
        or llama_response.get("content")
        or llama_response.get("response")
        or str(llama_response)
    )

    result = clean_output(raw)

    add_message("assistant", result)

    return {
        "intent": intent,
        "reply": result
    }