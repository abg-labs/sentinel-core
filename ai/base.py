from typing import List, Dict, Tuple, Optional
import numpy as np

class Detection:
    """
    Standardized container for situational awareness data.
    """
    def __init__(
        self,
        class_id: int,
        class_name: str,
        confidence: float,
        bbox: Tuple[float, float, float, float],
        track_id: Optional[int] = None,
    ):
        self.class_id = class_id
        self.class_name = class_name
        self.confidence = confidence
        self.bbox = bbox  # (x1, y1, x2, y2) normalized 0-1
        self.track_id = track_id

    def to_dict(self) -> dict:
        """Serialize detection for transmission or storage."""
        return {
            "class_id": self.class_id,
            "class_name": self.class_name,
            "confidence": float(self.confidence),
            "bbox": {
                "x1": float(self.bbox[0]),
                "y1": float(self.bbox[1]),
                "x2": float(self.bbox[2]),
                "y2": float(self.bbox[3]),
            },
            "track_id": self.track_id,
        }

class BaseDetector:
    """
    Interface for AI model integration. 
    Can be extended for YOLO, CLIP, or custom classification models.
    """
    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold

    def detect(self, frame: np.ndarray) -> List[Detection]:
        """Run inference on a single frame."""
        raise NotImplementedError("Detectors must implement the detect method.")
