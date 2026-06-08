from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved cyber career documents.
    """
    fallback_message = "I do not have enough information in the collected documents to answer that."

    if not retrieved_chunks:
        return fallback_message

    context_blocks = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_blocks.append(
            f"--- Chunk {i} ---\n"
            f"Source: {chunk['source']}\n"
            f"Distance: {chunk['distance']:.3f}\n"
            f"Text:\n{chunk['text']}"
        )

    context = "\n\n".join(context_blocks)

    system_prompt = (
        "You are Cyber Career RAG Assistant. "
        "Answer the user's question using only the retrieved document context. "
        "Do not use outside knowledge, assumptions, or general career advice. "
        "If the answer is not clearly supported by the provided context, say: "
        "'I do not have enough information in the collected documents to answer that.' "
        "Cite the source document or documents used for your answer. "
        "Do not invent details, certifications, requirements, salaries, or recommendations."
    )

    user_prompt = (
        f"Retrieved context:\n{context}\n\n"
        f"User question:\n{query}"
    )

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )

    return response.choices[0].message.content