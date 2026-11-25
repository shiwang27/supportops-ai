import math
import re
from collections import Counter
from dataclasses import dataclass

from ingestion import DocumentChunk, ingest_documents


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "can",
    "do",
    "for",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "with",
}


@dataclass
class SearchResult:
    source: str
    chunk_number: int
    text: str
    score: float


class VectorSearch:
    def __init__(self, chunks: list[DocumentChunk]):
        self.chunks = chunks
        self.idf = self._build_idf(chunks)
        self.vectors = [self._make_vector(chunk.text) for chunk in chunks]

    @classmethod
    def from_documents(cls):
        return cls(ingest_documents())

    @staticmethod
    def _tokenize(text: str):
        words = re.findall(r"[a-z0-9']+", text.lower())
        return [word for word in words if word not in STOP_WORDS]

    def _build_idf(self, chunks: list[DocumentChunk]):
        document_frequency = Counter()

        for chunk in chunks:
            document_frequency.update(set(self._tokenize(chunk.text)))

        document_count = max(len(chunks), 1)
        return {
            word: math.log((1 + document_count) / (1 + frequency)) + 1
            for word, frequency in document_frequency.items()
        }

    def _make_vector(self, text: str):
        tokens = self._tokenize(text)
        if not tokens:
            return {}

        counts = Counter(tokens)
        token_count = len(tokens)

        return {
            word: (count / token_count) * self.idf.get(word, 0)
            for word, count in counts.items()
        }

    @staticmethod
    def _cosine_similarity(left, right):
        shared_words = set(left) & set(right)
        numerator = sum(left[word] * right[word] for word in shared_words)

        left_length = math.sqrt(sum(value * value for value in left.values()))
        right_length = math.sqrt(sum(value * value for value in right.values()))

        if not left_length or not right_length:
            return 0.0

        return numerator / (left_length * right_length)

    def search(self, query: str, limit: int = 3):
        query_vector = self._make_vector(query)
        scored_results = []

        for chunk, vector in zip(self.chunks, self.vectors):
            score = self._cosine_similarity(query_vector, vector)
            if score > 0:
                scored_results.append(
                    SearchResult(
                        source=chunk.source,
                        chunk_number=chunk.chunk_number,
                        text=chunk.text,
                        score=round(score, 4),
                    )
                )

        return sorted(scored_results, key=lambda result: result.score, reverse=True)[:limit]
