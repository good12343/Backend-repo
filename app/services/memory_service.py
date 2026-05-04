from collections import defaultdict
import time
import threading


# =========================
# THREAD SAFE MEMORY STORE
# =========================
memory_store = defaultdict(list)
lock = threading.Lock()


# =========================
# CONFIG
# =========================
MAX_HISTORY = 10


# =========================
# ADD MESSAGE (SAFE)
# =========================
def add_message(user_id: str, role: str, content: str):
    if not user_id:
        user_id = "default"

    if not content:
        return

    message = {
        "role": role,
        "content": content,
        "timestamp": time.time()
    }

    with lock:
        memory_store[user_id].append(message)

        # keep only last N messages (efficient slicing)
        if len(memory_store[user_id]) > MAX_HISTORY:
            memory_store[user_id] = memory_store[user_id][-MAX_HISTORY:]


# =========================
# GET HISTORY (SAFE COPY)
# =========================
def get_history(user_id: str):
    if not user_id:
        user_id = "default"

    with lock:
        return list(memory_store.get(user_id, []))


# =========================
# CLEAR MEMORY
# =========================
def clear_memory(user_id: str):
    if not user_id:
        user_id = "default"

    with lock:
        memory_store[user_id] = []


# =========================
# OPTIONAL: MEMORY STATS (PRO LEVEL FEATURE)
# =========================
def get_memory_stats():
    with lock:
        return {
            "active_users": len(memory_store),
            "total_messages": sum(len(v) for v in memory_store.values())
        }