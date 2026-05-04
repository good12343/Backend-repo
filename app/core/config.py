import os
from dataclasses import dataclass


# =========================
# ENV LOADER
# =========================
def _get_env(key: str, default=None, required: bool = False):
    value = os.getenv(key, default)

    if required and (value is None or value == ""):
        raise EnvironmentError(f"Missing required environment variable: {key}")

    return value


def _get_bool(key: str, default="false"):
    return _get_env(key, default).lower() == "true"


def _get_int(key: str, default):
    return int(_get_env(key, str(default)))


# =========================
# CONFIG
# =========================
@dataclass(frozen=True)
class Config:

    # -------- LLM --------
    LLAMA_API_URL: str = _get_env(
        "LLAMA_API_URL",
        "http://54.227.171.175:3000/completion"   # 🔥 endpoint واضح
    )

    API_KEY: str = _get_env(
        "API_KEY",
        required=True   # 🔥 لا fallback (مهم للاستقرار)
    )

    # -------- APP --------
    APP_ENV: str = _get_env("APP_ENV", "development")
    DEBUG: bool = _get_bool("DEBUG", "false")

    # -------- MEMORY --------
    MAX_MEMORY_MESSAGES: int = _get_int("MAX_MEMORY_MESSAGES", 5)

    # -------- MODEL --------
    DEFAULT_N_PREDICT: int = _get_int("DEFAULT_N_PREDICT", 100)
    MAX_N_PREDICT: int = _get_int("MAX_N_PREDICT", 500)

    # -------- SAFETY FLAGS (حقيقية أو احذفها لاحقًا) --------
    ENABLE_PROMPT_GUARD: bool = True
    ENABLE_RESPONSE_SANITIZER: bool = True


# =========================
# SINGLETON
# =========================
config = Config()