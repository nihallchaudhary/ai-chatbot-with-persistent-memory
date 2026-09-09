# Enterprise AI Knowledge Assistant

An advanced Retrieval-Augmented Generation (RAG) system built using Python, FastAPI, Google Gemini, ChromaDB, semantic search, reranking, conversation memory, and production-oriented deployment practices.

## Features

- Retrieval-Augmented Generation (RAG)
- Google Gemini LLM integration
- PDF document processing
- Semantic vector search
- Local document embeddings
- ChromaDB vector database
- Cross-encoder reranking
- Context filtering
- Query normalization
- Query rewriting
- Multi-turn conversations
- Conversation management
- Long-term memory
- Response caching
- Source attribution
- Pipeline performance metrics
- Health monitoring
- REST API
- Automated testing
- Docker containerization
- CI/CD using GitHub Actions

---

# Architecture

```text
                        User Query
                            |
                            v
                    Query Normalization
                            |
                            v
                     Query Rewriting
                            |
                            v
                     Semantic Retrieval
                            |
                            v
                       Vector Database
                            |
                            v
                         Reranking
                            |
                            v
                     Context Filtering
                            |
                            v
                   Conversation + Memory
                            |
                            v
                      Gemini LLM
                            |
                            v
                 Answer + Source Citations