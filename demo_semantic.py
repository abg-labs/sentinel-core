import cv2
import asyncio
import logging
from sentinel.camera.processor import StreamProcessor
from sentinel.ai.semantic import SemanticEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("sentinel.semantic_demo")

async def run_semantic_demo():
    """
    Sentinel v0.3.0 Semantic Search Demo
    Indexes frames in real-time and allows for natural language querying.
    """
    logger.info("Initializing Sentinel Semantic Memory Engine...")
    
    # 1. Initialize the Semantic Engine
    engine = SemanticEngine()
    
    # 2. Initialize the Stream Processor (using default webcam)
    processor = StreamProcessor(source=0, camera_id=101, fps=5) # Lower FPS for indexing demo
    
    if not processor.connect():
        logger.error("Failed to acquire camera source.")
        return

    logger.info("Stream acquired. Indexing start. Sit in front of the camera for 10 seconds.")

    async def indexing_callback(frame, frame_id):
        # Index every 5th frame to save on compute
        if frame_id % 5 == 0:
            logger.info(f"Indexing Frame {frame_id} into Semantic Memory...")
            engine.index(frame, camera_id=101)
        
        cv2.imshow("SENTINEL | Semantic Ingestion", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or frame_id > 50:
            processor.is_running = False

    # Start ingestion
    await processor.start_processing(indexing_callback)
    cv2.destroyAllWindows()
    
    logger.info("Ingestion phase complete. Entering Sovereign Query Mode.")
    
    # 3. Query Phase
    queries = [
        "a person wearing a dark shirt",
        "a person looking at the camera",
        "empty background"
    ]
    
    for query_text in queries:
        logger.info(f"EXECUTING QUERY: '{query_text}'")
        results = engine.query(query_text, top_k=1)
        if results:
            res = results[0]
            logger.info(f"Top Match Found! ID: {res.id} | Score: {res.similarity:.4f}")
        else:
            logger.warning("No matches found in semantic index.")

if __name__ == "__main__":
    try:
        asyncio.run(run_semantic_demo())
    except KeyboardInterrupt:
        pass
