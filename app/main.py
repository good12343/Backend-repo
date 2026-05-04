from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.core.config import config


# =========================
# APP FACTORY
# =========================
def create_app() -> FastAPI:

    app = FastAPI(
        title="AI Chat Backend",
        version="1.0.0",
        docs_url="/docs" if config.DEBUG else None,
        redoc_url="/redoc" if config.DEBUG else None,
    )

    # =========================
    # CORS (SECURE VERSION READY)
    # =========================
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if config.DEBUG else [],  # 🔥 production آمن
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
    )

    # =========================
    # ROUTES
    # =========================
    app.include_router(chat_router, prefix="/api")

    # =========================
    # HEALTH CHECK
    # =========================
    @app.get("/health")
    def health_check():
        return {
            "status": "ok",
            "env": config.APP_ENV
        }

    return app


# =========================
# APP INSTANCE
# =========================
app = create_app()