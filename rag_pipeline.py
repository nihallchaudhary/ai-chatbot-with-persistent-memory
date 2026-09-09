import logging
import time
from typing import Any

from config import config
from query_normalizer import QueryNormalizer
from query_rewriter import QueryRewriter
from document_retriever import DocumentRetriever
from reranker import Reranker
from context_filter import ContextFilter
from rag_generator import RAGGenerator


logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Advanced RAG orchestration pipeline.

    Flow:

    Query
      ↓
    Normalization
      ↓
    Query Rewriting
      ↓
    Retrieval
      ↓
    Reranking
      ↓
    Context Filtering
      ↓
    Gemini Generation
      ↓
    Answer + Sources + Metrics
    """

    def __init__(
        self,
        query_normalizer=None,
        query_rewriter=None,
        retriever=None,
        reranker=None,
        context_filter=None,
        generator=None,
    ):

        self.query_normalizer = (
            query_normalizer
            or QueryNormalizer()
        )

        self.query_rewriter = (
            query_rewriter
            or QueryRewriter()
        )

        self.retriever = (
            retriever
            or DocumentRetriever()
        )

        self.reranker = (
            reranker
            or Reranker()
        )

        self.context_filter = (
            context_filter
            or ContextFilter()
        )

        self.generator = (
            generator
            or RAGGenerator()
        )

    # --------------------------------------------------
    # SAFE COMPONENT EXECUTION
    # --------------------------------------------------

    def _call_method(
        self,
        component: Any,
        possible_methods: list[str],
        *args,
        **kwargs,
    ):

        for method_name in possible_methods:

            method = getattr(
                component,
                method_name,
                None,
            )

            if callable(method):
                return method(
                    *args,
                    **kwargs,
                )

        raise AttributeError(
            f"No compatible method found in "
            f"{component.__class__.__name__}. "
            f"Expected one of: "
            f"{possible_methods}"
        )

    # --------------------------------------------------
    # QUERY NORMALIZATION
    # --------------------------------------------------

    def normalize_query(
        self,
        query: str,
    ) -> str:

        try:

            return self._call_method(
                self.query_normalizer,
                [
                    "normalize",
                    "process",
                    "clean_query",
                ],
                query,
            )

        except Exception as error:

            logger.warning(
                "Query normalization failed: %s",
                error,
            )

            return query.strip()

    # --------------------------------------------------
    # QUERY REWRITING
    # --------------------------------------------------

    def rewrite_query(
        self,
        query: str,
        conversation_history=None,
    ) -> str:

        try:

            for method_name in [
                "rewrite",
                "rewrite_query",
                "process",
            ]:

                method = getattr(
                    self.query_rewriter,
                    method_name,
                    None,
                )

                if callable(method):

                    try:

                        return method(
                            query,
                            conversation_history,
                        )

                    except TypeError:

                        return method(query)

        except Exception as error:

            logger.warning(
                "Query rewriting failed: %s",
                error,
            )

        return query

    # --------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------

    def retrieve_documents(
        self,
        query: str,
    ) -> list[dict]:

        try:

            for method_name in [
                "retrieve",
                "search",
                "get_relevant_documents",
            ]:

                method = getattr(
                    self.retriever,
                    method_name,
                    None,
                )

                if callable(method):

                    try:

                        results = method(
                            query,
                            top_k=(
                                config.RETRIEVAL_TOP_K
                            ),
                        )

                    except TypeError:

                        results = method(query)

                    logger.info(
                        "RAG DEBUG | Retrieved documents: %s",
                        len(results) if results else 0,
                    )

                    return results

        except Exception as error:

            logger.exception(
                "Document retrieval failed: %s",
                error,
            )

        logger.info(
            "RAG DEBUG | Retrieved documents: 0"
        )

        return []

    # --------------------------------------------------
    # RERANKING
    # --------------------------------------------------

    def rerank_documents(
        self,
        query: str,
        documents: list[dict],
    ) -> list[dict]:

        if not documents:

            logger.info(
                "RAG DEBUG | Reranked documents: 0"
            )

            return []

        try:

            for method_name in [
                "rerank",
                "rank",
            ]:

                method = getattr(
                    self.reranker,
                    method_name,
                    None,
                )

                if callable(method):

                    try:

                        results = method(
                            query,
                            documents,
                            top_k=(
                                config.RERANK_TOP_K
                            ),
                        )

                    except TypeError:

                        results = method(
                            query,
                            documents,
                        )

                    logger.info(
                        "RAG DEBUG | Reranked documents: %s",
                        len(results) if results else 0,
                    )

                    return results

        except Exception as error:

            logger.warning(
                "Reranking failed: %s",
                error,
            )

        results = documents[
            :config.RERANK_TOP_K
        ]

        logger.info(
            "RAG DEBUG | Reranked documents: %s",
            len(results),
        )

        return results

    # --------------------------------------------------
    # CONTEXT FILTERING
    # --------------------------------------------------

    def filter_context(
        self,
        documents: list[dict],
    ) -> list[dict]:

        if not documents:

            logger.info(
                "RAG DEBUG | Context documents: 0"
            )

            return []

        try:

            for method_name in [
                "filter",
                "filter_context",
                "process",
            ]:

                method = getattr(
                    self.context_filter,
                    method_name,
                    None,
                )

                if callable(method):

                    results = method(
                        documents
                    )

                    logger.info(
                        "RAG DEBUG | Context documents: %s",
                        len(results) if results else 0,
                    )

                    return results

        except Exception as error:

            logger.warning(
                "Context filtering failed: %s",
                error,
            )

        logger.info(
            "RAG DEBUG | Context documents: %s",
            len(documents),
        )

        return documents

    # --------------------------------------------------
    # MAIN PIPELINE
    # --------------------------------------------------

    def run(
        self,
        query: str,
        conversation_history=None,
        memory_context=None,
    ) -> dict[str, Any]:

        pipeline_start = time.perf_counter()

        if not query or not query.strip():

            raise ValueError(
                "Query cannot be empty."
            )

        # Step 1
        normalized_query = (
            self.normalize_query(query)
        )

        logger.info(
            "RAG DEBUG | Original query: %s",
            query,
        )

        logger.info(
            "RAG DEBUG | Normalized query: %s",
            normalized_query,
        )

        # Step 2
        rewritten_query = (
            self.rewrite_query(
                normalized_query,
                conversation_history,
            )
        )

        logger.info(
            "RAG DEBUG | Retrieval query: %s",
            rewritten_query,
        )

        # Step 3
        retrieved_documents = (
            self.retrieve_documents(
                rewritten_query
            )
        )

        # Step 4
        reranked_documents = (
            self.rerank_documents(
                normalized_query,
                retrieved_documents,
            )
        )

        # Step 5
        filtered_documents = (
            self.filter_context(
                reranked_documents
            )
        )

        # --------------------------------------------------
        # DEBUG DOCUMENT INFORMATION
        # --------------------------------------------------

        logger.info(
            "RAG DEBUG | Final context documents: %s",
            len(filtered_documents),
        )

        for index, document in enumerate(
            filtered_documents,
            start=1,
        ):

            logger.info(
                "RAG DEBUG | Context %s | id=%s | metadata=%s | similarity=%s | rerank=%s",
                index,
                document.get("id"),
                document.get("metadata"),
                document.get("similarity_score"),
                document.get("rerank_score"),
            )

        # Step 6
        generation_result = (
            self.generator.generate_response(
                query=normalized_query,
                retrieved_documents=(
                    filtered_documents
                ),
                conversation_history=(
                    conversation_history
                ),
                memory_context=(
                    memory_context
                ),
            )
        )

        latency = (
            time.perf_counter()
            - pipeline_start
        )

        generation_result.update(
            {
                "original_query": query,
                "normalized_query": (
                    normalized_query
                ),
                "retrieval_query": (
                    rewritten_query
                ),
                "pipeline_latency": round(
                    latency,
                    4,
                ),
                "metrics": {
                    "retrieved_documents": len(
                        retrieved_documents
                    ),
                    "reranked_documents": len(
                        reranked_documents
                    ),
                    "context_documents": len(
                        filtered_documents
                    ),
                    "pipeline_latency_seconds": (
                        round(latency, 4)
                    ),
                },
            }
        )

        return generation_result

    # --------------------------------------------------
    # COMPATIBILITY METHODS
    # --------------------------------------------------

    def process(
        self,
        query: str,
        conversation_history=None,
        memory_context=None,
    ):

        return self.run(
            query,
            conversation_history,
            memory_context,
        )

    def answer(
        self,
        query: str,
        conversation_history=None,
        memory_context=None,
    ):

        return self.run(
            query,
            conversation_history,
            memory_context,
        )