import uuid
from datetime import datetime, timezone
from typing import Any

from memory_processor import MemoryProcessor


class MemoryManager:
    """
    Long-term memory management system.

    Supports:
    - Conversation memory
    - User preferences
    - Important facts
    - Metadata
    - Importance scoring
    """

    def __init__(
        self,
        processor: MemoryProcessor | None = None,
        max_memories_per_user: int = 500,
    ):
        self.processor = (
            processor
            or MemoryProcessor()
        )

        self.max_memories_per_user = (
            max_memories_per_user
        )

        self.memories: dict[
            str,
            list[dict[str, Any]]
        ] = {}

    def add_memory(
        self,
        user_id: str,
        content: str,
        memory_type: str = "conversation",
        importance: float = 0.5,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:

        memory_data = (
            self.processor.create_memory(
                content=content,
                memory_type=memory_type,
                importance=importance,
                metadata=metadata,
            )
        )

        if not memory_data:
            return None

        memory = {
            "memory_id": str(uuid.uuid4()),
            "user_id": user_id,
            **memory_data,
            "created_at": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
            "access_count": 0,
            "last_accessed": None,
        }

        if user_id not in self.memories:
            self.memories[user_id] = []

        self.memories[user_id].append(
            memory
        )

        self._enforce_limit(user_id)

        return memory

    def _enforce_limit(
        self,
        user_id: str,
    ):
        user_memories = self.memories.get(
            user_id,
            [],
        )

        if (
            len(user_memories)
            <= self.max_memories_per_user
        ):
            return

        user_memories.sort(
            key=lambda memory: (
                memory["importance"],
                memory["access_count"],
                memory["created_at"],
            ),
            reverse=True,
        )

        self.memories[user_id] = (
            user_memories[
                :self.max_memories_per_user
            ]
        )

    def get_memories(
        self,
        user_id: str,
        limit: int = 10,
    ) -> list[dict[str, Any]]:

        memories = self.memories.get(
            user_id,
            [],
        )

        ranked = sorted(
            memories,
            key=lambda memory: (
                memory["importance"],
                memory["access_count"],
            ),
            reverse=True,
        )

        selected = ranked[:limit]

        for memory in selected:
            memory["access_count"] += 1
            memory["last_accessed"] = (
                datetime.now(
                    timezone.utc
                ).isoformat()
            )

        return selected

    def delete_memory(
        self,
        user_id: str,
        memory_id: str,
    ) -> bool:

        memories = self.memories.get(
            user_id,
            [],
        )

        for index, memory in enumerate(
            memories
        ):
            if memory["memory_id"] == memory_id:
                memories.pop(index)
                return True

        return False

    def clear_memories(
        self,
        user_id: str,
    ):
        self.memories.pop(
            user_id,
            None,
        )

    def get_memory_count(
        self,
        user_id: str,
    ) -> int:
        return len(
            self.memories.get(
                user_id,
                [],
            )
        )