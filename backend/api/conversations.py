from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from backend.dependencies import (
    get_chat_service,
)
from backend.models.requests import (
    ConversationCreateRequest,
)
from backend.services.chat_service import (
    ChatService,
)


router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversations"],
)


@router.post("/")
async def create_conversation(
    request: ConversationCreateRequest,
    chat_service: ChatService = Depends(
        get_chat_service
    ),
):

    conversation_id = (
        chat_service
        .conversation_manager
        .create_conversation()
    )

    return (
        chat_service
        .get_conversation(
            conversation_id
        )
    )


@router.get(
    "/{conversation_id}"
)
async def get_conversation(
    conversation_id: str,
    chat_service: ChatService = Depends(
        get_chat_service
    ),
):

    conversation = (
        chat_service
        .get_conversation(
            conversation_id
        )
    )

    if not conversation:

        raise HTTPException(
            status_code=404,
            detail=(
                "Conversation not found."
            ),
        )

    return conversation


@router.delete(
    "/{conversation_id}"
)
async def delete_conversation(
    conversation_id: str,
    chat_service: ChatService = Depends(
        get_chat_service
    ),
):

    deleted = (
        chat_service
        .delete_conversation(
            conversation_id
        )
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail=(
                "Conversation not found."
            ),
        )

    return {
        "success": True,
        "conversation_id":
        conversation_id,
    }