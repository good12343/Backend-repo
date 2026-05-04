from app.core.response_parser import parse_tool_response
import time


def safe_call_llm(call_fn, max_retries=2):
    """
    يستدعي LLM ويرجع الـ RAW (dict/str) مو الـ parsed
    """
    last_error = None

    for attempt in range(max_retries):
        try:
            raw = call_fn()
            return raw  # ✅ يرجع RAW كما هو

        except Exception as e:
            last_error = e
            time.sleep(0.2 * (attempt + 1))

    return {"reply": f"Service temporarily unavailable | error: {last_error}"}
