from unittest.mock import Mock

from rag_pipeline import RAGPipeline


def test_pipeline_returns_answer():

    normalizer = Mock()
    normalizer.normalize.return_value = (
        "What is artificial intelligence?"
    )

    rewriter = Mock()
    rewriter.rewrite.return_value = (
        "What is artificial intelligence?"
    )

    retriever = Mock()
    retriever.retrieve.return_value = [
        {
            "text": (
                "Artificial intelligence is a "
                "field of computer science."
            ),
            "metadata": {
                "filename": "ai.pdf"
            },
        }
    ]

    reranker = Mock()
    reranker.rerank.return_value = (
        retriever.retrieve.return_value
    )

    context_filter = Mock()
    context_filter.filter.return_value = (
        reranker.rerank.return_value
    )

    generator = Mock()
    generator.generate_response.return_value = {
        "answer": (
            "Artificial intelligence is a field "
            "of computer science."
        ),
        "sources": [
            {
                "filename": "ai.pdf"
            }
        ],
        "model": "test-model",
        "grounded": True,
    }

    pipeline = RAGPipeline(
        query_normalizer=normalizer,
        query_rewriter=rewriter,
        retriever=retriever,
        reranker=reranker,
        context_filter=context_filter,
        generator=generator,
    )

    result = pipeline.run(
        "What is artificial intelligence?"
    )

    assert "answer" in result

    assert result["grounded"] is True

    assert (
        result["metrics"]
        ["retrieved_documents"]
        == 1
    )


def test_empty_query_raises_error():

    pipeline = RAGPipeline.__new__(
        RAGPipeline
    )

    try:
        pipeline.run("")
        assert False

    except ValueError:
        assert True