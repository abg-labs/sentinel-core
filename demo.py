import cv2
import asyncio
import logging
from sentinel.core.stream import TechnicalStream
from sentinel.ai.base import BaseDetector
from sentinel.ai.detector import YOLODetector
from sentinel.ai.zone import ZoneEngine, ZoneConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("sentinel.demo")

async def run_visual_demo():
    """
    Sentinel v0.2.0 Visual Demo
    Connects to the default camera and runs real-time object detection.
    """
    logger.info("Initializing Sentinel Situational Awareness Demo...")
    
    # 1. Initialize the Intelligence Layer (using YOLOv8n)
    # Note: If no GPU is found, it will default to CPU automatically.
    detector = YOLODetector(model_type="yolov8n", confidence_threshold=0.3)
    
    # 2. Initialize the Zone Engine and define a "Restricted Area"
    # Polygon coordinates are normalized (0-1)
    zone_engine = ZoneEngine()
    restricted_zone = ZoneConfig(
        id=1,
        name="RESTRICTED PERSONNEL ZONE",
        coordinates=[[0.3, 0.3], [0.7, 0.3], [0.7, 0.7], [0.3, 0.7]], # Center box
        zone_type="restricted",
        color="#ef4444" # Alert Red
    )
    zone_engine.add_zone(restricted_zone)

    # 3. Initialize the Stream Processor (0 is usually the default webcam)
    # You can replace 0 with an RTSP URL or a video file path.
    processor = StreamProcessor(source=0, camera_id=999, fps=30)
    
    if not processor.connect():
        logger.error("Failed to acquire camera source. Ensure webcam is connected.")
        return

    logger.info("Stream acquired. Press 'q' in the window to terminate session.")

    async def detection_callback(frame, frame_id):
        # Run intelligence inference
        detections = detector.detect(frame)
        
        # Process situational zones
        violations = zone_engine.process(detections)
        
        # Render tactical overlays
        output_frame = zone_engine.overlay(frame, violations)
        h, w = frame.shape[:2]
        
        for det in detections:
            x1, y1, x2, y2 = det.bbox
            cv2.rectangle(
                output_frame, 
                (int(x1*w), int(y1*h)), 
                (int(x2*w), int(y2*h)), 
                (216, 79, 31), # AB Strategic Blue
                2
            )
            cv2.putText(
                output_frame, 
                f"{det.class_name} {det.confidence:.2f}",
                (int(x1*w), int(y1*h) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (216, 79, 31), 1
            )

        # Show the institutional visualizer
        cv2.imshow("SENTINEL | Situational Awareness Terminal", output_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            processor.is_running = False

    # Start the continuous awareness cycle
    await processor.start_processing(detection_callback)
    
    cv2.destroyAllWindows()
    logger.info("Surveillance session terminated.")

if __name__ == "__main__":
    try:
        asyncio.run(run_visual_demo())
    except KeyboardInterrupt:
        pass
