import time
from collections import defaultdict
from typing import Any


class PipelineStats:
    """
    Tracks performance metrics across the AI pipeline.

    Useful for:
    - API monitoring
    - Debugging
    - Performance evaluation
    - Placement project demonstrations
    """

    def __init__(self):
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)

    def record_latency(
        self,
        operation: str,
        latency: float,
    ):
        self.metrics[
            operation
        ].append(latency)

    def increment(
        self,
        name: str,
        value: int = 1,
    ):
        self.counters[name] += value

    def record(
        self,
        operation: str,
        function,
        *args,
        **kwargs,
    ) -> Any:

        start = time.perf_counter()

        try:
            result = function(
                *args,
                **kwargs,
            )

            self.increment(
                f"{operation}_success"
            )

            return result

        except Exception:

            self.increment(
                f"{operation}_failure"
            )

            raise

        finally:

            latency = (
                time.perf_counter()
                - start
            )

            self.record_latency(
                operation,
                latency,
            )

    def get_operation_stats(
        self,
        operation: str,
    ) -> dict[str, Any]:

        values = self.metrics.get(
            operation,
            [],
        )

        if not values:
            return {
                "count": 0,
                "average_latency": 0,
                "min_latency": 0,
                "max_latency": 0,
            }

        return {
            "count": len(values),
            "average_latency": round(
                sum(values) / len(values),
                4,
            ),
            "min_latency": round(
                min(values),
                4,
            ),
            "max_latency": round(
                max(values),
                4,
            ),
        }

    def get_all_stats(
        self,
    ) -> dict[str, Any]:

        return {
            "operations": {
                operation:
                self.get_operation_stats(
                    operation
                )
                for operation
                in self.metrics
            },
            "counters": dict(
                self.counters
            ),
        }

    def reset(self):
        self.metrics.clear()
        self.counters.clear()


pipeline_stats = PipelineStats()