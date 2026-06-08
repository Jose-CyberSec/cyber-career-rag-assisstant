import os
import re
from config import DOCS_PATH


def clean_text(text):
    """Basic text cleaning for copied/plain-text career documents."""
    text = re.sub(r"\s+", " ", text)
    text = text.replace("&amp;", "&")
    text = text.replace("&nbsp;", " ")
    return text.strip()


def load_documents():
    """Load all .txt documents from the docs folder."""
    documents = []

    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                raw_text = f.read()

            cleaned = clean_text(raw_text)

            documents.append({
                "source": filename,
                "text": cleaned,
            })

    print(f"Loaded {len(documents)} document(s): {[d['source'] for d in documents]}")
    return documents


def chunk_document(text, source):
    """
    Split a document into chunks for embedding.

    Strategy:
    - 500-character chunks preserve full career/certification ideas.
    - 100-character overlap helps preserve context across boundaries.
    - 50-character minimum filters out tiny fragments.
    """
    chunk_size = 500
    overlap = 100
    min_length = 50

    chunks = []
    prefix = source.replace(".txt", "").replace(" ", "_").lower()
    counter = 0

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()

        if len(chunk_text) >= min_length:
            chunks.append({
                "text": chunk_text,
                "source": source,
                "chunk_id": f"{prefix}_{counter}",
            })
            counter += 1

        start += chunk_size - overlap

    return chunks