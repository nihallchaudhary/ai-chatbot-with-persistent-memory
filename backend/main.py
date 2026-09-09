import logging

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)

from backend.api import (
    chat,
    conversations,
    documents,
    health,
)
from logging_config import setup_logging


setup_logging()

logger = logging.getLogger(
    __name__
)


app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    description=(
        "Production-oriented AI Knowledge "
        "Assistant using RAG and Gemini."
    ),
    version="1.0.0",
)


# ----------------------------------
# CORS
# ----------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ----------------------------------
# ROUTES
# ----------------------------------

app.include_router(
    chat.router
)

app.include_router(
    documents.router
)

app.include_router(
    conversations.router
)

app.include_router(
    health.router
)


@app.get(
    "/"
)
async def root():

    return {
        "message":
        "Enterprise AI Knowledge "
        "Assistant API is running.",

        "version": "1.0.0",

        "docs": "/docs",
    }


@app.on_event(
    "startup"
)
async def startup_event():

    logger.info(
        "AI Knowledge Assistant "
        "backend started."
    )


@app.on_event(
    "shutdown"
)
async def shutdown_event():

    logger.info(
        "AI Knowledge Assistant "
        "backend stopped."
    )