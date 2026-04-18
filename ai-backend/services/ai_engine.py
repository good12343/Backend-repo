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
Follow rules strictly:
- Be direct
- No repetition
"""

    persona_map = {
        "DEBUG": "You are a senior software engineer. Debug only.",
        "SOLVE": "You solve problems step-by-step.",
        "TEACH": "You are a teacher. Explain simply.",
    }

    persona = persona_map.get(intent, "You are a helpful assistant.")

    history = get_history()

    # ✅ حماية من الكراش
    safe_history = []
    for m in history[-6:]:
        role = m.get("role", "user")
        text = m.get("text", "")
        if text:
            safe_history.append(f"{role}: {text}")

    history_text = "\n".join(safe_history)

    prompt = f"""
{base_rules}

{persona}

History:
{history_text if history_text else "No history"}

User:
{message}

Answer:
"""

    return prompt.strip()


def call_llama(prompt: str, n_predict: int):

    try:
        response = requests.post(
            LLAMA_API_URL,
            json={
                "prompt": prompt,
                "n_predict": n_predict,
                "temperature": 0.2,
            },
            headers={
                "x-api-key": API_KEY
            },
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("LLAMA RESPONSE RAW:", response.text)

        # 🔥 حماية كاملة من الكراش
        try:
            return response.json()
        except:
            return {"reply": response.text}

    except Exception as e:
        return {"reply": f"LLAMA CALL ERROR: {str(e)}"}


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
    "reply": result,
    "raw_model": llama_response
}