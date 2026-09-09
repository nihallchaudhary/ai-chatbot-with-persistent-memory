from typing import Any


class RAGEvaluator:
    """
    Basic evaluation framework for the RAG pipeline.

    Measures:
    - Retrieval quality
    - Answer grounding
    - Source availability
    """

    def evaluate_retrieval(
        self,
        retrieved_documents: list[dict],
        expected_keywords: list[str],
    ) -> dict[str, Any]:

        if not expected_keywords:
            return {
                "keyword_recall": None,
                "matched_keywords": [],
            }

        combined_text = " ".join(
            document.get(
                "text",
                "",
            ).lower()
            for document
            in retrieved_documents
        )

        matched = [
            keyword
            for keyword
            in expected_keywords
            if keyword.lower()
            in combined_text
        ]

        recall = (
            len(matched)
            / len(expected_keywords)
        )

        return {
            "keyword_recall": round(
                recall,
                4,
            ),
            "matched_keywords": matched,
            "total_expected_keywords": (
                len(expected_keywords)
            ),
        }

    def evaluate_grounding(
        self,
        answer: str,
        sources: list[dict],
    ) -> dict[str, Any]:

        has_answer = bool(
            answer
            and answer.strip()
        )

        has_sources = bool(sources)

        grounded = (
            has_answer
            and has_sources
        )

        return {
            "has_answer": has_answer,
            "has_sources": has_sources,
            "grounded": grounded,
        }

    def evaluate_response(
        self,
        result: dict[str, Any],
        expected_keywords: (
            list[str] | None
        ) = None,
    ) -> dict[str, Any]:

        retrieval = (
            self.evaluate_retrieval(
                result.get(
                    "documents",
                    [],
                ),
                expected_keywords or [],
            )
        )

        grounding = (
            self.evaluate_grounding(
                result.get(
                    "answer",
                    "",
                ),
                result.get(
                    "sources",
                    [],
                ),
            )
        )

        return {
            "retrieval": retrieval,
            "grounding": grounding,
        }