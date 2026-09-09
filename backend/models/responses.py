from typing import Any

from pydantic import BaseModel


class SourceResponse(BaseModel):
    filename: str | None = None
    page: int | None = None
    document_id: str | None = None
    chunk_id: str | None = None
    score: float | None = None


class ChatResponse(BaseModel):
    request_id: str
    conversation_id: str

    answer: str

    sources: list[
        SourceResponse
    ] = []

    model: str | None = None

    grounded: bool = False

    cached: bool = False

    metrics: dict[str, Any] = {}


class DocumentUploadResponse(BaseModel):
    success: bool

    filename: str

    document_id: str | None = None

    chunks_created: int = 0

    chunks_stored: int = 0


class ConversationResponse(BaseModel):
    conversation_id: str

    created_at: str | None = None

    updated_at: str | None = None

    message_count: int = 0


class ErrorResponse(BaseModel):
    detail: str