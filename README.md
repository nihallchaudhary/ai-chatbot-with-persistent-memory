# 🧠 AI Knowledge Assistant

### Full-Stack Retrieval-Augmented Generation System

<p align="center">
  <b>Turn your documents into an intelligent, searchable knowledge base.</b>
</p>

<p align="center">
  A production-style AI application combining RAG, semantic retrieval,
  vector embeddings, Cross-Encoder reranking, contextual memory,
  response caching, and Google Gemini.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=flat-square&logo=react&logoColor=black)
![Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?style=flat-square&logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-orange?style=flat-square)
![RAG](https://img.shields.io/badge/RAG-Architecture-purple?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white)

</p>

---

# 🚀 What Is This?

**AI Knowledge Assistant** is a full-stack document intelligence application that allows users to upload PDF documents and ask questions about their contents using natural language.

Instead of directly sending every question to an LLM, the application first retrieves relevant information from the user's documents.

The retrieved information is then:

```text
Query
  ↓
Normalization
  ↓
Query Rewriting
  ↓
Semantic Retrieval
  ↓
Cross-Encoder Reranking
  ↓
Context Filtering
  ↓
Conversation + Memory Context
  ↓
Google Gemini
  ↓
Grounded Answer
  ↓
Source Attribution
