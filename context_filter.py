from typing import Any


class ContextFilter:
    """
    Removes duplicate and excessively large context chunks
    before LLM generation.

    Relevance filtering is intentionally handled by the
    retrieval and reranking stages rather than assuming
    CrossEncoder scores are bounded between 0 and 1.
    """

    def __init__(
        self,
        max_chunks: int = 5,
        max_characters: int = 15000,
    ):
        self.max_chunks = max_chunks

        self.max_characters = (
            max_characters
        )

    def filter(
        self,
        documents: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        if not documents:
            return []

        results = []

        seen_texts = set()

        total_characters = 0

        for document in documents:

            text = (
                document.get(
                    "text",
                    "",
                )
                .strip()
            )

            if not text:
                continue

            normalized_text = (
                text.lower()
                .replace(" ", "")
            )

            if normalized_text in seen_texts:
                continue

            if (
                total_characters
                + len(text)
                > self.max_characters
            ):
                remaining = (
                    self.max_characters
                    - total_characters
                )

                if remaining <= 0:
                    break

                document = document.copy()

                document["text"] = (
                    text[:remaining]
                )

                text = document["text"]

            results.append(document)

            seen_texts.add(
                normalized_text
            )

            total_characters += len(text)

            if (
                len(results)
                >= self.max_chunks
            ):
                break

        return results

    def filter_context(
        self,
        documents: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        return self.filter(documents)