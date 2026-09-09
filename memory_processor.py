import re
from typing import Any


class MemoryProcessor:
    """
    Processes conversation information before storing it
    as long-term memory.
    """

    STOP_PATTERNS = [
        r"^hi$",
        r"^hello$",
        r"^hey$",
        r"^thanks?$",
        r"^thank you$",
        r"^ok$",
        r"^okay$",
        r"^bye$",
    ]

    def normalize(
        self,
        text: str,
    ) -> str:
        text = text.strip()

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text

    def is_useful_memory(
        self,
        content: str,
    ) -> bool:
        content = self.normalize(content)

        if len(content) < 10:
            return False

        normalized = content.lower().strip(
            " .!?",
        )

        for pattern in self.STOP_PATTERNS:
            if re.match(pattern, normalized):
                return False

        return True

    def create_memory(
        self,
        content: str,
        memory_type: str = "conversation",
        importance: float = 0.5,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        content = self.normalize(content)

        if not self.is_useful_memory(content):
            return None

        return {
            "content": content,
            "memory_type": memory_type,
            "importance": max(
                0.0,
                min(float(importance), 1.0),
            ),
            "metadata": metadata or {},
        }