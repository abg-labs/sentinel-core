"""
Sentinel Core - Institutional Usage Example
This script demonstrates how to utilize the v0.1.0 architectural primitives.
"""

import asyncio
import logging
from ai.base import BaseDetector, Detection
from core.manager import StreamManager

# Configure institutional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger("sentinel.example")

class MockSituationalDetector(BaseDetector):
    """
    A mock implementation of a detector for framework verification.
    In v0.3.0, this will be replaced by native YOLO/CLIP wrappers.
    """
    def detect(self, frame):
        logger.info("Inference cycle executed on mission-critical frame.")
        # Simulating a detection of a high-value asset
        return [
            Detection(
                class_id=0, 
                class_name="unauthorized_entry", 
                confidence=0.99, 
                bbox=(0.2, 0.2, 0.4, 0.4)
            )
        ]

async def run_surveillance_session():
    """
    Example workflow for initiating a surveillance session.
    """
    # 1. Initialize the Stream Orchestrator
    manager = StreamManager()
    
    # 2. Assign the Intelligence Layer
    detector = MockSituationalDetector(confidence_threshold=0.85)
    manager.set_detector(detector)
    
    # 3. Register a Technical Stream
    # Note: Stream ingestion logic will be fully implemented in v0.2.0
    await manager.start_stream(
        camera_id=101, 
        source="rtsp://secure-intelligence-feed.local/unit-1"
    )
    
    logger.info("Surveillance session initiated successfully.")

if __name__ == "__main__":
    asyncio.run(run_surveillance_session())
