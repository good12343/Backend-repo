from fastapi import APIRouter, HTTPException, Request
from app.api.schemas.chat_schema import ChatRequest
from app.services.chat_service import handle_chat
import time

router = APIRouter()


# =========================
# LOGGING
# =========================
def _log_request(req: ChatRequest):
    print(f"[CHAT REQUEST] message={req.message}")


# =========================
# POST /chat
# =========================
@router.post("/chat")
async def chat(req: ChatRequest, request: Request):

    start_time = time.time()

    # =========================
    # VALIDATION (CLEANER)
    # =========================
    if not req.message or not req.message.strip():
        raise HTTPException(
            status_code=400,
            detail="message is required"
        )

    try:
        # =========================
        # LOG
        # =========================
        _log_request(req)

        # =========================
        # BUSINESS LOGIC
        # =========================
        response = handle_chat(req)

        # =========================
        # LATENCY
        # =========================
        duration = round(time.time() - start_time, 4)

        return {
            "success": True,
            "response": response,
            "latency": duration
        }

    except HTTPException as he:
        raise he

    except Exception as e:
        print(f"[CHAT ERROR] {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )