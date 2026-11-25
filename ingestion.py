from dataclasses import dataclass
from pathlib import Path


DOCUMENTS_DIR = Path(__file__).parent / "documents"


@dataclass
class DocumentChunk:
    source: str
    chunk_number: int
    text: str


def split_text(text: str, words_per_chunk: int = 100):
    words = text.split()
    return [
        " ".join(words[start : start + words_per_chunk])
        for start in range(0, len(words), words_per_chunk)
    ]


def ingest_documents(folder: Path = DOCUMENTS_DIR):
    chunks = []

    for document_path in sorted(folder.glob("*.txt")):
        text = document_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        document_chunks = split_text(text)
        for number, chunk in enumerate(document_chunks, start=1):
            chunks.append(
                DocumentChunk(
                    source=document_path.name,
                    chunk_number=number,
                    text=chunk,
                )
            )

    return chunks
