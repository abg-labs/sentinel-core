import cv2
import numpy as np
import logging
import asyncio
from typing import Optional, Tuple, Callable
from datetime import datetime

logger = logging.getLogger(__name__)

class StreamProcessor:
    """
    High-performance video acquisition and processing engine.
    Handles stream connectivity, FPS management, and frame normalization.
    """
    def __init__(
        self,
        source: str,
        camera_id: int,
        fps: int = 30,
        resolution: Tuple[int, int] = (1920, 1080),
    ):
        self.source = source
        self.camera_id = camera_id
        self.fps = fps
        self.resolution = resolution
        
        self.capture: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.frame_count = 0
        self.last_frame_time = None

    def connect(self) -> bool:
        """Initiate connection to the mission-critical data source."""
        try:
            logger.info(f"Acquiring stream for Unit {self.camera_id}: {self.source}")
            self.capture = cv2.VideoCapture(self.source)
            
            if not self.capture.isOpened():
                logger.error("Source acquisition failed. Verify stream protocol.")
                return False

            return True
        except Exception as e:
            logger.error(f"Acquisition error: {e}")
            return False

    async def start_processing(self, callback: Callable[[np.ndarray, int], None]):
        """Continuous situational awareness cycle."""
        if not self.capture or not self.capture.isOpened():
            return

        self.is_running = True
        frame_delay = 1.0 / self.fps

        try:
            while self.is_running:
                ret, frame = self.capture.read()
                if not ret or frame is None:
                    logger.warning("Frame drop detected. Re-evaluating stream health.")
                    await asyncio.sleep(1)
                    continue

                self.frame_count += 1
                self.last_frame_time = datetime.utcnow()
                
                # Execute situational awareness callback
                await callback(frame, self.frame_count)
                
                await asyncio.sleep(frame_delay)
        finally:
            self.is_running = False
            if self.capture:
                self.capture.release()
