from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

LLAMA_API_URL = "http://54.227.171.175:3000/chat"
API_KEY = "712825736aA$"


# ====== REQUEST MODEL ======
class ChatRequest(BaseModel):
    message: str | None = None
    prompt: str | None = None
    n_predict: int | None = 100


def extract_message(req: ChatRequest):
    return req.message or req.prompt or ""


# ====== INTENT ======
def detect_intent(text: str):
    text = text.lower()

    if "error" in text or "bug" in text or "خطأ" in text:
        return "DEBUG"

    if "solve" in text or "حل" in text:
        return "SOLVE"

    if "explain" in text or "اشرح" in text:
        return "TEACH"

    return "GENERAL"


# ====== PROMPT (🔥 محسّن جدًا) ======
def build_prompt(message: str, intent: str):

    instruction = {
        "TEACH": "Explain step-by-step with a simple example.",
        "SOLVE": "Give the final solution first, then a short explanation.",
        "DEBUG": "Identify the bug and provide the fix only.",
        "GENERAL": "Answer clearly and briefly."
    }

    return f"""<|system|>
You are a professional programming tutor.
- Do NOT repeat the question
- Do NOT generate multiple Q&A
- Give ONE clear answer only

<|user|>
{message}

<|assistant|>
""".strip()


# ====== CALL NODE ======
def call_llama(prompt: str, n_predict: int):

    headers = {
        "x-api-key": API_KEY
    }

    response = requests.post(
        LLAMA_API_URL,
        json={
            "prompt": prompt,
            "n_predict": n_predict,
            "temperature": 0.3,
            "stop": ["<|user|>", "Question:", "Answer:"]
        },
        headers=headers
    )

    return response.json()


# ====== CLEAN RESPONSE (🔥 مهم جدًا) ======
def clean_output(text: str):
    if not text:
        return ""

    # إزالة أي تكرار مزعج
    for token in ["Question:", "Answer:", "<|assistant|>"]:
        text = text.replace(token, "")

    return text.strip()


# ====== API ======
@app.post("/chat")
def chat(req: ChatRequest):

    message = extract_message(req)

    intent = detect_intent(message)
    prompt = build_prompt(message, intent)

    llama_response = call_llama(prompt, req.n_predict or 100)

    raw = (
        llama_response.get("reply")
        or llama_response.get("content")
        or llama_response.get("response")
        or str(llama_response)
    )

    result = clean_output(raw)

    return {
        "intent": intent,
        "reply": result
    }