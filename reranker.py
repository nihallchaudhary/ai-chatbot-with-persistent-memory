import logging
from typing import Any

from sentence_transformers import CrossEncoder


logger = logging.getLogger(__name__)


class Reranker:
    """
    Cross-encoder reranking layer.

    The vector database retrieves semantically similar
    chunks. The cross-encoder performs a second,
    more precise relevance ranking.
    """

    def __init__(
        self,
        model_name: str = (
            "cross-encoder/"
            "ms-marco-MiniLM-L-6-v2"
        ),
    ):
        self.model_name = model_name

        logger.info(
            "Loading reranker model: %s",
            model_name,
        )

        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query: str,
        documents: list[dict[str, Any]],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:

        if not documents:
            return []

        pairs = [
            (
                query,
                document.get(
                    "text",
                    "",
                ),
            )
            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        results = []

        for document, score in zip(
            documents,
            scores,
        ):
            result = document.copy()

            result[
                "rerank_score"
            ] = float(score)

            results.append(result)

        results.sort(
            key=lambda document: (
                document[
                    "rerank_score"
                ]
            ),
            reverse=True,
        )

        return results[:top_k]