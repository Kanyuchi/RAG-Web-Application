"""
OpenAI integration for RAG query processing.
"""
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

def query_rag_system(query: str, context_chunks: list):
    """
    Query the RAG system using OpenAI's GPT models.

    Args:
        query: User's question
        context_chunks: List of relevant context chunks from retrieval

    Returns:
        Generated response from the LLM
    """
    prompt = f"Use the following context to answer the question:\n{context_chunks}\n\nQuestion: {query}"
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500,
    )
    return response.choices[0].message.content
