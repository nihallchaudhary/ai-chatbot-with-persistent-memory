from unittest.mock import Mock

from document_retriever import (
    DocumentRetriever,
)


def test_document_retrieval():

    embedder = Mock()

    embedder.embed_query.return_value = [
        0.1,
        0.2,
        0.3,
    ]

    store = Mock()

    store.search.return_value = [
        {
            "id": "chunk_1",
            "text": (
                "Artificial intelligence uses "
                "machine learning."
            ),
            "metadata": {
                "filename": "test.pdf"
            },
            "similarity_score": 0.92,
        }
    ]

    retriever = DocumentRetriever(
        embedder=embedder,
        store=store,
    )

    results = retriever.retrieve(
        "What is artificial intelligence?"
    )

    assert len(results) == 1

    assert (
        results[0]["id"]
        == "chunk_1"
    )

    assert (
        results[0]["similarity_score"]
        == 0.92
    )