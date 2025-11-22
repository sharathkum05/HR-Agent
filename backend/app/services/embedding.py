from openai import OpenAI
from app.config import settings
from typing import List
import os

client = OpenAI(api_key=settings.openai_api_key)


def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generate embedding for text using OpenAI embeddings API.
    
    Args:
        text: Input text to embed
        model: Embedding model to use (default: text-embedding-3-small)
    
    Returns:
        List of floats representing the embedding vector
    """
    try:
        # Truncate text if too long (max tokens for embedding)
        max_chars = 8000  # Safe limit for text-embedding-3-small
        if len(text) > max_chars:
            text = text[:max_chars]
        
        response = client.embeddings.create(
            model=model,
            input=text
        )
        
        return response.data[0].embedding
    except Exception as e:
        raise Exception(f"Error generating embedding: {str(e)}")

