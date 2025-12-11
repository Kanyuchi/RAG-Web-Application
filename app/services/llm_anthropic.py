"""
Anthropic Claude integration for RAG query processing.
"""
import anthropic
import os

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_API_KEY"))

def query_rag_system(query: str, context_chunks: list):
    """
    Query the RAG system using Anthropic's Claude models.

    Args:
        query: User's question
        context_chunks: List of relevant context chunks from retrieval

    Returns:
        Generated response from the LLM
    """
    prompt = f"Use the following context to answer the question:\n{context_chunks}\n\nQuestion: {query}"

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text
