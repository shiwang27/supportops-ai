from dataclasses import dataclass

from vector_search import SearchResult, VectorSearch


@dataclass
class GroundedAnswer:
    answer: str
    sources: list[str]
    matches: list[SearchResult]


def answer_question(question: str, search_index: VectorSearch | None = None):
    search_index = search_index or VectorSearch.from_documents()
    results = search_index.search(question)

    if not results:
        return GroundedAnswer(
            answer="I could not find an answer in the support documents.",
            sources=[],
            matches=[],
        )

    answer_lines = ["Here is what I found in the support documents:"]
    for result in results:
        answer_lines.append(f"- {result.text} [{result.source}]")

    sources = sorted({result.source for result in results})
    return GroundedAnswer(
        answer="\n".join(answer_lines),
        sources=sources,
        matches=results,
    )
