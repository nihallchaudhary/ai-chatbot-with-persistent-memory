from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from backend.dependencies import (
    get_chat_service,
)
from backend.models.requests import ChatRequest
from backend.models.responses import (
    ChatResponse,
    ErrorResponse,
)
from backend.services.chat_service import (
    ChatService,
)


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
    responses={
        400: {
            "model": ErrorResponse
        },
        500: {
            "model": ErrorResponse
        },
    },
)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(
        get_chat_service
    ),
):

    try:

        return chat_service.chat(
            query=request.query,
            user_id=request.user_id,
            conversation_id=request.conversation_id,
            metadata=request.metadata,
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error