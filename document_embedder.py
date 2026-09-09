import logging
from typing import Any

from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)


class DocumentEmbedder:
    """
    Generates semantic embeddings.

    Uses SentenceTransformers locally, meaning document
    embeddings do not require Gemini API calls.
    """

    def __init__(
        self,
        model_name: str = (
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        ),
    ):
        self.model_name = model_name

        logger.info(
            "Loading embedding model: %s",
            model_name,
        )

        self.model = SentenceTransformer(
            model_name
        )

    def embed_texts(
        self,
        texts: list[str],
        batch_size: int = 32,
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def embed_documents(
        self,
        documents: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        if not documents:
            return []

        texts = [
            document.get(
                "text",
                "",
            )
            for document in documents
        ]

        embeddings = self.embed_texts(
            texts
        )

        results = []

        for document, embedding in zip(
            documents,
            embeddings,
        ):
            result = document.copy()

            result["embedding"] = embedding

            results.append(result)

        return results

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        embedding = self.model.encode(
            query,
            normalize_embeddings=True,
        )

        return embedding.tolist()