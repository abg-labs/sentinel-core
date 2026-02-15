import cv2
import numpy as np
import logging
from typing import List, Optional, Tuple
from ai.base import BaseDetector, Detection
from core.accelerator import HardwareAccelerator

# Note: Requires 'ultralytics' to be installed for full functionality
try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None

logger = logging.getLogger(__name__)

class YOLODetector(BaseDetector):
    """
    Standardized wrapper for YOLO-based situational awareness.
    Optimized for high-throughput detection in mission-critical deployments.
    """
    def __init__(
        self,
        model_type: str = "yolov8n",
        confidence_threshold: float = 0.5,
        device: Optional[str] = None
    ):
        super().__init__(confidence_threshold)
        self.model_type = model_type
        # Use provided device or auto-detect via accelerator
        self.device = device or HardwareAccelerator.get_device()
        self.model = None
        self._load_model()

    def _load_model(self):
        if YOLO is None:
            logger.warning("Ultralytics library not found. Running in Schema-Only mode.")
            return

        try:
            self.model = YOLO(f"{self.model_type}.pt")
            # Apply institutional optimizations
            HardwareAccelerator.optimize_model(self.model)
            logger.info(f"Intelligence model {self.model_type} synchronized with {self.device}")
        except Exception as e:
            logger.error(f"Intelligence loading error: {e}")

    def detect(self, frame: np.ndarray) -> List[Detection]:
        if self.model is None:
            return []

        results = self.model(frame, conf=self.confidence_threshold, verbose=False)[0]
        detections = []
        h, w = frame.shape[:2]

        for box in results.boxes:
            class_id = int(box.cls[0])
            class_name = self.model.names[class_id]
            confidence = float(box.conf[0])
            
            # Normalize BBox (x1, y1, x2, y2)
            coords = box.xyxy[0].cpu().numpy()
            bbox = (coords[0]/w, coords[1]/h, coords[2]/w, coords[3]/h)

            detections.append(Detection(
                class_id=class_id,
                class_name=class_name,
                confidence=confidence,
                bbox=bbox
            ))

        return detections
