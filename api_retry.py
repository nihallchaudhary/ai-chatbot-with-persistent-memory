import logging
import time
from typing import Callable, TypeVar


logger = logging.getLogger(__name__)

T = TypeVar("T")


class APIRetryHandler:
    """
    Handles retry logic for external API calls.
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 2.0,
        max_delay: float = 30.0,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def execute(
        self,
        function: Callable[..., T],
        *args,
        **kwargs,
    ) -> T:

        last_error = None

        for attempt in range(
            self.max_retries + 1
        ):
            try:
                return function(
                    *args,
                    **kwargs,
                )

            except Exception as error:
                last_error = error

                if attempt >= self.max_retries:
                    break

                delay = min(
                    self.base_delay * (2 ** attempt),
                    self.max_delay,
                )

                logger.warning(
                    "API request failed. "
                    "Attempt %s/%s. "
                    "Retrying in %.2f seconds. Error: %s",
                    attempt + 1,
                    self.max_retries,
                    delay,
                    error,
                )

                time.sleep(delay)

        logger.error(
            "API request failed after %s attempts.",
            self.max_retries + 1,
        )

        raise RuntimeError(
            f"API request failed: {last_error}"
        )