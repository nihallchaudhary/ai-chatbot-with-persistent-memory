import time
from typing import Any

from evaluation.metrics import EvaluationResult


class RAGEvaluator:
    """
    Lightweight evaluation layer for measuring
    retrieval quality and response performance.
    """

    def evaluate(
        self,
        query: str,
        answer: str,
        retrieved_documents: list[dict[str, Any]],
        latency_seconds: float | None = None,
    ) -> EvaluationResult:

        scores = []

        for document in retrieved_documents:
            score = (
                document.get("rerank_score")
                or document.get("similarity_score")
                or document.get("score")
                or 0.0
            )

            scores.append(float(score))

        retrieval_score = (
            sum(scores) / len(scores)
            if scores
            else 0.0
        )

        return EvaluationResult(
            query=query,
            answer=answer,
            retrieval_score=round(retrieval_score, 4),
            context_count=len(retrieved_documents),
            latency_seconds=round(latency_seconds or 0.0, 4),
            answer_length=len(answer),
        )


class PipelineTimer:
    """Simple context manager for pipeline latency measurement."""

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.perf_counter()

    @property
    def elapsed(self) -> float:
        return time.perf_counter() - self.start_time