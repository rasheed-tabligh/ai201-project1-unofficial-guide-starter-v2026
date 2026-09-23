"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents on paragraph breaks, then merge the short paragraphs.

    Each document is cut on blank lines. Consecutive paragraphs are joined
    while the combined text stays under 400 characters, so a run of one-line
    paragraphs becomes one chunk instead of several fragments. Anything still
    under 100 characters is folded into the chunk before it, on the grounds
    that a paragraph that short rarely carries enough context to answer a
    question on its own.

    Whitespace is stripped and empty results are dropped. `index` counts from
    0 within each source document, and every chunk is stamped
    "chunker.py::split_documents".
    """
    max_chars = 400
    min_chars = 100

    chunks: list[Chunk] = []
    for doc in documents:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", doc.text)]
        paragraphs = [p for p in paragraphs if p]

        # Group paragraphs while they still fit under max_chars.
        grouped: list[str] = []
        for para in paragraphs:
            if grouped and len(grouped[-1]) + 2 + len(para) < max_chars:
                grouped[-1] = f"{grouped[-1]}\n\n{para}"
            else:
                grouped.append(para)

        # A group that is still too short belongs with the one before it.
        merged: list[str] = []
        for group in grouped:
            if merged and len(group) < min_chars:
                merged[-1] = f"{merged[-1]}\n\n{group}"
            else:
                merged.append(group)

        for index, text in enumerate(merged):
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
