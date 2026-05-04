from typing import List, Dict


# =========================
# 1. MEMORY NORMALIZER (SAFE)
# =========================
def _normalize_history(history: List[Dict], limit: int = 3) -> str:
    output = []

    for msg in history[-limit:]:
        role = msg.get("role")
        content = (msg.get("content") or "").strip()

        if not content:
            continue

        if role == "user":
            output.append(f"User: {content}")
        elif role == "assistant":
            output.append(f"Assistant: {content}")

    return "\n".join(output)


# =========================
# 2. STRICT SYSTEM RULES (FIXED!)
# =========================
SYSTEM_RULES = """You are a helpful AI assistant. You help with all topics.

SMART CONTRACTS:
- Solana → Rust + Anchor
- Ethereum → Solidity
- Others → Ask user

LANGUAGE RULE (CRITICAL):
- If user writes in Arabic → YOU MUST reply in Arabic only
- If user writes in English → YOU MUST reply in English only
- If user writes in mixed → reply in the dominant language
- NEVER mix languages in the same reply

FORMAT:
{"tool":"chat_reply","args":{"reply":"WRITE YOUR REAL ANSWER HERE"}}

CRITICAL RULES:
- Replace WRITE YOUR REAL ANSWER HERE with your actual response
- Do NOT write "string" or placeholders
- No text before/after JSON
- No markdown code blocks
- No comments
- Natural and conversational"""



# =========================
# 3. MAIN PROMPT BUILDER (FIXED)
# =========================
def build_prompt(message: str, history: List[Dict]) -> str:
    history_block = _normalize_history(history)

    if history_block:
        prompt = f"""{SYSTEM_RULES}

Previous conversation:
{history_block}

User: {message}

Your response (JSON only):"""
    else:
        prompt = f"""{SYSTEM_RULES}

User: {message}

Your response (JSON only):"""

    return prompt
