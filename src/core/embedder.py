"""Local embedding service using sentence-transformers.

Provides a singleton wrapper around a local embedding model (default: BAAI/bge-m3)
for encoding text chunks and queries into dense vectors for semantic search.
"""

import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", "64"))
EMBEDDING_ENABLED = os.getenv("EMBEDDING_ENABLED", "true").lower() == "true"

# Known bare model names that are missing their HuggingFace org prefix.
# A stray shell env like `EMBEDDING_MODEL=bge-m3` (no "BAAI/") makes
# sentence-transformers fail to resolve the model, silently disabling the
# vector store (see Redmine #66). Normalize such names back to their full id.
_MODEL_ALIASES = {
    "bge-m3": "BAAI/bge-m3",
    "bge-large-zh-v1.5": "BAAI/bge-large-zh-v1.5",
    "bge-large-en-v1.5": "BAAI/bge-large-en-v1.5",
    "bge-base-zh-v1.5": "BAAI/bge-base-zh-v1.5",
}


def _normalize_model_name(name):
    """Repair a model id that lost its HF org prefix (e.g. 'bge-m3').

    Only rewrites known bare names; anything already namespaced (contains '/')
    or a local path is returned unchanged.
    """
    if not name:
        return name
    n = name.strip()
    if "/" in n or os.path.sep in n:
        return n  # already a full repo id or a local path
    return _MODEL_ALIASES.get(n, n)


EMBEDDING_MODEL = _normalize_model_name(os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3"))


class LocalEmbedder:
    """Singleton wrapper around sentence-transformers model for local embedding.
    
    Usage:
        embedder = LocalEmbedder.get_instance()
        vectors = embedder.encode(["text1", "text2"])
        query_vec = embedder.encode_query("search query")
    """

    _instance = None
    _initialized = False

    def __init__(self, model_name=None, device=None):
        """Initialize the embedding model. Use get_instance() for singleton access."""
        if not EMBEDDING_ENABLED:
            raise RuntimeError("Embedding is disabled (EMBEDDING_ENABLED=false)")

        model_name = _normalize_model_name(model_name or EMBEDDING_MODEL)
        device = device or EMBEDDING_DEVICE

        print(f"🔄 Loading embedding model: {model_name} (device={device})...")
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name, device=device)
            self.dimension = self.model.get_sentence_embedding_dimension()
            self.model_name = model_name
            self._initialized = True
            print(f"✅ Embedding model loaded: {model_name} (dim={self.dimension})")
        except Exception as e:
            self._initialized = False
            raise RuntimeError(f"Failed to load embedding model: {e}")

    @classmethod
    def get_instance(cls):
        """Get or create the singleton embedder instance.
        
        Returns:
            LocalEmbedder instance, or None if loading fails.
        """
        if cls._instance is None:
            try:
                cls._instance = cls()
            except RuntimeError as e:
                print(f"⚠️ Embedding unavailable: {e}")
                return None
        return cls._instance

    @classmethod
    def reset(cls):
        """Reset singleton (for testing or model switching)."""
        cls._instance = None

    @property
    def is_ready(self):
        """Check if model is loaded and ready."""
        return self._initialized

    def encode(self, texts: list, batch_size=None, show_progress=True) -> np.ndarray:
        """Encode a list of texts into embedding vectors.
        
        Args:
            texts: List of strings to encode.
            batch_size: Batch size for encoding (default from env).
            show_progress: Show progress bar for large batches.
            
        Returns:
            numpy array of shape (N, dimension) with float32 normalized vectors.
        """
        if not self._initialized:
            raise RuntimeError("Embedding model not initialized")

        if not texts:
            return np.empty((0, self.dimension), dtype=np.float32)

        batch_size = batch_size or EMBEDDING_BATCH_SIZE
        show_bar = show_progress and len(texts) > batch_size

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=show_bar,
            convert_to_numpy=True,
        )
        return embeddings.astype(np.float32)

    def encode_query(self, query: str) -> np.ndarray:
        """Encode a single query string into an embedding vector.
        
        Args:
            query: The search query string.
            
        Returns:
            numpy array of shape (dimension,) with float32 normalized vector.
        """
        if not self._initialized:
            raise RuntimeError("Embedding model not initialized")

        embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        return embedding[0].astype(np.float32)
