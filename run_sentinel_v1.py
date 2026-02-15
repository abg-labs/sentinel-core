import cv2
import asyncio
import logging
import threading
import webbrowser
import time
import uvicorn
from camera.processor import StreamProcessor
from dashboard.backend import app, semantic_engine, memory

import shutil
from pathlib import Path

# Institutional Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("sentinel.v1")

def cleanup_session():
    """Wipe all ephemeral session data to protect privacy and prevent bloat."""
    logger.info("Initiating Ephemeral Data Purge...")
    try:
        # 1. Wipe Search Index (Snapshots + Embeddings)
        if Path("search_index").exists():
            shutil.rmtree("search_index")
            logger.info("Search Index Purged.")
        
        # 2. Wipe Memory Vault (SQLite)
        db_path = Path("sentinel_memory.db")
        if db_path.exists():
            db_path.unlink()
            logger.info("Sovereign Memory Vault Dissolved.")
            
        logger.info("Cleanup Protocol Complete. No traces remain.")
    except Exception as e:
        logger.error(f"Cleanup Protocol Failure: {e}")

def run_backend():
    """Run the FastAPI backend in a dedicated thread."""
    logger.info("Initializing Sovereign Backend on Port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")

async def run_sentinel_engine():
    """
    Main Sentinel Engine: Ingestion + Semantic Indexing.
    """
    logger.info("Initializing Sentinel Engine (v0.8.0)...")
    
    # Use Shared Components from backend
    processor = StreamProcessor(source=0, camera_id=202, fps=15)
    
    if not processor.connect():
        logger.error("Optical source acquisition failed.")
        return

    logger.info("Mission Started. Indexing situational data. Dashboard: http://localhost:8000")
    
    # Give the backend a second to start before opening browser
    time.sleep(2)

    async def operational_callback(frame, frame_id):
        # Index every 30 frames (approx every 2 seconds at 15fps)
        if frame_id % 30 == 0:
            logger.info(f"Indexing Situational Snapshot: Frame {frame_id}")
            # Run indexing in a thread to not block the stream
            threading.Thread(target=semantic_engine.index, args=(frame, 202)).start()

        # Local Visualizer (Technical Overlay)
        cv2.putText(frame, "SENTINEL | RECORDING ACTIVE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("SENTINEL | Institutional Eye", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            processor.is_running = False

    try:
        await processor.start_processing(operational_callback)
    finally:
        logger.info("Operational session finalized.")
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # 1. Start Backend Thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()

    # 2. Start Lens + Engine
    try:
        asyncio.run(run_sentinel_engine())
    finally:
        # ALWAYS cleanup on exit
        cleanup_session()
