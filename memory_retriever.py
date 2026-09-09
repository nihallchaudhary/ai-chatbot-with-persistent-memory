import re
from typing import Any


class MemoryRetriever:
    """
    Retrieves relevant long-term memories using
    lightweight keyword similarity.

    Your existing embedding-based retrieval can later
    replace or extend this layer without changing the
    MemoryManager interface.
    """

    def tokenize(
        self,
        text: str,
    ) -> set[str]:

        return set(
            re.findall(
                r"\b\w+\b",
                text.lower(),
            )
        )

    def calculate_relevance(
        self,
        query: str,
        memory_content: str,
    ) -> float:

        query_tokens = self.tokenize(query)
        memory_tokens = self.tokenize(
            memory_content
        )

        if not query_tokens or not memory_tokens:
            return 0.0

        intersection = (
            query_tokens
            & memory_tokens
        )

        union = (
            query_tokens
            | memory_tokens
        )

        return len(intersection) / len(union)

    def retrieve(
        self,
        query: str,
        memories: list[dict[str, Any]],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:

        results = []

        for memory in memories:
            content = memory.get(
                "content",
                "",
            )

            relevance = (
                self.calculate_relevance(
                    query,
                    content,
                )
            )

            importance = float(
                memory.get(
                    "importance",
                    0.5,
                )
            )

            final_score = (
                relevance * 0.7
                + importance * 0.3
            )

            result = memory.copy()

            result[
                "relevance_score"
            ] = round(
                relevance,
                4,
            )

            result[
                "final_score"
            ] = round(
                final_score,
                4,
            )

            results.append(result)

        results.sort(
            key=lambda item: (
                item["final_score"],
                item["importance"],
            ),
            reverse=True,
        )

        return results[:top_k]