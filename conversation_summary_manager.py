from typing import Any


class ConversationSummaryManager:
    """
    Maintains compact summaries of long conversations.

    This prevents the complete conversation history from
    being sent to the LLM for every request.
    """

    def __init__(
        self,
        max_summary_length: int = 2000,
    ):
        self.max_summary_length = max_summary_length
        self.summaries: dict[str, str] = {}

    def create_fallback_summary(
        self,
        messages: list[dict[str, Any]],
    ) -> str:
        """
        Creates a lightweight summary without another LLM call.
        """

        if not messages:
            return ""

        summary_parts = []

        for message in messages[-20:]:
            role = message.get("role", "unknown")
            content = message.get("content", "")

            if content:
                summary_parts.append(
                    f"{role.capitalize()}: {content}"
                )

        summary = "\n".join(summary_parts)

        if len(summary) > self.max_summary_length:
            summary = summary[
                -self.max_summary_length:
            ]

        return summary

    def update_summary(
        self,
        conversation_id: str,
        messages: list[dict[str, Any]],
        summary: str | None = None,
    ) -> str:
        if summary is None:
            summary = self.create_fallback_summary(messages)

        self.summaries[conversation_id] = summary

        return summary

    def get_summary(
        self,
        conversation_id: str,
    ) -> str:
        return self.summaries.get(
            conversation_id,
            "",
        )

    def delete_summary(
        self,
        conversation_id: str,
    ):
        self.summaries.pop(
            conversation_id,
            None,
        )