import re


class QueryRewriter:
    """
    Converts conversational follow-up questions into
    better standalone retrieval queries.

    Uses conversation context without unnecessarily
    calling another LLM API.
    """

    FOLLOW_UP_PATTERNS = [
        r"^(what about|how about)\b",
        r"^(tell me more)\b",
        r"^(explain more)\b",
        r"^(and what)\b",
        r"^(what else)\b",
    ]

    def is_follow_up(
        self,
        query: str,
    ) -> bool:

        normalized = query.lower().strip()

        return any(
            re.search(
                pattern,
                normalized,
            )
            for pattern
            in self.FOLLOW_UP_PATTERNS
        )

    def get_last_user_topic(
        self,
        conversation_history: (
            list[dict] | None
        ),
    ) -> str:

        if not conversation_history:
            return ""

        for message in reversed(
            conversation_history
        ):
            if (
                message.get("role")
                == "user"
            ):
                content = message.get(
                    "content",
                    ""
                ).strip()

                if content:
                    return content

        return ""

    def rewrite(
        self,
        query: str,
        conversation_history=None,
    ) -> str:

        query = query.strip()

        if not self.is_follow_up(
            query
        ):
            return query

        previous_topic = (
            self.get_last_user_topic(
                conversation_history
            )
        )

        if not previous_topic:
            return query

        return (
            f"{previous_topic}. "
            f"Follow-up question: {query}"
        )

    def rewrite_query(
        self,
        query: str,
        conversation_history=None,
    ) -> str:

        return self.rewrite(
            query,
            conversation_history,
        )