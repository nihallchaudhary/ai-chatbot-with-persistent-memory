import logging
import re
import time
import uuid
from typing import Any

from conversation_manager import (
    ConversationManager,
)
from conversation_summary_manager import (
    ConversationSummaryManager,
)
from memory_manager import MemoryManager
from memory_retriever import MemoryRetriever
from rag_pipeline import RAGPipeline
from response_cache import ResponseCache


logger = logging.getLogger(__name__)


class ChatService:
    """
    Main orchestration service for AI conversations.

    Handles:
    - Conversation history
    - Long-term memory
    - Response caching
    - RAG pipeline execution
    - Source formatting and deduplication
    """

    def __init__(
        self,
        pipeline: RAGPipeline | None = None,
        conversation_manager: (
            ConversationManager | None
        ) = None,
        summary_manager: (
            ConversationSummaryManager | None
        ) = None,
        memory_manager: (
            MemoryManager | None
        ) = None,
        memory_retriever: (
            MemoryRetriever | None
        ) = None,
        response_cache: (
            ResponseCache | None
        ) = None,
    ):

        self.pipeline = (
            pipeline
            or RAGPipeline()
        )

        self.conversation_manager = (
            conversation_manager
            or ConversationManager()
        )

        self.summary_manager = (
            summary_manager
            or ConversationSummaryManager()
        )

        self.memory_manager = (
            memory_manager
            or MemoryManager()
        )

        self.memory_retriever = (
            memory_retriever
            or MemoryRetriever()
        )

        self.response_cache = (
            response_cache
            or ResponseCache()
        )

    # --------------------------------------------------
    # FILENAME CLEANUP
    # --------------------------------------------------

    def _clean_filename(
        self,
        filename: Any,
    ) -> str | None:
        """
        Converts generated upload filenames such as:

        533b6b14-3307-4a50-bb44-809f9c71804b_Resume.pdf

        into:

        Resume.pdf
        """

        if not filename:
            return None

        filename = str(filename).strip()

        if not filename:
            return None

        # Remove UUID prefix followed by "_"
        uuid_prefix_pattern = (
            r"^[0-9a-fA-F]{8}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{4}-"
            r"[0-9a-fA-F]{12}_"
        )

        cleaned_filename = re.sub(
            uuid_prefix_pattern,
            "",
            filename,
        )

        return cleaned_filename

    # --------------------------------------------------
    # SOURCE FORMATTING
    # --------------------------------------------------

    def _format_sources(
        self,
        sources: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Formats and deduplicates retrieved sources.

        Multiple chunks from the same document and page are
        represented by a single source card.
        """

        if not sources:
            return []

        formatted_sources = []

        seen_sources = set()

        for source in sources:

            if not isinstance(
                source,
                dict,
            ):
                continue

            source_metadata = source.get(
                "metadata",
                source,
            )

            if not isinstance(
                source_metadata,
                dict,
            ):
                source_metadata = {}

            filename = self._clean_filename(
                source_metadata.get(
                    "filename"
                )
            )

            page = source_metadata.get(
                "page"
            )

            document_id = source_metadata.get(
                "document_id"
            )

            chunk_id = source.get(
                "id"
            )

            score = source.get(
                "rerank_score"
            )

            if score is None:
                score = source.get(
                    "similarity_score"
                )

            # --------------------------------------------------
            # CREATE UNIQUE SOURCE KEY
            # --------------------------------------------------
            #
            # Same document + same page = same visible source.
            #
            # This prevents:
            #
            # Resume.pdf Page 1
            # Resume.pdf Page 1
            # Resume.pdf Page 1
            #
            # from appearing three times.

            source_key = (
                str(document_id)
                if document_id
                else str(filename),
                str(page)
                if page is not None
                else "",
            )

            if source_key in seen_sources:
                continue

            seen_sources.add(
                source_key
            )

            formatted_sources.append(
                {
                    "filename": filename,

                    "page": page,

                    "document_id":
                    document_id,

                    "chunk_id":
                    chunk_id,

                    "score": score,
                }
            )

        return formatted_sources

    # --------------------------------------------------
    # CHAT
    # --------------------------------------------------

    def chat(
        self,
        query: str,
        user_id: str = "default_user",
        conversation_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:

        start_time = time.perf_counter()

        request_id = str(
            uuid.uuid4()
        )

        # -------------------------
        # CREATE / GET CONVERSATION
        # -------------------------

        conversation_id = (
            self.conversation_manager
            .create_conversation(
                conversation_id
            )
        )

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty."
            )

        # -------------------------
        # CACHE CHECK
        # -------------------------

        cached_response = (
            self.response_cache.get(
                query=query,
                context={
                    "conversation_id":
                    conversation_id
                },
            )
        )

        if cached_response:

            cached_response = (
                cached_response.copy()
            )

            cached_response[
                "request_id"
            ] = request_id

            cached_response[
                "conversation_id"
            ] = conversation_id

            cached_response[
                "cached"
            ] = True

            return cached_response

        # -------------------------
        # SAVE USER MESSAGE
        # -------------------------

        self.conversation_manager.add_message(
            conversation_id=conversation_id,
            role="user",
            content=query,
            metadata=metadata,
        )

        conversation_history = (
            self.conversation_manager
            .get_messages(
                conversation_id,
                limit=10,
            )
        )

        # -------------------------
        # RETRIEVE MEMORY
        # -------------------------

        user_memories = (
            self.memory_manager
            .get_memories(
                user_id,
                limit=50,
            )
        )

        relevant_memories = (
            self.memory_retriever
            .retrieve(
                query=query,
                memories=user_memories,
                top_k=5,
            )
        )

        memory_context = [
            memory["content"]
            for memory
            in relevant_memories
        ]

        # -------------------------
        # RUN RAG PIPELINE
        # -------------------------

        pipeline_result = (
            self.pipeline.run(
                query=query,
                conversation_history=conversation_history,
                memory_context=memory_context,
            )
        )

        answer = (
            pipeline_result.get(
                "answer",
                "",
            )
        )

        # -------------------------
        # SAVE ASSISTANT MESSAGE
        # -------------------------

        self.conversation_manager.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
        )

        # -------------------------
        # UPDATE MEMORY
        # -------------------------

        self.memory_manager.add_memory(
            user_id=user_id,
            content=query,
            memory_type="user_query",
            importance=0.5,
            metadata={
                "conversation_id":
                conversation_id
            },
        )

        # -------------------------
        # UPDATE CONVERSATION SUMMARY
        # -------------------------

        updated_messages = (
            self.conversation_manager
            .get_messages(
                conversation_id
            )
        )

        self.summary_manager.update_summary(
            conversation_id=conversation_id,
            messages=updated_messages,
        )

        # -------------------------
        # FORMAT SOURCES
        # -------------------------

        sources = (
            pipeline_result.get(
                "sources",
                [],
            )
        )

        formatted_sources = (
            self._format_sources(
                sources
            )
        )

        # -------------------------
        # DEBUG SOURCE COUNT
        # -------------------------

        logger.info(
            "SOURCE DEBUG | Raw sources: %s",
            len(sources),
        )

        logger.info(
            "SOURCE DEBUG | Unique sources: %s",
            len(formatted_sources),
        )

        for index, source in enumerate(
            formatted_sources,
            start=1,
        ):

            logger.info(
                "SOURCE DEBUG | Source %s | filename=%s | page=%s",
                index,
                source.get("filename"),
                source.get("page"),
            )

        # -------------------------
        # FINAL RESPONSE
        # -------------------------

        response = {
            "request_id":
            request_id,

            "conversation_id":
            conversation_id,

            "answer":
            answer,

            "sources":
            formatted_sources,

            "model":
            pipeline_result.get(
                "model"
            ),

            "grounded":
            pipeline_result.get(
                "grounded",
                bool(formatted_sources),
            ),

            "cached":
            False,

            "metrics": {
                **pipeline_result.get(
                    "metrics",
                    {},
                ),

                "total_latency":
                round(
                    time.perf_counter()
                    - start_time,
                    4,
                ),
            },
        }

        # -------------------------
        # CACHE RESPONSE
        # -------------------------

        self.response_cache.set(
            query=query,
            value=response,
            context={
                "conversation_id":
                conversation_id
            },
        )

        return response

    # --------------------------------------------------
    # GET CONVERSATION
    # --------------------------------------------------

    def get_conversation(
        self,
        conversation_id: str,
    ):

        return (
            self.conversation_manager
            .get_conversation(
                conversation_id
            )
        )

    # --------------------------------------------------
    # DELETE CONVERSATION
    # --------------------------------------------------

    def delete_conversation(
        self,
        conversation_id: str,
    ) -> bool:

        self.summary_manager.delete_summary(
            conversation_id
        )

        return (
            self.conversation_manager
            .delete_conversation(
                conversation_id
            )
        )