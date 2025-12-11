"""
LLM service for generating RAG responses.
Supports OpenAI GPT-4 and Anthropic Claude models.
"""
from typing import List, Dict, Any
from openai import OpenAI
from anthropic import Anthropic
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Initialize clients
openai_client = OpenAI(api_key=settings.openai_api_key)
anthropic_client = Anthropic(api_key=settings.anthropic_api_key)


def generate_rag_prompt(query: str, context_chunks: List[Dict[str, Any]]) -> str:
    """
    Generate RAG prompt with context chunks.

    Args:
        query: User's query
        context_chunks: List of relevant document chunks

    Returns:
        Formatted prompt with context
    """
    prompt = "You are a helpful assistant that answers questions based on the provided context.\n\n"
    prompt += "Context from documents:\n\n"

    for i, chunk in enumerate(context_chunks, 1):
        prompt += f"[{i}] {chunk['text']}\n\n"

    prompt += f"\nQuestion: {query}\n\n"
    prompt += "Please provide a comprehensive answer based on the context above. "
    prompt += "If the answer cannot be found in the context, say so. "
    prompt += "Include relevant citations using [1], [2], etc. to reference the context chunks."

    return prompt


def generate_response_openai(query: str, context_chunks: List[Dict[str, Any]], model: str = "gpt-4") -> str:
    """
    Generate response using OpenAI GPT models.

    Args:
        query: User's query
        context_chunks: Relevant document chunks
        model: Model to use (default: gpt-4)

    Returns:
        Generated response
    """
    try:
        logger.info(f"Generating response with OpenAI {model}")

        # Create prompt with context
        prompt = generate_rag_prompt(query, context_chunks)

        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        answer = response.choices[0].message.content
        logger.info("Successfully generated OpenAI response")
        return answer

    except Exception as e:
        logger.error(f"Error generating OpenAI response: {e}")
        raise


def generate_response_anthropic(query: str, context_chunks: List[Dict[str, Any]], model: str = "claude-3-5-sonnet-20241022") -> str:
    """
    Generate response using Anthropic Claude models.

    Args:
        query: User's query
        context_chunks: Relevant document chunks
        model: Model to use (default: claude-3-5-sonnet-20241022)

    Returns:
        Generated response
    """
    try:
        logger.info(f"Generating response with Anthropic {model}")

        # Create prompt with context
        prompt = generate_rag_prompt(query, context_chunks)

        # Call Anthropic API
        response = anthropic_client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.content[0].text
        logger.info("Successfully generated Anthropic response")
        return answer

    except Exception as e:
        logger.error(f"Error generating Anthropic response: {e}")
        raise


def generate_rag_response(
    query: str,
    context_chunks: List[Dict[str, Any]],
    model: str = "gpt-4"
) -> str:
    """
    Generate RAG response using specified model.

    Args:
        query: User's query
        context_chunks: Relevant document chunks with metadata
        model: Model to use (gpt-4 or claude-3-5-sonnet)

    Returns:
        Generated response
    """
    if not context_chunks:
        return "I couldn't find any relevant information in the documents to answer your question."

    # Route to appropriate model
    if model == "claude-3-5-sonnet" or model.startswith("claude"):
        return generate_response_anthropic(query, context_chunks)
    else:
        return generate_response_openai(query, context_chunks, model)
