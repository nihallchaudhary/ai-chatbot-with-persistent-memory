import hashlib
import logging
import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from config import config


logger = logging.getLogger(__name__)


class PDFProcessor:
    """
    Extracts and prepares text from PDF documents.

    Features:
    - Multi-page extraction
    - Text cleaning
    - Page metadata
    - Document hashing
    - Chunk creation
    """

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        self.chunk_size = chunk_size or config.CHUNK_SIZE
        self.chunk_overlap = (
            chunk_overlap or config.CHUNK_OVERLAP
        )

    def _clean_text(
        self,
        text: str,
    ) -> str:
        if not text:
            return ""

        text = text.replace("\x00", " ")

        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()

    def _generate_document_id(
        self,
        file_path: str,
    ) -> str:
        path = Path(file_path)

        hasher = hashlib.sha256()

        with path.open("rb") as file:
            for chunk in iter(
                lambda: file.read(8192),
                b"",
            ):
                hasher.update(chunk)

        return hasher.hexdigest()[:20]

    def extract_pages(
        self,
        file_path: str,
    ) -> list[dict[str, Any]]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF not found: {file_path}"
            )

        reader = PdfReader(file_path)

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            try:
                text = page.extract_text() or ""

                text = self._clean_text(text)

                if text:
                    pages.append(
                        {
                            "page": page_number,
                            "text": text,
                        }
                    )

            except Exception as error:
                logger.warning(
                    "Failed to extract page %s: %s",
                    page_number,
                    error,
                )

        return pages

    def split_text(
        self,
        text: str,
    ) -> list[str]:
        if not text:
            return []

        chunks = []

        start = 0

        while start < len(text):

            end = min(
                start + self.chunk_size,
                len(text),
            )

            if end < len(text):

                last_break = max(
                    text.rfind(
                        "\n",
                        start,
                        end,
                    ),
                    text.rfind(
                        ". ",
                        start,
                        end,
                    ),
                    text.rfind(
                        " ",
                        start,
                        end,
                    ),
                )

                if last_break > start:
                    end = last_break + 1

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            next_start = (
                end - self.chunk_overlap
            )

            if next_start <= start:
                next_start = end

            start = next_start

        return chunks

    def process(
        self,
        file_path: str,
    ) -> list[dict[str, Any]]:

        path = Path(file_path)

        document_id = (
            self._generate_document_id(
                file_path
            )
        )

        pages = self.extract_pages(
            file_path
        )

        chunks = []

        for page_data in pages:

            page_number = (
                page_data["page"]
            )

            page_chunks = self.split_text(
                page_data["text"]
            )

            for chunk_index, text in enumerate(
                page_chunks
            ):

                chunk_id = (
                    f"{document_id}_"
                    f"p{page_number}_"
                    f"c{chunk_index}"
                )

                chunks.append(
                    {
                        "id": chunk_id,
                        "text": text,
                        "metadata": {
                            "document_id": (
                                document_id
                            ),
                            "filename": (
                                path.name
                            ),
                            "source": (
                                str(path)
                            ),
                            "page": (
                                page_number
                            ),
                            "chunk_index": (
                                chunk_index
                            ),
                        },
                    }
                )

        logger.info(
            "Processed %s pages into %s chunks.",
            len(pages),
            len(chunks),
        )

        return chunks

    def process_pdf(
        self,
        file_path: str,
    ) -> list[dict[str, Any]]:
        return self.process(file_path)