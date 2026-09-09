import logging
from pathlib import Path
from uuid import uuid4

from document_loader import DocumentLoader


logger = logging.getLogger(__name__)


class DocumentService:
    """
    Service responsible for document upload
    and document ingestion.
    """

    def __init__(
        self,
        document_loader:
        DocumentLoader | None = None,
        upload_directory: str =
        "data/uploads",
    ):

        self.document_loader = (
            document_loader
            or DocumentLoader()
        )

        self.upload_directory = Path(
            upload_directory
        )

        self.upload_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def save_and_process(
        self,
        file,
    ) -> dict:

        original_filename = (
            file.filename
            or "document.pdf"
        )

        extension = Path(
            original_filename
        ).suffix.lower()

        if extension != ".pdf":

            raise ValueError(
                "Only PDF files are currently supported."
            )

        unique_filename = (
            f"{uuid4()}_{original_filename}"
        )

        file_path = (
            self.upload_directory
            / unique_filename
        )

        try:

            content = await file.read()

            if not content:

                raise ValueError(
                    "Uploaded file is empty."
                )

            with open(
                file_path,
                "wb",
            ) as output_file:

                output_file.write(
                    content
                )

            logger.info(
                "Saved uploaded document: %s",
                original_filename,
            )

            result = (
                self.document_loader
                .load_document(
                    str(file_path)
                )
            )

            return result

        except Exception:

            if file_path.exists():

                file_path.unlink()

            raise

    def delete_document(
        self,
        document_id: str,
    ) -> dict:

        return (
            self.document_loader
            .delete_document(
                document_id
            )
        )