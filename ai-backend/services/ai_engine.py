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

    base_rules = """
You are NOT a general chatbot.

Follow these rules strictly:
- Do NOT repeat the user message
- Do NOT add unnecessary conversation
- Be direct and structured
"""

    if intent == "DEBUG":
        persona = """
You are a senior software engineer.
Your job is ONLY debugging.

Rules:
- Identify the error
- Explain why it happens
- Provide a fix only
"""
    elif intent == "SOLVE":
        persona = """
You are a problem solver.
Give full step-by-step solution.
"""
    elif intent == "TEACH":
        persona = """
You are a teacher.
Explain simply with examples and steps.
"""
    else:
        persona = """
You are a helpful programming assistant.
Give clear and concise answers.
"""

    history = get_history()

    history_text = "\n".join([
        f"{m['role']}: {m['text']}" for m in history[-6:]
    ])

    return f"""
{base_rules}

{persona}

Conversation History:
{history_text}

User:
{message}

Final Answer:
"""


def call_llama(prompt: str, n_predict: int):

    try:
        response = requests.post(
            LLAMA_API_URL,
            json={
                "prompt": prompt,
                "n_predict": n_predict,
                "temperature": 0.3
            },
            headers={
                "x-api-key": API_KEY
            },
            timeout=30
        )

        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {"error": str(e)}


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