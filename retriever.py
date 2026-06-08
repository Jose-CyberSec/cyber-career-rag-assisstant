import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

_client = chromadb.PersistentClient(path=CHROMA_PATH)

_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection."""
    return _collection


def embed_and_store(chunks):
    """Embed chunks and store them in ChromaDB."""
    if not chunks:
        print("No chunks to store.")
        return

    _collection.add(
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"]} for c in chunks],
        ids=[c["chunk_id"] for c in chunks],
    )

    print(f"Stored {_collection.count()} total chunks in the vector database.")


def retrieve(query, n_results=N_RESULTS):
    """Retrieve the most relevant chunks for a user query."""
    if _collection.count() == 0:
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        chunk = {
            "text": document,
            "source": metadata.get("source", "Unknown Source"),
            "distance": distance,
        }

        chunks.append(chunk)

        print(
            f"[{chunk['source']}] "
            f"(dist: {chunk['distance']:.3f}) "
            f"{chunk['text'][:100]}..."
        )

    return chunks