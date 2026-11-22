"""
rag/embeddings.py
=================
Embedding generator for ThreatRAG dense retrieval.
Wraps SentenceTransformer with local disk caching and CPU-optimized inference.
Provides a deterministic fallback embedding model for offline/air-gapped resilience.
"""

import os
import hashlib
import numpy as np
from typing import List, Union

# Ensure offline cache mode to avoid connection retries
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

class EmbeddingManager:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", cache_dir: str = "artifacts/embeddings_cache"):
        self.model_name = model_name
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.model = None
        self._dimension = 384
        self._init_model()

    def _init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            print(f"[EMBEDDINGS] Loading SentenceTransformer: {self.model_name}...")
            self.model = SentenceTransformer(self.model_name, device="cpu")
            self._dimension = self.model.get_sentence_embedding_dimension()
            print(f"[EMBEDDINGS] Model loaded successfully. Dimension: {self._dimension}")
        except Exception as e:
            print(f"[WARNING] Could not load SentenceTransformer ({e}). Initializing deterministic fallback embedding.")
            self.model = None
            self._dimension = 384

    @property
    def dimension(self) -> int:
        return self._dimension

    def encode(self, texts: Union[str, List[str]], batch_size: int = 32, normalize: bool = True) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            return np.empty((0, self._dimension), dtype=np.float32)

        if self.model is not None:
            try:
                embeddings = self.model.encode(
                    texts,
                    batch_size=batch_size,
                    show_progress_bar=False,
                    normalize_embeddings=normalize,
                    convert_to_numpy=True
                )
                return embeddings.astype(np.float32)
            except Exception as e:
                print(f"[EMBEDDINGS] Inference failed on model ({e}). Using fallback.")

        # Fallback: Deterministic character n-gram hashing embedding (ensures reproducibility)
        embeddings = []
        for text in texts:
            vec = np.zeros(self._dimension, dtype=np.float32)
            words = text.lower().split()
            for i, word in enumerate(words):
                h = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
                idx = h % self._dimension
                sign = 1.0 if ((h >> 8) % 2 == 0) else -1.0
                vec[idx] += sign * (1.0 / (1.0 + np.log1p(i)))
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec /= norm
            embeddings.append(vec)
        return np.array(embeddings, dtype=np.float32)
