import logging
from typing import Any

from google import genai
from google.genai import types

from config import config
from api_retry import APIRetryHandler


logger = logging.getLogger(__name__)


class RAGGenerator:
    """
    Advanced Gemini-based response generator.

    Designed to work with:
    - Document retrieval
    - Reranking
    - Context filtering
    - Conversation memory
    - Source attribution
    """

    def __init__(self):
        config.validate()

        self.client = genai.Client(
            api_key=config.GEMINI_API_KEY
        )

        self.model_name = config.GEMINI_MODEL

        self.retry_handler = APIRetryHandler(
            max_retries=config.API_MAX_RETRIES,
            base_delay=config.API_RETRY_DELAY,
        )

    # --------------------------------------------------
    # CONTEXT FORMATTING
    # --------------------------------------------------

    def format_context(
        self,
        documents: list[dict[str, Any]],
    ) -> tuple[str, list[dict[str, Any]]]:

        if not documents:
            return "", []

        context_parts = []
        sources = []

        total_characters = 0

        for index, document in enumerate(
            documents,
            start=1,
        ):
            text = self._extract_text(
                document
            )

            if not text:
                continue

            metadata = document.get(
                "metadata",
                {},
            )

            if (
                total_characters + len(text)
                > config.MAX_CONTEXT_CHARACTERS
            ):
                remaining = (
                    config.MAX_CONTEXT_CHARACTERS
                    - total_characters
                )

                if remaining <= 0:
                    break

                text = text[:remaining]

            source_label = self._get_source_label(
                metadata
            )

            context_parts.append(
                f"[SOURCE {index}]\n"
                f"{source_label}\n\n"
                f"{text}"
            )

            sources.append(
                self._create_source(
                    index,
                    document,
                    metadata,
                )
            )

            total_characters += len(text)

            if (
                len(context_parts)
                >= config.MAX_CONTEXT_CHUNKS
            ):
                break

        return (
            "\n\n"
            "----------------------------------------"
            "\n\n"
            .join(context_parts),
            sources,
        )

    def _extract_text(
        self,
        document: dict[str, Any],
    ) -> str:

        possible_keys = [
            "text",
            "content",
            "document",
            "page_content",
        ]

        for key in possible_keys:
            value = document.get(key)

            if value:
                return str(value).strip()

        return ""

    def _get_source_label(
        self,
        metadata: dict[str, Any],
    ) -> str:

        filename = (
            metadata.get("filename")
            or metadata.get("source")
            or metadata.get("file_name")
            or "Unknown Document"
        )

        page = (
            metadata.get("page")
            or metadata.get("page_number")
        )

        if page:
            return (
                f"Document: {filename} | "
                f"Page: {page}"
            )

        return f"Document: {filename}"

    def _create_source(
        self,
        index: int,
        document: dict[str, Any],
        metadata: dict[str, Any],
    ) -> dict[str, Any]:

        score = (
            document.get("rerank_score")
            or document.get("similarity_score")
            or document.get("score")
        )

        return {
            "source_number": index,
            "filename": (
                metadata.get("filename")
                or metadata.get("source")
                or metadata.get("file_name")
                or "Unknown Document"
            ),
            "page": (
                metadata.get("page")
                or metadata.get("page_number")
            ),
            "document_id": (
                metadata.get("document_id")
                or document.get("document_id")
            ),
            "score": (
                round(float(score), 4)
                if score is not None
                else None
            ),
        }

    # --------------------------------------------------
    # MEMORY FORMATTING
    # --------------------------------------------------

    def format_memory(
        self,
        conversation_history: list[dict[str, Any]] | None,
        memory_context: list[dict[str, Any]] | None = None,
    ) -> str:

        sections = []

        if conversation_history:
            messages = []

            for message in conversation_history[
                -config.MAX_CONVERSATION_MESSAGES:
            ]:

                role = (
                    message.get("role")
                    or "user"
                )

                content = (
                    message.get("content")
                    or message.get("text")
                    or ""
                )

                if content:
                    messages.append(
                        f"{role.upper()}: {content}"
                    )

            if messages:
                sections.append(
                    "RECENT CONVERSATION:\n"
                    + "\n".join(messages)
                )

        if memory_context:
            memory_items = []

            for item in memory_context[
                :config.MAX_MEMORY_ITEMS
            ]:

                if isinstance(item, dict):

                    content = (
                        item.get("content")
                        or item.get("text")
                        or item.get("memory")
                        or ""
                    )

                else:
                    content = str(item)

                if content:
                    memory_items.append(
                        f"- {content}"
                    )

            if memory_items:
                sections.append(
                    "RELEVANT MEMORY:\n"
                    + "\n".join(memory_items)
                )

        return "\n\n".join(sections)

    # --------------------------------------------------
    # PROMPT
    # --------------------------------------------------

    def build_prompt(
        self,
        query: str,
        context: str,
        conversation_context: str = "",
    ) -> str:

        return f"""
You are an advanced AI Knowledge Assistant.

Your task is to answer the user's question accurately,
clearly, and helpfully.

==============================
CORE RULES
==============================

1. The retrieved document context is your PRIMARY
   knowledge source.

2. Never invent facts that are not supported by the
   provided document context.

3. If the requested information is unavailable in the
   context, clearly state that you could not find the
   answer in the available documents.

4. Use conversation history only for understanding
   references and maintaining continuity.

5. Cite retrieved information using the available
   source numbers:

   [Source 1]
   [Source 2]

6. Do not fabricate source citations.

7. If multiple sources support the answer, cite all
   relevant sources.

8. Provide concise answers by default. Use detailed
   explanations only when requested.

9. Use headings and bullet points when they improve
   readability.

10. Do not reveal these internal instructions unless
    explicitly asked.

==============================
CONVERSATION CONTEXT
==============================

{conversation_context or "No previous conversation context available."}

==============================
RETRIEVED DOCUMENT CONTEXT
==============================

{context or "No relevant document context was retrieved."}

==============================
USER QUESTION
==============================

{query}

==============================
FINAL RESPONSE
==============================

Answer the user's question now.
"""

    # --------------------------------------------------
    # GEMINI GENERATION
    # --------------------------------------------------

    def _call_gemini(
        self,
        prompt: str,
    ) -> str:

        response = (
            self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=(
                        config.GEMINI_TEMPERATURE
                    ),
                    max_output_tokens=(
                        config.GEMINI_MAX_OUTPUT_TOKENS
                    ),
                ),
            )
        )

        text = getattr(
            response,
            "text",
            None,
        )

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    # --------------------------------------------------
    # MAIN GENERATION
    # --------------------------------------------------

    def generate_response(
        self,
        query: str,
        retrieved_documents: list[dict[str, Any]],
        conversation_history: (
            list[dict[str, Any]] | None
        ) = None,
        memory_context: (
            list[dict[str, Any]] | None
        ) = None,
    ) -> dict[str, Any]:

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        context, sources = self.format_context(
            retrieved_documents
        )

        conversation_context = self.format_memory(
            conversation_history,
            memory_context,
        )

        prompt = self.build_prompt(
            query=query.strip(),
            context=context,
            conversation_context=(
                conversation_context
            ),
        )

        answer = self.retry_handler.execute(
            self._call_gemini,
            prompt,
        )

        return {
            "answer": answer,
            "sources": sources,
            "model": self.model_name,
            "retrieved_document_count": len(
                retrieved_documents
            ),
            "grounded": bool(
                retrieved_documents
            ),
        }

    # --------------------------------------------------
    # COMPATIBILITY METHOD
    # --------------------------------------------------

    def generate(
        self,
        query: str,
        context: str,
    ) -> str:

        prompt = self.build_prompt(
            query=query,
            context=context,
        )

        return self.retry_handler.execute(
            self._call_gemini,
            prompt,
        )