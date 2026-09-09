from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )

    conversation_id: str | None = None

    user_id: str = "default_user"

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class DocumentDeleteRequest(BaseModel):
    document_id: str


class ConversationCreateRequest(BaseModel):
    user_id: str = "default_user"


class ConversationMessageRequest(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )

    role: str = "user"