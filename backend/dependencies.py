from backend.services.service_container import (
    container,
)


def get_chat_service():
    return container.chat_service


def get_document_service():
    return container.document_service


def get_document_store():
    return container.document_store


def get_service_container():
    return container