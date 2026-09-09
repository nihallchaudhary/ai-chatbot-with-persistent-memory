import uuid
from datetime import datetime, timezone
from typing import Any


class ConversationManager:
    """
    Manages multiple conversations and their message history.
    """

    def __init__(self, max_messages: int = 50):
        self.max_messages = max_messages
        self.conversations: dict[str, dict[str, Any]] = {}

    def create_conversation(
        self,
        conversation_id: str | None = None,
    ) -> str:
        conversation_id = conversation_id or str(uuid.uuid4())

        if conversation_id not in self.conversations:
            now = datetime.now(timezone.utc).isoformat()

            self.conversations[conversation_id] = {
                "conversation_id": conversation_id,
                "created_at": now,
                "updated_at": now,
                "messages": [],
                "metadata": {},
            }

        return conversation_id

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if role not in {"user", "assistant", "system"}:
            raise ValueError("Invalid message role.")

        conversation_id = self.create_conversation(conversation_id)

        message = {
            "message_id": str(uuid.uuid4()),
            "role": role,
            "content": content.strip(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }

        conversation = self.conversations[conversation_id]
        conversation["messages"].append(message)

        if len(conversation["messages"]) > self.max_messages:
            conversation["messages"] = conversation["messages"][
                -self.max_messages:
            ]

        conversation["updated_at"] = message["timestamp"]

        return message

    def get_messages(
        self,
        conversation_id: str,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        conversation = self.conversations.get(conversation_id)

        if not conversation:
            return []

        messages = conversation["messages"]

        if limit:
            return messages[-limit:]

        return messages.copy()

    def get_conversation(
        self,
        conversation_id: str,
    ) -> dict[str, Any] | None:
        return self.conversations.get(conversation_id)

    def update_metadata(
        self,
        conversation_id: str,
        metadata: dict[str, Any],
    ):
        self.create_conversation(conversation_id)

        self.conversations[
            conversation_id
        ]["metadata"].update(metadata)

    def delete_conversation(
        self,
        conversation_id: str,
    ) -> bool:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True

        return False

    def get_all_conversations(self) -> list[dict[str, Any]]:
        return [
            {
                "conversation_id": conversation_id,
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "message_count": len(data["messages"]),
                "metadata": data["metadata"],
            }
            for conversation_id, data
            in self.conversations.items()
        ]