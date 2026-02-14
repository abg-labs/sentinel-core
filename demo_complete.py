import cv2
import asyncio
import logging
from camera.processor import StreamProcessor
from ai.detector import YOLODetector
from core.alerts import AlertManager, TelegramProtocol, AlertSeverity
from core.recorder import VideoRecorder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("sentinel.complete_demo")

async def run_complete_demo():
    """
    Sentinel v0.4.0 Complete Operational Demo.
    Demonstrates Detection -> Alerting -> Evidence Persistence.
    """
    logger.info("Initializing Sentinel Operational Pipeline...")

    # 1. Initialize Components
    detector = YOLODetector(confidence_threshold=0.4)
    recorder = VideoRecorder(output_dir="./sentinel_evidence")
    
    # 2. Configure Alerting (Example using Mock values)
    alert_manager = AlertManager()
    # To test actual Telegram, provide real tokens:
    # alert_manager.register_protocol(TelegramProtocol(bot_token="YOUR_TOKEN", chat_id="YOUR_ID"))
    
    # 3. Initialize Stream
    processor = StreamProcessor(source=0, camera_id=202, fps=30)
    
    if not processor.connect():
        logger.error("Source acquisition failed.")
        return

    logger.info("Mission Started. Monitoring for high-value targets. Press 'q' to terminate.")

    async def operational_callback(frame, frame_id):
        # detection
        detections = detector.detect(frame)
        
        # Check for 'person' as a trigger for recording and alerting
        has_person = any(d.class_name == "person" for d in detections)
        
        # 4. Recording with Pre-event Buffer
        # If no person is present, it just fills the buffer.
        # Once a person is detected, it flushes the buffer and starts writing the file.
        recorder.write(frame, trigger=has_person)
        
        if has_person:
            # 5. Alert Dispatch
            # We notify on first detection (demonstration purpose)
            if frame_id % 100 == 0: # Rate limit alerts for demo
                 await alert_manager.notify(
                    title="UNAUTHORIZED ACCESS",
                    message="Human detection verified in secure sector.",
                    severity=AlertSeverity.HIGH,
                    metadata={"camera_id": 202}
                )

        # Tactical Overlay
        h, w = frame.shape[:2]
        for det in detections:
            x1, y1, x2, y2 = det.bbox
            cv2.rectangle(frame, (int(x1*w), int(y1*h)), (int(x2*w), int(y2*h)), (0, 0, 255) if has_person else (255, 0, 0), 2)
        
        cv2.imshow("SENTINEL | Operational Eye", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            processor.is_running = False

    # Start the cycle
    try:
        await processor.start_processing(operational_callback)
    finally:
        recorder.stop()
        cv2.destroyAllWindows()
        logger.info("Operational session finalized.")

if __name__ == "__main__":
    try:
        asyncio.run(run_complete_demo())
    except KeyboardInterrupt:
        pass
