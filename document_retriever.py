import logging
from typing import Any

from document_embedder import DocumentEmbedder
from document_store import DocumentStore


logger = logging.getLogger(__name__)


class DocumentRetriever:
    """
    Semantic vector retrieval layer.
    """

    def __init__(
        self,
        embedder: (
            DocumentEmbedder | None
        ) = None,
        store: (
            DocumentStore | None
        ) = None,
    ):
        self.embedder = (
            embedder
            or DocumentEmbedder()
        )

        self.store = (
            store
            or DocumentStore()
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        document_id: str | None = None,
    ) -> list[dict[str, Any]]:

        if not query.strip():
            return []

        query_embedding = (
            self.embedder.embed_query(
                query
            )
        )

        where = None

        if document_id:
            where = {
                "document_id": document_id
            }

        results = self.store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            where=where,
        )

        logger.info(
            "Retrieved %s documents.",
            len(results),
        )

        return results

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[dict[str, Any]]:

        return self.retrieve(
            query,
            top_k,
        )