# 🧠 AI Knowledge Assistant

## Full-Stack RAG Application with Semantic Search, Reranking, Conversational Memory & Google Gemini

<p align="center">

  <strong>
    An intelligent document-grounded AI assistant that transforms uploaded PDFs into an interactive knowledge base.
  </strong>

</p>

<p align="center">

  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react" />
  <img src="https://img.shields.io/badge/Google-Gemini-4285F4?style=for-the-badge&logo=google" />
  <img src="https://img.shields.io/badge/ChromaDB-Vector%20Database-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/RAG-AI%20Pipeline-purple?style=for-the-badge" />

</p>

---

# 📌 Overview

**AI Knowledge Assistant** is a full-stack Retrieval-Augmented Generation (RAG) application designed to let users interact with their own documents using natural-language queries.

Instead of simply sending a user's question to an LLM and relying on its pre-trained knowledge, the application first retrieves relevant information from uploaded documents.

The retrieved information is then:

1. Processed and normalized
2. Rewritten when necessary
3. Converted into vector embeddings
4. Retrieved using semantic similarity search
5. Reranked using a Cross-Encoder
6. Filtered to remove redundant or excessive context
7. Combined with conversation and memory context
8. Sent to Google Gemini for response generation

The final response is returned together with source information from the retrieved document chunks.

---

# 🎯 Problem Statement

Large Language Models are powerful, but they do not automatically know the contents of a user's private documents.

A simple LLM chatbot can also:

- Hallucinate information
- Ignore relevant document content
- Lose conversational context
- Struggle with long documents
- Provide answers without showing where information came from

This project addresses these problems by implementing a complete document-grounded AI pipeline.

The system separates **knowledge retrieval** from **response generation**:

```text
User Query
     │
     ▼
Retrieve Relevant Knowledge
     │
     ▼
Rank & Filter Context
     │
     ▼
Generate Response
     │
     ▼
Answer + Sources
