from conversation_manager import ConversationManager
from conversation_summary_manager import ConversationSummaryManager
from document_embedder import DocumentEmbedder
from document_loader import DocumentLoader
from document_store import DocumentStore
from memory_manager import MemoryManager
from memory_retriever import MemoryRetriever
from pdf_processor import PDFProcessor
from rag_pipeline import RAGPipeline
from response_cache import ResponseCache

from backend.services.chat_service import ChatService
from backend.services.document_service import DocumentService


class ServiceContainer:
    """
    Central application dependency container.

    Creates shared service instances so all API routes
    operate on the same conversation, memory, document,
    and RAG pipeline instances.
    """

    def __init__(self):

        # ----------------------------------------
        # DOCUMENT / RAG COMPONENTS
        # ----------------------------------------

        self.pdf_processor = PDFProcessor()

        self.document_embedder = (
            DocumentEmbedder()
        )

        self.document_store = (
            DocumentStore()
        )

        self.document_loader = (
            DocumentLoader(
                pdf_processor=self.pdf_processor,
                embedder=self.document_embedder,
                document_store=self.document_store,
            )
        )

        # ----------------------------------------
        # CONVERSATION COMPONENTS
        # ----------------------------------------

        self.conversation_manager = (
            ConversationManager()
        )

        self.conversation_summary_manager = (
            ConversationSummaryManager()
        )

        # ----------------------------------------
        # MEMORY COMPONENTS
        # ----------------------------------------

        self.memory_manager = (
            MemoryManager()
        )

        self.memory_retriever = (
            MemoryRetriever()
        )

        # ----------------------------------------
        # CACHE
        # ----------------------------------------

        self.response_cache = (
            ResponseCache()
        )

        # ----------------------------------------
        # RAG PIPELINE
        # ----------------------------------------

        self.rag_pipeline = (
            RAGPipeline()
        )

        # ----------------------------------------
        # APPLICATION SERVICES
        # ----------------------------------------

        self.chat_service = (
            ChatService(
                pipeline=self.rag_pipeline,
                conversation_manager=
                self.conversation_manager,
                summary_manager=
                self.conversation_summary_manager,
                memory_manager=
                self.memory_manager,
                memory_retriever=
                self.memory_retriever,
                response_cache=
                self.response_cache,
            )
        )

        self.document_service = (
            DocumentService(
                document_loader=
                self.document_loader
            )
        )


# Shared application container

container = ServiceContainer()