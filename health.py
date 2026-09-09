import time
from datetime import datetime, timezone

from config import config


class HealthService:
    """
    Performs health checks for important
    application components.
    """

    def __init__(
        self,
        document_store=None,
    ):
        self.document_store = (
            document_store
        )

    def check_vector_database(
        self,
    ) -> dict:

        if not self.document_store:
            return {
                "status": "unknown",
                "message": (
                    "Document store not initialized."
                ),
            }

        try:

            count = (
                self.document_store.count()
            )

            return {
                "status": "healthy",
                "document_chunks": count,
            }

        except Exception as error:

            return {
                "status": "unhealthy",
                "error": str(error),
            }

    def check_configuration(
        self,
    ) -> dict:

        try:

            config.validate()

            return {
                "status": "healthy",
                "gemini_model": (
                    config.GEMINI_MODEL
                ),
            }

        except Exception as error:

            return {
                "status": "unhealthy",
                "error": str(error),
            }

    def get_health(
        self,
    ) -> dict:

        start = time.perf_counter()

        configuration = (
            self.check_configuration()
        )

        vector_database = (
            self.check_vector_database()
        )

        statuses = [
            configuration["status"],
            vector_database["status"],
        ]

        overall_status = (
            "healthy"
            if all(
                status in (
                    "healthy",
                    "unknown",
                )
                for status in statuses
            )
            else "unhealthy"
        )

        return {
            "status": overall_status,
            "timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            "components": {
                "configuration": configuration,
                "vector_database": (
                    vector_database
                ),
            },
            "response_time_ms": round(
                (
                    time.perf_counter()
                    - start
                ) * 1000,
                2,
            ),
        }