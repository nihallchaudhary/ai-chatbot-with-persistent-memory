import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    # --------------------------------------------------
    # APPLICATION
    # --------------------------------------------------

    APP_NAME = "Enterprise AI Knowledge Assistant"
    APP_VERSION = "2.0.0"

    DEBUG = os.getenv(
        "DEBUG",
        "False",
    ).lower() == "true"

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )

    # --------------------------------------------------
    # GEMINI
    # --------------------------------------------------

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY",
    )

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    GEMINI_TEMPERATURE = float(
        os.getenv(
            "GEMINI_TEMPERATURE",
            "0.3",
        )
    )

    GEMINI_MAX_OUTPUT_TOKENS = int(
        os.getenv(
            "GEMINI_MAX_OUTPUT_TOKENS",
            "2048",
        )
    )

    API_MAX_RETRIES = int(
        os.getenv(
            "API_MAX_RETRIES",
            "3",
        )
    )

    API_RETRY_DELAY = float(
        os.getenv(
            "API_RETRY_DELAY",
            "2",
        )
    )

    # --------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------

    RETRIEVAL_TOP_K = int(
        os.getenv(
            "RETRIEVAL_TOP_K",
            "10",
        )
    )

    RERANK_TOP_K = int(
        os.getenv(
            "RERANK_TOP_K",
            "5",
        )
    )

    MIN_RELEVANCE_SCORE = float(
        os.getenv(
            "MIN_RELEVANCE_SCORE",
            "0.15",
        )
    )

    # --------------------------------------------------
    # CONTEXT
    # --------------------------------------------------

    MAX_CONTEXT_CHUNKS = int(
        os.getenv(
            "MAX_CONTEXT_CHUNKS",
            "5",
        )
    )

    MAX_CONTEXT_CHARACTERS = int(
        os.getenv(
            "MAX_CONTEXT_CHARACTERS",
            "15000",
        )
    )

    # --------------------------------------------------
    # MEMORY
    # --------------------------------------------------

    MAX_CONVERSATION_MESSAGES = int(
        os.getenv(
            "MAX_CONVERSATION_MESSAGES",
            "10",
        )
    )

    MAX_MEMORY_ITEMS = int(
        os.getenv(
            "MAX_MEMORY_ITEMS",
            "10",
        )
    )

    # --------------------------------------------------
    # CACHE
    # --------------------------------------------------

    ENABLE_CACHE = os.getenv(
        "ENABLE_CACHE",
        "true",
    ).lower() == "true"

    CACHE_TTL = int(
        os.getenv(
            "CACHE_TTL",
            "3600",
        )
    )

    # --------------------------------------------------
    # DOCUMENT PROCESSING
    # --------------------------------------------------

    CHUNK_SIZE = int(
        os.getenv(
            "CHUNK_SIZE",
            "800",
        )
    )

    CHUNK_OVERLAP = int(
        os.getenv(
            "CHUNK_OVERLAP",
            "150",
        )
    )

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Add it to your .env file."
            )

        return True


config = Config()