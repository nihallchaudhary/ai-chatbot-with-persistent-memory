import logging
from typing import Any

import chromadb


logger = logging.getLogger(__name__)


class DocumentStore:
    """
    Persistent ChromaDB vector store.
    """

    def __init__(
        self,
        collection_name: str = "ai_knowledge_base",
        persist_directory: str = "./data/chroma_db",
    ):
        self.collection_name = collection_name

        self.client = (
            chromadb.PersistentClient(
                path=persist_directory
            )
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name,
                metadata={
                    "description": (
                        "AI Knowledge Assistant "
                        "vector database"
                    )
                },
            )
        )

    def add_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> int:

        if not documents:
            return 0

        ids = []
        texts = []
        embeddings = []
        metadatas = []

        for document in documents:

            document_id = document.get("id")

            text = document.get("text")

            embedding = document.get(
                "embedding"
            )

            metadata = document.get(
                "metadata",
                {},
            )

            if (
                not document_id
                or not text
                or embedding is None
            ):
                continue

            ids.append(str(document_id))
            texts.append(text)
            embeddings.append(embedding)
            metadatas.append(
                self._sanitize_metadata(
                    metadata
                )
            )

        if not ids:
            return 0

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        logger.info(
            "Stored %s document chunks.",
            len(ids),
        )

        return len(ids)

    def _sanitize_metadata(
        self,
        metadata: dict[str, Any],
    ) -> dict[str, Any]:

        cleaned = {}

        for key, value in metadata.items():

            if value is None:
                continue

            if isinstance(
                value,
                (
                    str,
                    int,
                    float,
                    bool,
                ),
            ):
                cleaned[key] = value

            else:
                cleaned[key] = str(value)

        return cleaned

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 10,
        where: dict | None = None,
    ) -> list[dict[str, Any]]:

        if self.collection.count() == 0:
            return []

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=min(
                top_k,
                self.collection.count(),
            ),
            where=where,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = (
            results.get(
                "documents",
                [[]],
            )[0]
        )

        metadatas = (
            results.get(
                "metadatas",
                [[]],
            )[0]
        )

        distances = (
            results.get(
                "distances",
                [[]],
            )[0]
        )

        ids = (
            results.get(
                "ids",
                [[]],
            )[0]
        )

        formatted_results = []

        for (
            document_id,
            text,
            metadata,
            distance,
        ) in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):

            similarity_score = (
                1.0
                - float(distance)
            )

            formatted_results.append(
                {
                    "id": document_id,
                    "text": text,
                    "metadata": metadata,
                    "distance": (
                        float(distance)
                    ),
                    "similarity_score": (
                        round(
                            similarity_score,
                            6,
                        )
                    ),
                }
            )

        return formatted_results

    def delete_document(
        self,
        document_id: str,
    ) -> int:

        results = self.collection.get(
            where={
                "document_id": document_id
            }
        )

        ids = results.get(
            "ids",
            [],
        )

        if ids:
            self.collection.delete(
                ids=ids
            )

        return len(ids)

    def count(self) -> int:
        return self.collection.count()

    def clear(self):
        self.client.delete_collection(
            self.collection_name
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=self.collection_name
            )
        )