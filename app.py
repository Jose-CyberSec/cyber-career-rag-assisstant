import gradio as gr

from ingest import load_documents, chunk_document
from retriever import get_collection, embed_and_store, retrieve
from generator import generate_response


def ingest_documents_if_needed():
    collection = get_collection()

    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        print("To re-ingest, delete the ./chroma_db folder and restart.")
        return

    print("Ingesting cyber career documents...")

    documents = load_documents()
    all_chunks = []

    for doc in documents:
        chunks = chunk_document(doc["text"], doc["source"])
        all_chunks.extend(chunks)

    embed_and_store(all_chunks)
    print(f"Ingestion complete. {len(all_chunks)} chunks stored.")


def ask(question):
    if not question.strip():
        return "Please enter a question."

    chunks = retrieve(question)
    answer = generate_response(question, chunks)

    sources = sorted({chunk["source"] for chunk in chunks})
    source_text = "\n\nSources retrieved:\n" + "\n".join(f"- {s}" for s in sources)

    return answer + source_text


def main():
    print("=" * 60)
    print("Cyber Career RAG Assistant - starting up")
    print("=" * 60)

    ingest_documents_if_needed()

    with gr.Blocks(title="Cyber Career RAG Assistant") as demo:
        gr.Markdown("# Cyber Career RAG Assistant")
        gr.Markdown(
            "Ask questions about cybersecurity careers, certifications, job skills, and portfolio projects. "
            "Answers are grounded in the collected documents."
        )

        question = gr.Textbox(
            label="Ask a question",
            placeholder="Example: What topics does Security+ cover?",
            lines=2,
        )

        submit = gr.Button("Ask")

        answer = gr.Textbox(
            label="Grounded Answer",
            lines=12,
        )

        submit.click(fn=ask, inputs=question, outputs=answer)
        question.submit(fn=ask, inputs=question, outputs=answer)

    demo.launch(share=True)


if __name__ == "__main__":
    main()