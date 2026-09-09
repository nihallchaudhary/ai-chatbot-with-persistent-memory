from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class EvaluationResult:
    query: str
    answer: str
    retrieval_score: float
    context_count: int
    latency_seconds: float
    answer_length: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)