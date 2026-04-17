from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

LLAMA_API_URL = "http://54.227.171.175:3000/chat"


# ====== يقبل أي شكل من Flutter بدون كسر ======
class ChatRequest(BaseModel):
    message: str | None = None
    prompt: str | None = None
    n_predict: int | None = 100


# ====== اختيار النص الصحيح بدون كسر التطبيق ======
def extract_message(req: ChatRequest):
    return req.message or req.prompt or ""


# ====== INTENT (خفيف بدون تعقيد) ======
def detect_intent(text: str):
    text = text.lower()

    if "error" in text or "bug" in text or "خطأ" in text:
        return "DEBUG"

    if "solve" in text or "حل" in text:
        return "SOLVE"

    if "explain" in text or "اشرح" in text:
        return "TEACH"

    return "GENERAL"


# ====== PROMPT ======
def build_prompt(message: str, intent: str):

    instruction = {
        "TEACH": "Explain clearly step by step with simple examples.",
        "SOLVE": "Give the solution first then short explanation.",
        "DEBUG": "Find the issue and explain the fix clearly.",
        "GENERAL": "Answer clearly and simply."
    }

    return f"""
You are a helpful programming tutor.

Instruction:
{instruction[intent]}

Question:
{message}

Answer only. Do not repeat the question.
""".strip()


# ====== CALL LLAMA ======
def call_llama(prompt: str, n_predict: int):

    response = requests.post(
        LLAMA_API_URL,
        json={
            "prompt": prompt,
            "n_predict": n_predict,
            "temperature": 0.5
        }
    )

    return response.json()


# ====== API ======
@app.post("/chat")
def chat(req: ChatRequest):

    message = extract_message(req)

    intent = detect_intent(message)
    prompt = build_prompt(message, intent)

    llama_response = call_llama(prompt, req.n_predict or 100)

    # يدعم كل أشكال الرد بدون كسر التطبيق
    result = (
        llama_response.get("reply")
        or llama_response.get("content")
        or llama_response.get("response")
        or str(llama_response)
    )

    return {
        "intent": intent,
        "reply": result   # 🔴 مهم: متوافق مع Flutter عندك
    }