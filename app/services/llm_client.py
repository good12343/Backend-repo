import requests
import time
from app.core.config import config


def call_llm(prompt: str, n_predict: int = 100, retries: int = 2, api_url=None, api_key=None):
    url = api_url or config.LLAMA_API_URL
    key = api_key or config.API_KEY

    payload = {
        "prompt": prompt,
        "n_predict": n_predict,
        "temperature": 0.2,
        "stop": [
            "User:",
            "Assistant:",
            "\nUser",
            "\nAssistant",
            "//",
            "#",
            "```",
            "(Write your code here)"
        ]
    }

    headers = {
        "x-api-key": key,
        "Content-Type": "application/json"
    }

    last_error = None

    for attempt in range(retries + 1):
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            # ✅ إصلاح الـ Encoding
            raw_text = response.text
            
            # جرب إصلاح الـ encoding
            try:
                # إذا كان الرد bytes
                if hasattr(response, 'content'):
                    raw_text = response.content.decode('utf-8')
            except:
                pass
            
            # جرب latin-1 → utf-8 fix
            try:
                fixed = raw_text.encode('latin-1').decode('utf-8')
                if 'Ù' not in fixed and 'Ø' not in fixed:
                    raw_text = fixed
            except:
                pass

            # ✅ دائماً نرجع dict موحد
            try:
                data = response.json()
                if isinstance(data, dict):
                    if "content" in data and "reply" not in data:
                        data["reply"] = data.pop("content")
                    # إصلاح encoding داخل الـ dict
                    if "reply" in data and isinstance(data["reply"], str):
                        try:
                            fixed_reply = data["reply"].encode('latin-1').decode('utf-8')
                            if 'Ù' not in fixed_reply:
                                data["reply"] = fixed_reply
                        except:
                            pass
                    return data
                return {"reply": str(data)}
            except Exception:
                return {"reply": raw_text.strip()}

        except Exception as e:
            last_error = str(e)
            time.sleep(0.5 * (attempt + 1))

    return {"reply": f"LLM timeout | error: {last_error}"}
