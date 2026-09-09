from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from backend.dependencies import (
    get_document_service,
)
from backend.models.requests import (
    DocumentDeleteRequest,
)
from backend.models.responses import (
    DocumentUploadResponse,
)
from backend.services.document_service import (
    DocumentService,
)


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=
    DocumentUploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    document_service: DocumentService =
    Depends(get_document_service),
):

    try:

        return (
            await document_service
            .save_and_process(file)
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to process "
                "the uploaded document."
            ),
        ) from error


@router.delete("/")
async def delete_document(
    request: DocumentDeleteRequest,
    document_service: DocumentService =
    Depends(get_document_service),
):

    try:

        return (
            document_service
            .delete_document(
                request.document_id
            )
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to delete "
                "the document."
            ),
        ) from error