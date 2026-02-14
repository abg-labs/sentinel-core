import logging
from typing import Dict, Optional
from core.stream import TechnicalStream
from ai.base import BaseDetector

logger = logging.getLogger(__name__)

class StreamManager:
    """
    Orchestrator for concurrent surveillance streams.
    Manages camera lifecycles and AI detector assignment.
    """
    def __init__(self):
        self.active_streams: Dict[int, TechnicalStream] = {}
        self.detector: Optional[BaseDetector] = None

    def set_detector(self, detector: BaseDetector):
        """Assign an active AI intelligence layer."""
        self.detector = detector
        logger.info(f"Situational intelligence layer assigned: {type(detector).__name__}")

    async def start_stream(self, camera_id: int, source: str):
        """Register and initiate a technical stream."""
        logger.info(f"Initiating stream acquisition: {camera_id} from {source}")
        # Implementation details for stream acquisition to follow in v0.2.0

    async def stop_stream(self, camera_id: int):
        """Terminate and cleanup a stream."""
        if camera_id in self.active_streams:
            logger.info(f"Terminating stream session: {camera_id}")
            self.active_streams.pop(camera_id)
