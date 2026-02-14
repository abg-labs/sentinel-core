import logging
import threading
import json
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Institutional Defaults
DEFAULT_MODEL = "ViT-L/14"

@dataclass
class SemanticResult:
    """
    Standardized result for a sovereign search query.
    """
    id: str
    camera_id: int
    timestamp: datetime
    similarity: float
    metadata: Dict[str, Any]

class SemanticEngine:
    """
    Sovereign Semantic Search Engine.
    Utilizes CLIP embeddings to enable natural language querying across technical data streams.
    """
    def __init__(self, index_dir: str = "./search_index"):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        self.embeddings: Dict[str, np.ndarray] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        self.embedding_matrix: Optional[np.ndarray] = None
        self.entry_ids: List[str] = []
        
        self.lock = threading.Lock()
        self._model = None
        self._preprocess = None
        self._device = None
        
        self._load_index()

    def _ensure_model(self):
        """Lazy load the vision-language model."""
        if self._model is not None:
            return

        try:
            import torch
            import clip
            self._device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Loading Semantic Intelligence Model ({DEFAULT_MODEL}) on {self._device}...")
            self._model, self._preprocess = clip.load(DEFAULT_MODEL, device=self._device)
        except ImportError:
            logger.error("CLIP dependencies missing. Installation required: pip install git+https://github.com/openai/CLIP.git")
            raise

    def _load_index(self):
        """Load sovereign embeddings from persistent storage."""
        meta_file = self.index_dir / "index_metadata.json"
        matrix_file = self.index_dir / "embeddings.npy"
        
        if meta_file.exists() and matrix_file.exists():
            try:
                with open(meta_file, 'r') as f:
                    data = json.load(f)
                self.metadata = data['metadata']
                self.entry_ids = data['entry_ids']
                self.embedding_matrix = np.load(matrix_file)
                logger.info(f"Sovereign Index loaded: {len(self.entry_ids)} entries.")
            except Exception as e:
                logger.error(f"Index restoration failure: {e}")

    def index(self, frame: np.ndarray, camera_id: int, metadata: Optional[Dict[str, Any]] = None):
        """
        Ingest and index a frame into the semantic memory.
        """
        self._ensure_model()
        import torch
        from PIL import Image

        # Preprocessing
        pil_img = Image.fromarray(frame[:, :, ::-1]) # BGR to RGB
        img_input = self._preprocess(pil_img).unsqueeze(0).to(self._device)

        with torch.no_grad():
            features = self._model.encode_image(img_input)
            features /= features.norm(dim=-1, keepdim=True)
            embedding = features.cpu().numpy().flatten()

        entry_id = f"unit{camera_id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        with self.lock:
            self.entry_ids.append(entry_id)
            self.metadata[entry_id] = {
                "camera_id": camera_id,
                "timestamp": datetime.now().isoformat(),
                **(metadata or {})
            }
            
            if self.embedding_matrix is None:
                self.embedding_matrix = embedding.reshape(1, -1)
            else:
                self.embedding_matrix = np.vstack([self.embedding_matrix, embedding])

    def query(self, text: str, top_k: int = 5) -> List[SemanticResult]:
        """
        Execute a natural language query against the semantic index.
        """
        if not self.entry_ids: return []
        
        self._ensure_model()
        import torch
        import clip

        tokens = clip.tokenize([text]).to(self._device)
        with torch.no_grad():
            text_features = self._model.encode_text(tokens)
            text_features /= text_features.norm(dim=-1, keepdim=True)
            query_emb = text_features.cpu().numpy().flatten()

        # Compute similarities via dot product
        similarities = np.dot(self.embedding_matrix, query_emb)
        
        results = []
        for idx, entry_id in enumerate(self.entry_ids):
            meta = self.metadata[entry_id]
            results.append(SemanticResult(
                id=entry_id,
                camera_id=meta['camera_id'],
                timestamp=datetime.fromisoformat(meta['timestamp']),
                similarity=float(similarities[idx]),
                metadata=meta
            ))

        results.sort(key=lambda x: x.similarity, reverse=True)
        return results[:top_k]
