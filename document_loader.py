import logging
from pathlib import Path
from typing import Any

from document_embedder import DocumentEmbedder
from document_store import DocumentStore
from pdf_processor import PDFProcessor


logger = logging.getLogger(__name__)


class DocumentLoader:
    """
    Complete document ingestion pipeline.

    Flow:
        PDF
         ↓
    Text Extraction
         ↓
    Chunking
         ↓
    Embedding
         ↓
    Vector Storage
    """

    def __init__(
        self,
        pdf_processor: PDFProcessor | None = None,
        embedder: DocumentEmbedder | None = None,
        document_store: DocumentStore | None = None,
    ):
        self.pdf_processor = (
            pdf_processor
            or PDFProcessor()
        )

        self.embedder = (
            embedder
            or DocumentEmbedder()
        )

        self.document_store = (
            document_store
            or DocumentStore()
        )

    def load_pdf(
        self,
        file_path: str,
    ) -> dict[str, Any]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                "Currently only PDF files are supported."
            )

        logger.info(
            "Starting ingestion: %s",
            path.name,
        )

        # 1. Extract and chunk PDF
        documents = self.pdf_processor.process(
            str(path)
        )

        if not documents:
            raise ValueError(
                "No readable text was extracted from the PDF."
            )

        # 2. Generate embeddings
        embedded_documents = (
            self.embedder.embed_documents(
                documents
            )
        )

        # 3. Store vectors
        stored_count = (
            self.document_store.add_documents(
                embedded_documents
            )
        )

        document_id = (
            documents[0]
            .get("metadata", {})
            .get("document_id")
        )

        logger.info(
            "Completed ingestion: %s chunks stored.",
            stored_count,
        )

        return {
            "success": True,
            "filename": path.name,
            "document_id": document_id,
            "chunks_created": len(documents),
            "chunks_stored": stored_count,
        }

    def load_document(
        self,
        file_path: str,
    ) -> dict[str, Any]:

        return self.load_pdf(file_path)

    def delete_document(
        self,
        document_id: str,
    ) -> dict[str, Any]:

        deleted_count = (
            self.document_store.delete_document(
                document_id
            )
        )

        return {
            "document_id": document_id,
            "deleted_chunks": deleted_count,
        }