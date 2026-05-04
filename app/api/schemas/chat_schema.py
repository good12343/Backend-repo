from pydantic import BaseModel, Field
from typing import Optional


# =========================
# REQUEST SCHEMA
# =========================
class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="User input message"
    )

    user_id: str = Field(
        default="default",
        max_length=100
    )

    n_predict: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Max tokens to generate"
    )


# =========================
# RESPONSE SCHEMA
# =========================
class ChatResponse(BaseModel):
    reply: str = Field(
        ...,
        description="Model generated response"
    )

    intent: str = Field(
        default="GENERAL"
    )

    latency: float = Field(
        default=0.0,
        description="Response time in seconds"
    )

    model: str = Field(
        default="llama"
    )