from fastapi import (
    APIRouter,
    Depends,
)

from backend.dependencies import (
    get_document_store,
)
from document_store import DocumentStore
from health import HealthService


router = APIRouter(
    prefix="/api",
    tags=["Health"],
)


@router.get(
    "/health"
)
async def health_check(
    document_store: DocumentStore = Depends(
        get_document_store
    ),
):

    health_service = HealthService(
        document_store=document_store
    )

    return health_service.get_health()